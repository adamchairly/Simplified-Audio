from PyQt5.QtWidgets import QFrame, QVBoxLayout
from PyQt5.QtGui import QIcon
from ..util.CustomControls import PlayerPanel,VolumePanel, AlbumPanel, MetaTablePanel, RoundEdgesWidget

class PlayerView(QFrame):

    def __init__(self, controller, parent=None):
        super().__init__(parent= parent)
        self.controller = controller
        self.initUi()

    def play(self):
        if self.controller._isPlaying():
            self.controller._stopPlaying()
            self.playerPanel.playButton.setIcon(QIcon('resources/icons/play.svg'))
        else:
            self.controller._startPlaying()
            self.playerPanel.playButton.setIcon(QIcon('resources/icons/pause.svg'))

    def left(self):
        self.controller._get_previous_song()

    def right(self):
        self.controller._get_next_song()

    def setPosition(self, position): #oke
        self.controller._setPosition(position)
        current_time = self.controller._requestPlayerTime() / 1000
        self.playerPanel.currentTime.setText(self.convert_seconds(int(current_time))) 
       
    def positionChanged(self, current_time, length):
        self.playerPanel.currentTime.setText(self.convert_seconds(int(current_time))) 
        if length != 0: 
            percentage_played = (current_time / length) * 100
            self.playerPanel.slider.setValue(int(percentage_played))
        if length == 0: self.playerPanel.slider.setValue(0)

    def convert_seconds(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return f"{int(minutes)}:{int(seconds):02d}"
        
    def mediaChanged(self, audio, value):
        self.playerPanel.update_ui(audio.length)
        self.albumPanel.update_ui(audio, value)
        self.metaPanel.update_ui(audio)
        self.volumePanel.update_ui()

    def mute(self):
        self.controller._muteAudio(True)
        self.volumePanel.volumeSlider.setSliderPosition(0)
        self.controller._log_message("Audio muted!")

    def unMute(self):
        self.controller._muteAudio(False)
        if self.volumePanel.volumeSlider.value() <= 90: self.volumePanel.volumeSlider.setValue(self.volumePanel.volumeSlider.value() + 10)
        self.controller._log_message("Audio unmuted!")
        
    def setVolume(self, volume):
        icon_path = 'resources/icons/volume2.svg' if volume > 50 else 'resources/icons/volume1.svg' if volume > 20 else 'resources/icons/volume0.svg'
        self.volumePanel.unmuteButton.setIcon(QIcon(icon_path))

        self.controller._muteAudio(False)
        self.controller._setVolume(volume)
        self.controller._log_message(f"Volume: {volume} %")

    def setController(self, controller):
        self.controller = controller
    
    def slider_pressed(self):
        self.playerPanel.slider.sliderMoved.disconnect(self.setPosition)
    
    def slider_released(self):
        self.setPosition(self.playerPanel.slider.value())
        self.playerPanel.slider.sliderMoved.connect(self.setPosition)

    def initUi(self):
        self.playerPanel = PlayerPanel()
        self.volumePanel = VolumePanel()
        self.albumPanel = AlbumPanel(self.controller)
        self.metaPanel = MetaTablePanel()

        vboxLayout = QVBoxLayout()
        vboxLayout.setContentsMargins(10,0,0,0)
        vboxLayout.addWidget(self.albumPanel)
        vboxLayout.addWidget(self.metaPanel)
        vboxLayout.addWidget(self.volumePanel)
        vboxLayout.addWidget(self.playerPanel)
        vboxLayout.setStretchFactor(self.albumPanel, 0)
        vboxLayout.setStretchFactor(self.playerPanel, 0)
        vboxLayout.setStretchFactor(self.volumePanel,0)
        self.setLayout(vboxLayout)

        self.playerPanel.playButton.clicked.connect(self.play)
        self.playerPanel.leftButton.clicked.connect(self.left)
        self.playerPanel.rightButton.clicked.connect(self.right)
        self.playerPanel.slider.sliderMoved.connect(self.setPosition)
        self.playerPanel.slider.sliderPressed.connect(self.slider_pressed)
        self.playerPanel.slider.sliderReleased.connect(self.slider_released)

        self.volumePanel.muteButton.clicked.connect(self.mute)
        self.volumePanel.unmuteButton.clicked.connect(self.unMute)
        self.volumePanel.volumeSlider.valueChanged.connect(self.setVolume)
        
    def switch_theme(self):
        for child in self.findChildren(RoundEdgesWidget):
            child.switch_theme()
    