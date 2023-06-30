from PyQt5.QtCore import pyqtSignal
import sqlite3
import os
from src.model.MediaData import MediaData

class MusicDatabase:
    def __init__(self, controller, db_name='music_player.db'):
        
        self.controller = controller
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
                FilePath TEXT UNIQUE
            )
        """)
        self.conn.commit()
    
    def add_song(self, title, artist, album_name, codec, file_path):
        self.cursor.execute("""
            SELECT SongID FROM Songs WHERE FilePath = ? OR (Title = ? AND Artist = ? AND AlbumName = ?)
        """, (file_path, title, artist, album_name))
        existing_song = self.cursor.fetchone()
        if existing_song:
            print(f"Song at {file_path} is already in the database.")
        else:
            self.cursor.execute("""
                INSERT INTO Songs (Title, Artist, AlbumName, Codec, FilePath)
                VALUES (?, ?, ?, ?, ?)
            """, (title, artist, album_name, codec, file_path))
            self.conn.commit()



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
    
    def get_next_song(self, current_track_id):
        self.cursor.execute("""
            SELECT * FROM Songs WHERE SongID > ? ORDER BY SongID LIMIT 1
        """, (current_track_id,))
        return self.cursor.fetchone()

    def get_all_tracks(self, db_path):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT Artist, AlbumName, Codec, FilePath FROM Songs")
        rows = cur.fetchall()
        conn.close()
        return rows

    def close(self):
        self.conn.close()
