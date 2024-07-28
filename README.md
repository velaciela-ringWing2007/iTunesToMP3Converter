以下は、ローカルにインストールされた`ffmpeg`を使用するために修正したREADME.mdファイルのテンプレートです。

### README.md

```markdown
# iTunesToMP3Converter

iTunesToMP3Converter is a Python script that converts iTunes music directories to MP3 format while preserving metadata such as album art, album name, track name, track number, artist name, and composer name. It maintains the directory structure and copies files to a specified output directory.

## Features

- Convert various audio formats (such as m4a) to MP3
- Preserve metadata including album art, album name, track name, track number, artist name, and composer name
- Maintain the original directory structure
- Specify output directory for converted files

## Requirements

- Python 3.6+
- ffmpeg (must be installed separately)
- mutagen

## Installation

1. Install `ffmpeg`. Follow the installation instructions for your operating system [here](https://ffmpeg.org/download.html).
   - **Windows**: Download the static build, extract the files, and add the directory containing `ffmpeg.exe` to your system's PATH.

2. Install the required Python packages:

```bash
pip install mutagen
```

## Usage

1. Clone the repository:

```bash
git clone https://github.com/yourusername/iTunesToMP3Converter.git
```

2. Navigate to the project directory:

```bash
cd iTunesToMP3Converter
```

3. Modify the `source_dir` and `target_dir` variables in `converter.py` to specify your iTunes music directory and the desired output directory.

4. Run the script:

```bash
python converter.py
```

## Script Overview

```python
import os
import shutil
import subprocess
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
import tkinter as tk
from tkinter import filedialog, messagebox

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

def process_directory(src_dir, dst_dir):
    for root, _, files in os.walk(src_dir):
        relative_path = os.path.relpath(root, src_dir)
        target_path = os.path.join(dst_dir, relative_path)
        ensure_dir_exists(target_path)

        for file in files:
            src_file = os.path.join(root, file)
            try:
                if file.lower().endswith('.mp3'):
                    dst_file = os.path.join(target_path, file)
                    shutil.copy2(src_file, dst_file)
                    copy_metadata(src_file, dst_file)
                elif file.lower().endswith('.m4a'):
                    dst_file = os.path.join(target_path, os.path.splitext(file)[0] + '.mp3')
                    convert_to_mp3(src_file, dst_file)
                    copy_mp4_metadata(src_file, dst_file)
            except Exception as e:
                print(f"Skipping file {src_file}: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [ffmpeg](https://ffmpeg.org/)
- [mutagen](https://github.com/quodlibet/mutagen)
```

### 修正内容
- `ffmpeg`のローカルインストール手順と、`ffmpeg`実行ファイルを使った変換方法に関する説明を追加しました。
- `ffmpeg-python`ではなく、`subprocess`モジュールを使用して`ffmpeg`コマンドを直接呼び出す方法に変更しました。

このREADME.mdファイルをリポジトリに追加し、スクリプトとともに使用することで、ローカルにインストールされた`ffmpeg`を利用する手順を提供できます。