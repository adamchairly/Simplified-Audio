from PyQt5.QtCore import pyqtSignal
class Controller:
     

    def __init__(self):
        pass

    def _requestAudio(self):
        return self.media.audio
    
    def _isPlaying(self):
        return True if self.media.player.is_playing() else False
    
    def _stopPlaying(self):
        self.media.player.pause()
    
    def _startPlaying(self):
        self.media.player.play()
    
    def _setPosition(self, position):
        self.media.player.set_position(position)

    def _requestPlayerTime(self):
        return self.media.player.get_time()
    
    def _requestPlayerLength(self):
        return self.media.player.get_length()
    
    def _muteAudio(self, bool):
        self.media.player.audio_set_mute(bool)
    
    def _setVolume(self, volume):
        self.media.player.audio_set_volume(volume)
    
    def positionChange(self):
        self.window.playerView.positionChanged(self.media.player.get_time() / 1000, self.media.player.get_length() / 1000)

    def setWindow(self, window):
        self.window = window

    def setDB(self, db):
        self.db = db

    def mediaEnd(self):
        self.window.playerView.mediaEnd()
        pass
        #TODO db->next
    
    def setMedia(self, mediaPlayer):
        self.media = mediaPlayer
        self.media.positionChanged.connect(self.positionChange)
        self.media.mediaEnd.connect(self.mediaEnd)