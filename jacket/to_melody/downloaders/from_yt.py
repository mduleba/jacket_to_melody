from functools import cached_property
import os
import pytube as pt
from dataclasses import dataclass, field

from ..models import Song
from django.core.files.base import ContentFile, File
import shutil


@dataclass
class YTSong:
    url: str

    file_path: str = field(default="")
    converted: bool = field(default=False)
    moved_to_media: bool = field(default=False)

    @property
    def file_name(self):
        directory, file_name = self.file_path.rsplit("\\", 1)
        return file_name

    @property
    def title(self):
        return self.youtube.title

    @property
    def author(self):
        return self.youtube.author

    @cached_property
    def youtube(self):
        return pt.YouTube(self.url)

    def wait_until_file(self):
        while True:
            if self.file_path:
                break

    def download(self):
        t = self.youtube.streams.filter(only_audio=True)
        self.file_path = t[0].download(output_path="tmp\\")
        self.wait_until_file()
        self.converted = False

    def convert_to_mp3(self):
        assert self.file_path, 'download first'
        assert not self.converted, 'already converted'

        new_path = self.file_path[:-4] + '.mp3'
        shutil.move(self.file_path, new_path)
        self.wait_until_file()
        self.file_path = new_path
        self.converted = True

    def delete(self):
        assert self.file_path, 'nothing to delete'
        os.remove(self.file_path)
        self.file_path = ""

    def copy_to_media(self, media_path='C:\\Users\\duleb\\PycharmProjects\\jacket_to_melody\\jacket\\media\\songs\\'):
        src_path = self.file_path
        dst_path = media_path + self.file_name
        shutil.move(src_path, dst_path)
        self.file_path = dst_path
        self.moved_to_media = True

    def update_song(self, song: Song):
        assert self.moved_to_media
        assert self.converted
        song.title = self.title
        song.author = self.author
        song.audio_file = self.file_path
        song.save()

        return song


if __name__ == '__main__':
    billie_jean = YTSong("https://www.youtube.com/watch?v=Zi_XLOBDo_Y")
    billie_jean.download()
    billie_jean.convert_to_mp3()
    billie_jean.copy_to_media()