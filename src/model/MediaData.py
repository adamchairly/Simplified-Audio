
import os
import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from PIL import Image
import io

# Define the folder
#folder = 'D:/Zene/test/album'

class MediaData:    
    def __init__(self, filepath):

        self.filepath = filepath
        self.audio = None
        self.artist = 'error'
        self.album = 'error'
        self.type = 'error'
        self.length = 0
        self.artwork = None
        self.has_cover = False
        self.get_audio_metadata()
        

    def get_audio_metadata(self):

        file_extension = os.path.splitext(self.filepath)[1]

        try:
            if file_extension == '.mp3':
                self.get_mp3_metadata(self.filepath)
            elif file_extension == '.flac':
                self.get_flac_metadata(self.filepath)
            elif file_extension == '.wav':
                self.get_wav_metadata(self.filepath)
            elif file_extension == '.m4a':
                self.get_m4a_metadata(self.filepath)
        except Exception as e:
            print(f"Error processing file: {self.filepath}, error: {e}")
             
    def get_mp3_metadata(self, filepath):
        
        print('belementem')
        self.audio = MP3(filepath, ID3=ID3)
        self.type = 'mp3'
        self.length = self.convert_seconds(self.audio.info.length)
        self.artist = self.audio['TPE1'].text[0]
        self.album = self.audio['TALB'].text[0]
        self.has_cover = True if self.audio.tags.getall('APIC') else False

    def get_flac_metadata(self, filepath):

        self.audio = FLAC(filepath)
        self.type = 'flac'
        self.length = self.convert_seconds(self.audio.info.length)
        self.artist = self.audio['artist']
        self.album = self.audio['album']
        self.has_cover = len(self.audio.pictures) > 0

    def get_wav_metadata(self, filepath):

        self.audio = mutagen.File(filepath)
        self.length = self.convert_seconds(self.audio.info.length)
        self.artist = None
        self.album = None
        self.has_cover = False

    def get_m4a_metadata(self, filepath):
                
        self.audio = MP4(filepath)
        self.type = 'm4a'
        self.length = self.convert_seconds(self.audio.info.length)
        self.artist = self.audio['\xa9ART']
        self.album = self.audio['\xa9alb']
        self.has_cover = 'covr' in self.audio

    def extract_album_cover(self, output_path):
    
        artwork = self.get_album_cover()
        filename = os.path.splitext(os.path.basename(self.audio.filename))[0]
        output_file_path = os.path.join(output_path, f'{filename}.jpg')

        if artwork is not None:
            try:
                with Image.open(io.BytesIO(artwork)) as img:
                    img.thumbnail((800, 800))
                    img.save(output_file_path, 'JPEG', optimize=True, quality=100)
                print(f'Saved album cover for {filename}')
            except Exception as e:
                print(f'Error processing album cover for {filename}: {str(e)}')
        else:
            print(f'No album cover found for {filename}')
    
    def get_album_cover(self):

        artwork = None 

        if self.has_cover and self.type =='m4a':
            artwork = self.audio['covr'][0]

        elif self.has_cover and self.type == 'mp3':
            for tag in self.audio.tags.values():
                if tag.FrameID == 'APIC':
                    artwork = tag.data
                    break

        elif self.has_cover and self.type == 'flac':
            for picture in self.audio.pictures:
                if picture.type == 3:
                    artwork = picture.data
                    break
                   
        if artwork is not None: return artwork

    def __eq__(self, other):
        if not isinstance(other, MediaData):
            return False
        if self.filepath == other.filepath:
            return True
        return object.__eq__(self, other)
    
    def convert_seconds(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return f"{int(minutes)}:{int(seconds):02d}"

# Go through all files in the folder
#for filename in os.listdir(folder):
    #filepath = os.path.join(folder, filename)
    #if not os.path.isfile(filepath):
       # continue
    #audio = Audio(filepath)
    #audio.get_audio_metadata()
    #audio.extract_album_cover(folder)
