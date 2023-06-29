# coding:utf-8
from PyQt5.QtWidgets import QFrame, QVBoxLayout
from PyQt5.QtGui import QIcon
from src.model import MediaData, Player
from util.CustomControls import PlayerPanel,VolumePanel, AlbumPanel, MetaTablePanel
import pythoncom

class PlayerView(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent= parent)

        self.audio = MediaData.MediaData('D:/Zene/test/Airdrop - tom.mp3')
        #print(self.audio.artist)
        #print(self.audio.length)
        #print(self.audio.type)

        self.mediaPlayer = Player.Player('D:/Zene/test/Airdrop - tom.mp3')
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.mediaChanged.connect(self.mediaChanged)
        self.mediaPlayer.mediaEnd.connect(self.mediaEnd)

        self.playerPanel = PlayerPanel()
        self.volumePanel = VolumePanel()
        self.albumPanel = AlbumPanel(self.audio)
        self.metaPanel = MetaTablePanel(self.audio)

        # Vertical Layout
        vboxLayout = QVBoxLayout()
        vboxLayout.setContentsMargins(10,0,10,0)
        vboxLayout.addWidget(self.albumPanel)
        vboxLayout.addWidget(self.metaPanel)
        vboxLayout.addWidget(self.volumePanel)
        vboxLayout.addWidget(self.playerPanel)
        vboxLayout.setStretchFactor(self.albumPanel, 0)
        vboxLayout.setStretchFactor(self.playerPanel, 0)
        vboxLayout.setStretchFactor(self.volumePanel,0)
        self.setLayout(vboxLayout)

        # Connecting button actions
        self.playerPanel.playButton.clicked.connect(self.play)
        self.playerPanel.leftButton.clicked.connect(self.left)
        self.playerPanel.rightButton.clicked.connect(self.right)
        self.playerPanel.slider.sliderMoved.connect(self.setPosition)

        self.volumePanel.muteButton.clicked.connect(self.mute)
        self.volumePanel.unmuteButton.clicked.connect(self.unMute)
        self.volumePanel.volumeSlider.valueChanged.connect(self.setVolume)

    def play(self):
        if self.mediaPlayer.player.is_playing():
            self.mediaPlayer.player.pause()
            self.playerPanel.playButton.setIcon(QIcon('icons/play.svg'))
        else:
            self.mediaPlayer.player.play()
            self.playerPanel.playButton.setIcon(QIcon('icons/pause.svg'))

    def left(self):
        self.mediaPlayer.player.stop()
        #TODO

    def right(self):
        self.mediaPlayer.player.stop()
        #TODO

    def setPosition(self, position):
       # Update the slider
        self.mediaPlayer.player.set_position(float(position / 100)) # VLC uses a 0.0-1.0 range

        # Update the time
        current_time = self.mediaPlayer.player.get_time() / 1000   # Current time in seconds
        length = self.mediaPlayer.player.get_length() / 1000    # Length in seconds
        self.playerPanel.currentTime.setText(self.convert_seconds(int(current_time))) 
       
    def positionChanged(self, position):
        # Current time
        current_time = self.mediaPlayer.player.get_time() / 1000   # Current time in seconds
        length = self.mediaPlayer.player.get_length() / 1000    # Length in seconds
        self.playerPanel.currentTime.setText(self.convert_seconds(int(current_time))) 

        # Update time slider 
        percentage_played = (current_time / length) * 100
        self.playerPanel.slider.setValue(int(percentage_played))


    def convert_seconds(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return f"{int(minutes)}:{int(seconds):02d}"
        
    def mediaChanged(self):
        #TODO
        self.mediaPlayer.player.set_position(0.0)
        self.playerPanel.trackTime.setText(self.audio.length)
        self.playerPanel.playButton.setIcon(QIcon('icons/pause.svg'))
        self.mediaPlayer.player.audio_set_volume(50)
        
        self.mediaPlayer.player.play()
        
    def mute(self):
        self.mediaPlayer.player.audio_set_mute(True)
        self.volumePanel.volumeSlider.setSliderPosition(0)

    def unMute(self):
        self.mediaPlayer.player.audio_set_mute(False)
        if self.volumePanel.volumeSlider.value() <= 90: self.volumePanel.volumeSlider.setValue(self.volumePanel.volumeSlider.value() + 10)
        
    def setVolume(self, volume):
        icon_path = 'icons/volume2.svg' if volume > 50 else 'icons/volume1.svg' if volume > 20 else 'icons/volume0.svg'
        self.volumePanel.unmuteButton.setIcon(QIcon(icon_path))
        self.mediaPlayer.player.audio_set_mute(False)
        self.mediaPlayer.player.audio_set_volume(volume) # volume is in the range 0-100
        print(volume)

    def mediaEnd(self):
        self.playerPanel.currentTime.setText("0:00")
        self.playerPanel.trackTime.setText("0:00")
        self.playerPanel.slider.setDisabled(True)
        self.playerPanel.slider.setValue(0)
        self.playerPanel.leftButton.setDisabled(True)
        self.playerPanel.rightButton.setDisabled(True)
        self.playerPanel.playButton.setDisabled(True)

   
        
