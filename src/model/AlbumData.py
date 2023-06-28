import os
from MediaData import MediaData
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from mutagen.mp3 import MP3

class AlbumData():
    def __init__(self):
        self.audio_list = []
    
    def import_folder(self, folder):

        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)
            if not os.path.isfile(filepath):
                continue
            track = MediaData(filepath)
            track.get_audio_metadata()
            self.audio_list.append(track)




