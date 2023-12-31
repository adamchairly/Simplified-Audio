import os
import io
from PyQt5.QtCore import pyqtSignal, QObject
import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4

class MediaData(QObject):

    errorOccured = pyqtSignal(str)

    def __init__(self, filepath):
        QObject.__init__(self)
        
        self.filepath = filepath
        self.title = 'Unknown'
        self.audio = None
        self.artist = 'Unknown'
        self.album = 'Unknown'
        self.type = 'Unknown'
        self.length = 0
        self.bitrate = 'Unknown'
        self.artwork = None
        self.has_cover = False
        self.get_audio_metadata()
        
    def get_audio_metadata(self):
        file_extension = os.path.splitext(self.filepath)[1].lower()

        try:
            if file_extension == '.mp3':
                self.get_mp3_metadata(self.filepath)
            elif file_extension == '.flac':
                self.get_flac_metadata(self.filepath)
            elif file_extension == '.wav':
                self.get_wav_metadata(self.filepath)
            elif file_extension == '.m4a':
                self.get_m4a_metadata(self.filepath)
        except Exception as e:
            self.errorOccured.emit(str(f'Error processing file: {self.filepath}, error: {e}'))
             
    def get_mp3_metadata(self, filepath):
        
        self.audio = MP3(filepath, ID3=ID3)
        self.title = self.audio.get("TIT2", "No Title")[0]
        self.artist = self.audio.get('TPE1', ['Unknown'])[0]
        self.album = self.audio.get('TALB', ['Unknown'])[0]
        self.type = 'mp3'
        self.length = self.convert_seconds(self.audio.info.length)
        self.bitrate = self.audio.info.bitrate / 1000

        self.has_cover = False
        if self.audio.tags is not None:
            for tag in self.audio.tags.values():
                if tag.FrameID == 'APIC':
                    self.has_cover = True
                    break

    def get_flac_metadata(self, filepath):

        self.audio = FLAC(filepath)
        self.title = self.audio.get("title", ["No Title"])[0]
        self.artist = self.audio.get('artist', ['Unknown'])[0]
        self.album = self.audio.get('album', ['Unknown'])[0]
        self.type = 'flac'
        self.length = self.convert_seconds(self.audio.info.length)
        self.bitrate = self.audio.info.bitrate / 1000

        self.has_cover = len(self.audio.pictures) > 0
        
    def get_wav_metadata(self, filepath):

        self.audio = mutagen.File(filepath)
        self.length = self.convert_seconds(self.audio.info.length)
        self.title = 'Unknown'
        self.artist = 'Unknown'
        self.album = 'Unknown'
        self.has_cover = False
        self.bitrate = self.audio.info.bitrate / 1000

    def get_m4a_metadata(self, filepath):

        self.audio = MP4(filepath)
        self.type = 'm4a'
        self.title = self.audio.get("\xa9nam", ["No Title"])[0]
        self.length = self.convert_seconds(self.audio.info.length)
        self.artist = self.audio.get('\xa9ART', ['Unknown'])[0]
        self.album = self.audio.get('\xa9alb', ['Unknown'])[0]
        self.has_cover = 'covr' in self.audio
        self.bitrate = self.audio.info.bitrate / 1000


    def get_album_cover(self):

        if self.has_cover and self.type == 'm4a':
            return self.audio['covr'][0]
        elif self.has_cover and self.type == 'mp3':
            return next((tag.data for tag in self.audio.tags.values() if tag.FrameID == 'APIC'), None)
        elif self.has_cover and self.type == 'flac':
            return next((picture.data for picture in self.audio.pictures if picture.type == 3), None)
    
    def convert_seconds(self, seconds):

        minutes, seconds = divmod(seconds, 60)
        return f"{int(minutes)}:{int(seconds):02d}"