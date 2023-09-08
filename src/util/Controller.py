from src.model.MediaData import MediaData
import os
from PyQt5.QtMultimedia import QMediaPlayer
    
class Controller:
     
    def __init__(self):
        pass
        
    def _requestAudio(self):
        return self.media.audio
    
    def _isPlaying(self):
        return True if self.media.state() == QMediaPlayer.PlayingState else False
    
    def _stopPlaying(self):
        self.media.pause()
    
    def _startPlaying(self):
        self.media.play()
    
    def _setPosition(self, position):
        self.media.setPosition(int(position * self.media.duration() / 100))

    def _requestPlayerTime(self):
        return self.media.position()
    
    def _requestPlayerLength(self):
        return self.media.duration()
    
    def _muteAudio(self, bool):
        self.media.setMuted(bool)
    
    def _setVolume(self, volume):
        self.media.setVolume(volume)

    def _musicFolderChanged(self, path):

        self.db.import_folder(path)

        self.db.cursor.execute("SELECT * FROM Songs")
        all_songs = self.db.cursor.fetchall()

        self.clear_layout(self.window.importView.scrollAreaLayout)

        for song in all_songs:
            id = song[0]
            title = song[1]
            artist = song[2]
            album_name = song[3]
            codec = song[4]
            bitrate = song[5]
            length = song[6]
            file_path = song[7]


            data = MediaData(file_path)
            data = data.get_album_cover()
            self.window.importView.add_track(data, title, artist, album_name, codec, bitrate, length, file_path)

        self.window.messagePanel.show_notification(f'Imported from: {path}')
    
    def _populate_liked(self):
        
        all_songs = self.db.get_all_tracks()

        for song in all_songs:
            id = song[0]
            title = song[1]
            artist = song[2]
            album_name = song[3]
            codec = song[4]
            bitrate = song[5]
            length = song[6]
            file_path = song[7]
            liked = song[8]

            if liked:
                data = MediaData(file_path)
                data = data.get_album_cover()
                self.window.likedView.add_track(data, title, artist, album_name, codec, bitrate, length, file_path)
    
    def _add_liked_track(self, file_path):

        song = self.db.get_song_by_path(file_path)

        if song:
            title = song[1]
            artist = song[2]
            album_name = song[3]
            codec = song[4]
            data = MediaData(file_path)
            data = data.get_album_cover()
            bitrate = song[5]
            length = song[6]

            self.window.likedView.add_track(data, title, artist, album_name, codec, bitrate, length, file_path)
    
    def _removed_liked_track(self, file_path):
        self.window.likedView.remove_track(self.media.audio.filepath)
        

    def _requestLoadTrack(self, path):
        self.media.set_media(path)
        self._setVolume(50)
        self.window.playerView.albumPanel.likeButton.setEnabled(True)
        self.window.playerView.mediaChanged(self.media.audio, self.db.get_like_state(path))

        self.window.messagePanel.show_notification(f'Media set to {path}')
    
    def _get_next_song(self):
        self.media.set_media(self.db.get_next_song(self.media.audio.filepath))
        self.window.playerView.mediaChanged(self.media.audio, self.db.get_like_state(self.media.audio.filepath))
    
    def _get_previous_song(self):
        self.media.set_media(self.db.get_previous_song(self.media.audio.filepath))
        self.window.playerView.mediaChanged(self.media.audio, self.db.get_like_state(self.media.audio.filepath))

    def _log_message(self, message):
        self.window.messagePanel.show_notification(message, 3000)
    
    def _track_liked(self, value):
        self.db.like_song(self.media.audio.filepath)

        if value:
            self._add_liked_track(self.media.audio.filepath)
        else: 
            self._removed_liked_track(self.media.audio.filepath)


    def on_theme_changed(self, value):
        if value == 1: self.window._set_theme_light()
        else: self.window._set_theme_dark()

    def positionChange(self):
        self.window.playerView.positionChanged(self.media.position() / 1000 , self.media.duration() / 1000)

    def setWindow(self, window):
        self.window = window
        self._musicFolderChanged('music_player.db')
        self._populate_liked()

        self.window.settingsView.importPanel.folderChanged.connect(self._musicFolderChanged)
        self.window.settingsView.switch_panel.theme_changed.connect(self.on_theme_changed)

        self.window.playerView.albumPanel.track_liked.connect(self._track_liked)

    def setDB(self, db):
        self.db = db

    def mediaEnd(self):
        self.window.playerView.playerPanel.mediaEnd()
    
    def setMedia(self, mediaPlayer):
        self.media = mediaPlayer
        self.media.customPositionChanged.connect(self.positionChange)
        self.media.customMediaEnd.connect(self.mediaEnd)
        
    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

            if item.widget() is not None:
                widget = item.widget()
                layout.removeWidget(widget)
                widget.deleteLater()

            elif item.layout() is not None:
                self.clear_layout(item.layout())
                layout.removeItem(item)
                item.deleteLater()
   
