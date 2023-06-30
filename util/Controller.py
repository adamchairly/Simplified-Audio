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

    def _musicFolderChanged(self, path):

        self.db.import_folder(path)

        self.db.cursor.execute("SELECT * FROM Songs")
        all_songs = self.db.cursor.fetchall()

        self.window.importView.table.clearContents()
        self.window.importView.table.setRowCount(0)

        for song in all_songs:
            id = song[0]
            title = song[1]
            artist = song[2]
            album_name = song[3]
            codec = song[4]
            file_path = song[5]
            self.window.importView.add_track(id, title, artist, album_name, codec, file_path)

    def _requestLoadTrack(self, path):
        self.media.set_media(path)
        self.window.playerView.mediaChanged(self.media.audio)

        print(f'Media set to {path}')
    
    def _applyEq(self, settings):
        self.media.apply_equalizer_settings(settings)

    def positionChange(self):
        self.window.playerView.positionChanged(self.media.player.get_time() / 1000, self.media.player.get_length() / 1000)

    def setWindow(self, window):
        self.window = window
        self._musicFolderChanged('music_player.db')
        self.window.settingsView.importPanel.folderChanged.connect(self._musicFolderChanged)

    def setDB(self, db):
        self.db = db

    def mediaEnd(self):
        self.window.playerView.playerPanel.mediaEnd()
        pass
        #TODO db->next
    
    def setMedia(self, mediaPlayer):
        self.media = mediaPlayer
        self.media.positionChanged.connect(self.positionChange)
        self.media.mediaEnd.connect(self.mediaEnd)
    
   
