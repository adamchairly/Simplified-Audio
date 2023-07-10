from src.model.MediaData import MediaData
import os
    
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

        self.clear_layout(self.window.importView.scrollAreaLayout)

        for song in all_songs:
            id = song[0]
            title = song[1]
            artist = song[2]
            album_name = song[3]
            codec = song[4]
            file_path = song[5]

            data = MediaData(file_path)
            data = data.get_album_cover()
            self.window.importView.add_track(data, title, artist, album_name, codec, file_path)

        self.window.messagePanel.show_notification(f'Imported from: {path}')
    
    def _populate_liked(self):
        
        all_songs = self.db.get_all_tracks()

        for song in all_songs:
            id = song[0]
            title = song[1]
            artist = song[2]
            album_name = song[3]
            codec = song[4]
            file_path = song[5]
            liked = song[6]

            if liked:
                data = MediaData(file_path)
                data = data.get_album_cover()
                self.window.likedView.add_track(data, title, artist, album_name, codec, file_path)
    
    def _add_liked_track(self, file_path):

        song = self.db.get_song_by_path(file_path)

        if song:
            title = song[1]
            artist = song[2]
            album_name = song[3]
            codec = song[4]
            data = MediaData(file_path)
            data = data.get_album_cover()

            self.window.likedView.add_track(data, title, artist, album_name, codec, file_path)
    
    def _removed_liked_track(self, file_path):
        self.window.likedView.remove_track(self.media.audio.filepath)
        

    def _requestLoadTrack(self, path):
        self.media.set_media(path)
        self._setVolume(50)
        self.window.playerView.albumPanel.extractButton.setEnabled(True)
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
    
    def _applyEq(self, settings):
        self.media.apply_equalizer_settings(settings)

    def _track_liked(self, value):
        self.db.like_song(self.media.audio.filepath)

        if value:
            self._add_liked_track(self.media.audio.filepath)
        else: 
            print('Song should be removed after like')
            self._removed_liked_track(self.media.audio.filepath)


    def on_theme_changed(self, value):
        if value == 1: self.window._set_theme_light()
        else: self.window._set_theme_dark()

    def positionChange(self):
        self.window.playerView.positionChanged(self.media.player.get_time() / 1000, self.media.player.get_length() / 1000)

    def setWindow(self, window):
        self.window = window
        self._musicFolderChanged('music_player.db')
        self._populate_liked()

        self.window.settingsView.importPanel.folderChanged.connect(self._musicFolderChanged)
        self.window.settingsView.extractPanel.folderChanged.connect(self._log_message)
        self.window.settingsView.switch_panel.theme_changed.connect(self.on_theme_changed)

        self.window.playerView.albumPanel.track_liked.connect(self._track_liked)

    def setDB(self, db):
        self.db = db

    def mediaEnd(self):
        self.window.playerView.playerPanel.mediaEnd()
    
    def setMedia(self, mediaPlayer):
        self.media = mediaPlayer
        self.media.positionChanged.connect(self.positionChange)
        self.media.mediaEnd.connect(self.mediaEnd)
        
    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

            # Check if the item is a widget
            if item.widget() is not None:
                widget = item.widget()
                # Remove it from the layout
                layout.removeWidget(widget)
                # Delete the widget
                widget.deleteLater()
            elif item.layout() is not None:
                # The item is a layout, so recursively delete its children
                self.clear_layout(item.layout())
                # Then remove the layout from its parent layout
                layout.removeItem(item)
                # And finally delete the layout itself
                item.deleteLater()
   
