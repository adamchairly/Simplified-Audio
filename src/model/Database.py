from PyQt5.QtCore import pyqtSignal
import sqlite3
import os
from src.model.MediaData import MediaData

class MusicDatabase:
    def __init__(self, db_name='music_player.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Songs (
                SongID INTEGER PRIMARY KEY AUTOINCREMENT,
                Title TEXT,
                Artist TEXT,
                AlbumName TEXT,
                Codec TEXT,
                FilePath TEXT UNIQUE
            )
        """)
        self.conn.commit()
    
    def add_song(self, title, artist, album_name, codec, file_path):
        try:
            self.cursor.execute("""
                INSERT INTO Songs (Title, Artist, AlbumName, Codec, FilePath)
                VALUES (?, ?, ?, ?, ?)
            """, (title, artist, album_name, codec, file_path))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f"Song at {file_path} is already in the database.")

    def import_folder(self, folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith((".mp3", ".wav", ".flac")):
                    file_path = os.path.join(root, file)
                    media_data = MediaData(file_path)
                    title = media_data.title
                    artist = media_data.artist
                    album_name = media_data.album
                    codec = media_data.type
                    self.add_song(title, artist, album_name, codec, file_path)

    def get_song_by_path(self, file_path):
        self.cursor.execute("""
            SELECT * FROM Songs WHERE FilePath = ?
        """, (file_path,))
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()