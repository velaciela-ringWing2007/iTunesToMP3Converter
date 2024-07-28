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


process_directory(source_dir, target_dir)
