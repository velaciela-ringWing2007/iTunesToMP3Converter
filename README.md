### プロジェクト名
`iTunesToMP3Converter`

### README.md テンプレート

```markdown
# iTunesToMP3Converter

iTunesToMP3Converter is a Python script that converts iTunes music directories to MP3 format while preserving metadata such as album art, album name, track name, track number, artist name, and composer name. It maintains the directory structure and copies files to a specified output directory.

## Features

- Convert various audio formats to MP3
- Preserve metadata including album art, album name, track name, track number, artist name, and composer name
- Maintain the original directory structure
- Specify output directory for converted files

## Requirements

- Python 3.6+
- ffmpeg
- ffmpeg-python
- mutagen

## Installation

1. Install `ffmpeg`. Follow the installation instructions for your operating system [here](https://ffmpeg.org/download.html).
2. Install the required Python packages:

```bash
pip install ffmpeg-python mutagen
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
import ffmpeg
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

source_dir = "path/to/itunes"
target_dir = "path/to/output"

def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def copy_metadata(src, dst):
    audio = MP3(src, ID3=EasyID3)
    audio.save(dst, v2_version=3)

def convert_to_mp3(src_file, dst_file, bitrate='192k'):
    src_audio = MP3(src_file, ID3=EasyID3)
    src_metadata = {key: src_audio.get(key, [None])[0] for key in src_audio.keys()]

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
                bitrate = MP3(src_file).info.bitrate if hasattr(MP3(src_file).info, 'bitrate') else '192k'
                convert_to_mp3(src_file, dst_file, bitrate=str(bitrate) + 'k')

process_directory(source_dir, target_dir)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [ffmpeg](https://ffmpeg.org/)
- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python)
- [mutagen](https://github.com/quodlibet/mutagen)
```

### 次のステップ
1. GitHubに新しいリポジトリを作成し、プロジェクト名を `iTunesToMP3Converter` にします。
2. 上記のREADME.mdファイルをリポジトリのルートディレクトリに追加します。
3. `converter.py` という名前でPythonスクリプトをリポジトリに追加します。
4. 必要に応じて、`.gitignore` ファイルを作成してPython環境ファイルなどの不要なファイルを無視します。

GitHubリポジトリのセットアップが必要な場合はお知らせください。さらに手順を詳しく説明します。
