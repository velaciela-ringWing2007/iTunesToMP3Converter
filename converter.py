import os
import shutil
import subprocess
from threading import Thread
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext


# GUI部分
class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("iTunes to MP3 Converter")

        self.source_dir = ""
        self.target_dir = ""

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="iTunes to MP3 Converter", font=("Helvetica", 16)).pack(pady=10)

        tk.Button(self.root, text="Select Source Directory", command=self.select_source).pack(pady=5)
        self.source_label = tk.Label(self.root, text="No directory selected", fg="red")
        self.source_label.pack(pady=5)

        tk.Button(self.root, text="Select Target Directory", command=self.select_target).pack(pady=5)
        self.target_label = tk.Label(self.root, text="No directory selected", fg="red")
        self.target_label.pack(pady=5)

        tk.Button(self.root, text="Start Conversion", command=self.start_conversion).pack(pady=20)

        self.log_text = scrolledtext.ScrolledText(self.root, width=80, height=20)
        self.log_text.pack(pady=10)

    def select_source(self):
        self.source_dir = filedialog.askdirectory()
        if self.source_dir:
            self.source_label.config(text=self.source_dir, fg="green")

    def select_target(self):
        self.target_dir = filedialog.askdirectory()
        if self.target_dir:
            self.target_label.config(text=self.target_dir, fg="green")

    def start_conversion(self):
        if not self.source_dir or not self.target_dir:
            messagebox.showerror("Error", "Please select both source and target directories")
            return

        self.log_text.delete(1.0, tk.END)
        thread = Thread(target=process_directory, args=(self.source_dir, self.target_dir, self.log_text))
        thread.start()


# 関数部分
def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def copy_metadata(src, dst):
    audio = MP3(src, ID3=EasyID3)
    audio.save(dst, v2_version=3)


def copy_mp4_metadata(src, dst):
    src_audio = MP4(src)
    dst_audio = MP3(dst, ID3=EasyID3)
    for key in src_audio.tags:
        try:
            if key.startswith("©"):
                dst_audio[key[1:]] = src_audio.tags[key]
            else:
                dst_audio[key] = src_audio.tags[key]
        except Exception as e:
            print(f"Skipping metadata key {key}: {e}")
    dst_audio.save(v2_version=3)


def convert_to_mp3(src_file, dst_file, bitrate='192k'):
    command = [
        'ffmpeg', '-i', src_file, '-b:a', bitrate, '-y', dst_file
    ]
    subprocess.run(command, check=True)


def process_directory(src_dir, dst_dir, log_widget):
    for root, _, files in os.walk(src_dir):
        relative_path = os.path.relpath(root, src_dir)
        target_path = os.path.join(dst_dir, relative_path)
        ensure_dir_exists(target_path)

        for file in files:
            src_file = os.path.join(root, file)
            parent_dir = os.path.basename(os.path.dirname(src_file))
            display_name = f"{parent_dir}/{file}"
            try:
                if file.lower().endswith('.mp3'):
                    dst_file = os.path.join(target_path, file)
                    log_widget.insert(tk.END, f"Copying {display_name}\n")
                    log_widget.see(tk.END)
                    shutil.copy2(src_file, dst_file)
                    copy_metadata(src_file, dst_file)
                elif file.lower().endswith('.m4a'):
                    dst_file = os.path.join(target_path, os.path.splitext(file)[0] + '.mp3')
                    log_widget.insert(tk.END, f"Converting {display_name}\n")
                    log_widget.see(tk.END)
                    convert_to_mp3(src_file, dst_file)
                    copy_mp4_metadata(src_file, dst_file)
            except Exception as e:
                log_widget.insert(tk.END, f"Skipping {display_name}: {e}\n")
                log_widget.see(tk.END)
    log_widget.insert(tk.END, "Conversion completed successfully.\n")
    log_widget.see(tk.END)


# GUIの実行部分
if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()
