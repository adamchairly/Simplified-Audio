from PyQt5.QtCore import QObject, pyqtSignal, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from src.model.MediaData import MediaData

class Player(QMediaPlayer):
    
    customPositionChanged = pyqtSignal()
    customMediaChanged = pyqtSignal()
    customMediaEnd = pyqtSignal()

    def __init__(self, media_path):
        super().__init__()

        self.setMedia(QMediaContent(QUrl.fromLocalFile(media_path)))
        self.audio = MediaData(media_path)
        self.setVolume(50)

        # Connect built-in positionChanged signal to custom slot
        self.positionChanged.connect(self.position_changed)
        self.mediaStatusChanged.connect(self.media_status_changed)
        self.play()

    def set_media(self, media_path):
        self.stop()
        self.setMedia(QMediaContent(QUrl.fromLocalFile(media_path)))
        self.audio = MediaData(media_path)
        self.play()
        
        self.customMediaChanged.emit()

    def position_changed(self, position):
        self.customPositionChanged.emit()

    def media_status_changed(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.customMediaEnd.emit()
