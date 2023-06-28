from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication
import vlc
from vlc import EventType
import sys
from PyQt5.QtGui import QIcon
from vlc import Instance
class Player(QObject):
    stateChanged = pyqtSignal()
    positionChanged = pyqtSignal(float)
    mediaChanged = pyqtSignal()
    mediaEnd = pyqtSignal()

    def __init__(self, media_path):
        super().__init__()
        self.player = vlc.MediaPlayer(media_path)
        self.events = self.player.event_manager()
        self.events.event_attach(EventType.MediaPlayerPositionChanged, self.position_changed, self.player)
        self.events.event_attach(EventType.MediaPlayerEndReached, self.media_end, self.player)
        self.player.audio_set_volume(50)
        
        self.player.play()
    
    def set_media(self, media_path):
        #media = self.instance.media_new_path(media_path)
        #self.player.set_media(media)
        #elf.mediaChanged.emit()
        #TODO
        pass

    def position_changed(self, event, player):

        position = self.player.get_position()
        if self.old_position != position:
            self.positionChanged.emit(position * 100) #Percentage of the track that has been played
            self.old_position = position

    def media_end(self,event,player):

        if self.player.is_playing():
            self.player.stop()

        self.mediaEnd.emit()
        
        
        

'''     
app = QApplication(sys.argv)

player = Player('D:/Zene/test/The Caracal Project - Journée de merde. (Original Mix).wav')  # Replace with your audio file

# Connect to the signals
player.stateChanged.connect(lambda state: print('State changed:', state))
player.positionChanged.connect(lambda position: print('Position changed:', position))
player.durationChanged.connect(lambda duration: print('Duration changed:', duration))
player.mediaChanged.connect(lambda: print('Media changed'))

sys.exit(app.exec_())
'''