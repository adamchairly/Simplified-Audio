from PyQt5.QtCore import QObject, pyqtSignal
import vlc
from vlc import EventType
from src.model.MediaData import MediaData

class Player(QObject):
    
    positionChanged = pyqtSignal()
    mediaChanged = pyqtSignal()
    mediaEnd = pyqtSignal()

    def __init__(self, media_path):
        super().__init__()

        self.player = vlc.MediaPlayer(media_path)
        self.audio = MediaData(media_path)
        self.player.audio_set_volume(50)

        self.events = self.player.event_manager()
        self.events.event_attach(EventType.MediaPlayerPositionChanged, self.position_changed, self.player)
        self.events.event_attach(EventType.MediaPlayerEndReached, self.media_end, self.player)
        
        
        self.player.play()

    def set_media(self, media_path):
        self.player.stop()
        self.player.set_mrl(media_path)
        self.audio = MediaData(media_path)
        self.player.play()
        
        self.mediaChanged.emit()

    def position_changed(self, event, player):

        self.positionChanged.emit() 

    def media_end(self, event, player):

        if self.player.is_playing():
            self.player.stop()

        self.mediaEnd.emit()
    
    def apply_equalizer_settings(self, settings):
        equalizer = vlc.AudioEqualizer()

        for i, gain in enumerate(settings):
            equalizer.set_amp_at_index(gain, i)

        self.player.set_equalizer(equalizer)