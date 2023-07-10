from PyQt5.QtCore import pyqtSignal
import sqlite3
import os
from src.model.MediaData import MediaData

class MusicDatabase:
    def __init__(self, db_name='music_player.db'):
        
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Songs (
                SongID INTEGER PRIMARY KEY AUTOINCREMENT,
                Title TEXT,
                Artist TEXT,
                AlbumName TEXT,
                Codec TEXT,
                FilePath TEXT UNIQUE,
                Liked INTEGER DEFAULT 0
            )
        """)
        self.conn.commit()
    
    def add_song(self, title, artist, album_name, codec, file_path, liked):
        self.cursor.execute("""
            SELECT SongID FROM Songs WHERE FilePath = ? OR (Title = ? AND Artist = ? AND AlbumName = ?)
        """, (file_path, title, artist, album_name))
        existing_song = self.cursor.fetchone()
        if existing_song:
            print(f"Song at {file_path} is already in the database.")
        else:
            self.cursor.execute("""
                INSERT INTO Songs (Title, Artist, AlbumName, Codec, FilePath, Liked)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (title, artist, album_name, codec, file_path, liked))
            self.conn.commit()

    def import_folder(self, folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith((".mp3", ".wav", ".flac", ".m4a")):
                    file_path = os.path.join(root, file)
                    file_path = os.path.normpath(file_path)
                    media_data = MediaData(file_path)
                    title = media_data.title
                    artist = media_data.artist
                    album_name = media_data.album
                    codec = media_data.type
                    self.add_song(title, artist, album_name, codec, file_path, liked = 0)

    def get_song_by_path(self, file_path):
        self.cursor.execute("""
            SELECT * FROM Songs WHERE FilePath = ?
        """, (file_path,))
        return self.cursor.fetchone()
    
    def like_song(self, file_path):

        self.cursor.execute("""
            SELECT Liked FROM Songs WHERE FilePath = ?
        """, (file_path,))
        result = self.cursor.fetchone()
        if result is not None:
            current_liked_status = result[0]
            new_liked_status = 0 if current_liked_status == 1 else 1
            self.cursor.execute("""
                UPDATE Songs SET Liked = ? WHERE FilePath = ?
            """, (new_liked_status, file_path))
            self.conn.commit()
        else:
            print(f"No song found at {file_path}.")
    
    def get_like_state(self, file_path):
        self.cursor.execute("""
            SELECT Liked FROM Songs WHERE FilePath = ?
        """, (file_path,))
        
        result = self.cursor.fetchone()
        if result is None:
            return False
        else:
            return result[0] == 1

    def get_next_song(self, current_track_path):
        self.cursor.execute("""
            SELECT SongID FROM Songs WHERE FilePath = ?
        """, (current_track_path,))
        result = self.cursor.fetchone()
        if result is not None:
            current_track_id = result[0]
        else:
            return None

        self.cursor.execute("""
            SELECT FilePath FROM Songs WHERE SongID > ? ORDER BY SongID LIMIT 1
        """, (current_track_id,))
        result = self.cursor.fetchone()
        if result is not None:
            return result[0]
        else:
            return None
        
    def get_previous_song(self, current_track_path):
        self.cursor.execute("""
            SELECT SongID FROM Songs WHERE FilePath = ?
        """, (current_track_path,))
        result = self.cursor.fetchone()
        if result is not None:
            current_track_id = result[0]
        else:
            return None

        self.cursor.execute("""
            SELECT FilePath FROM Songs WHERE SongID < ? ORDER BY SongID DESC LIMIT 1
        """, (current_track_id,))
        result = self.cursor.fetchone()
        if result is not None:
            return result[0]
        else:
            return None 
        
    def get_like_state(self, path):
        self.cursor.execute("""
            SELECT Liked FROM Songs WHERE FilePath = ?
        """, (path,))

        result = self.cursor.fetchone()
        return result is not None and result[0] == 1
    
    def get_all_tracks(self):
        self.cursor.execute("SELECT * FROM Songs")
        rows = self.cursor.fetchall()
        return rows

    def close(self):
        self.conn.close()
