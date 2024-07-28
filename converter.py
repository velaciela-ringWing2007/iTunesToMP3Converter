import os
import shutil
import ffmpeg
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import tkinter as tk
from tkinter import filedialog, messagebox


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

        process_directory(self.source_dir, self.target_dir)
        messagebox.showinfo("Success", "Conversion completed successfully")


# 関数部分
def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def copy_metadata(src, dst):
    audio = MP3(src, ID3=EasyID3)
    audio.save(dst, v2_version=3)


def convert_to_mp3(src_file, dst_file, bitrate='192k'):
    src_audio = MP3(src_file, ID3=EasyID3)
    src_metadata = {key: src_audio.get(key, [None])[0] for key in src_audio.keys()}

    ffmpeg.input(src_file).output(dst_file, audio_bitrate=bitrate).run()

    dst_audio = MP3(dst_file, ID3=EasyID3)
    for key, value in src_metadata.items():
        if value:
            dst_audio[key] = value
    dst_audio.save()


def process_directory(src_dir, dst_dir):
    for root, _, files in os.walk(src_dir):
        relative_path = os.path.relpath(root, src_dir)
        target_path = os.path.join(dst_dir, relative_path)
        ensure_dir_exists(target_path)

        for file in files:
            src_file = os.path.join(root, file)
            if file.lower().endswith('.mp3'):
                dst_file = os.path.join(target_path, file)
                shutil.copy2(src_file, dst_file)
                copy_metadata(src_file, dst_file)
            else:
                dst_file = os.path.join(target_path, os.path.splitext(file)[0] + '.mp3')
                src_audio = MP3(src_file)
                bitrate = src_audio.info.bitrate if hasattr(src_audio.info, 'bitrate') else 192000
                convert_to_mp3(src_file, dst_file, bitrate=str(bitrate) + 'k')


# GUIの実行部分
if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()
