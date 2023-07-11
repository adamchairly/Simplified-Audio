from PyQt5.QtWidgets import (QPushButton, QWidget, QSlider, QVBoxLayout, QLabel, QHBoxLayout, 
                             QSizePolicy, QSpacerItem, QGraphicsDropShadowEffect, QGridLayout, QFrame, QFileDialog, QWidget)
from PyQt5.QtGui import QPainterPath, QPainter, QPixmap, QIcon, QColor, QRegion, QPalette
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPoint
from qframelesswindow import StandardTitleBar
from QSwitchControl import SwitchControl
from enum import Enum
import sys
import os

class Theme(Enum):
    BLACK = QColor('#545463')
    WHITE = QColor('#e1e1e1')
    MAIN_WHITE = QColor('#b0b0b0')
    MAIN_BLACK = QColor('#2F2F37')

class CircularButton(QPushButton):

    def __init__(self, icon):
        super().__init__()
        self.tagged = False
        self.setObjectName("CircularButton")

        self.setIcon(QIcon(icon))

class RoundEdgesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.theme = Theme.BLACK

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.theme.value)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)

    def resizeEvent(self, event):
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 20, 20)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)
    
    def switch_theme(self):
        if self.theme == Theme.BLACK:
            self.theme = Theme.WHITE
        elif self.theme == Theme.WHITE:
            self.theme = Theme.BLACK
        else:
            raise ValueError(f'Unsupported theme: {self.theme}')
        
        self.update()
        
class ModernSlider(QSlider):

    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.setOrientation(Qt.Horizontal)

class NavigationPanel(RoundEdgesWidget):
    def __init__(self):
        super().__init__()
        self.initUi()
    
    def initUi(self):

        self.button1 = CircularButton('resources/icons/player.svg')
        self.button3 = CircularButton('resources/icons/folder.svg')
        self.button4 = CircularButton('resources/icons/mixer.svg')
        self.button5 = CircularButton('resources/icons/heart.svg')
        self.button2 = CircularButton('resources/icons/settings.svg')

        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.addWidget(self.button1)
        self.vBoxLayout.addWidget(self.button3)
        self.vBoxLayout.addWidget(self.button5)
        self.vBoxLayout.addWidget(self.button4)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.button2)

        palette = self.palette()
        palette.setColor(QPalette.Background, QColor('#545463'))

        self.setPalette(palette)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        self.setLayout(self.vBoxLayout)
    
class PlayerPanel(RoundEdgesWidget):
    def __init__(self):
        super().__init__()
        self.initUi()
    
    def initUi(self):
        
        # Play/Pause Button
        self.playButton = CircularButton('resources/icons/player.svg')
        self.playButton.setEnabled(True)

        # Left Button
        self.leftButton = CircularButton('resources/icons/backward.svg')
        self.leftButton.setEnabled(True)

        # Right Button
        self.rightButton = CircularButton('resources/icons/forward.svg')
        self.rightButton.setEnabled(True)

        # Slider
        self.slider = ModernSlider()
        self.slider.setRange(0, 100)

        # Minute markers
        self.currentTime = QLabel()
        #self.currentTime.setFixedSize(30,10)
        self.currentTime.setText('0:00')

        self.trackTime = QLabel()
        #self.trackTime.setFixedSize(30,10)
        self.trackTime.setText('')

        # Layout
        player_layout = QHBoxLayout()
        player_layout.setSpacing(20)
        player_layout.addWidget(self.leftButton)
        player_layout.addWidget(self.playButton)
        player_layout.addWidget(self.rightButton)
        player_layout.addWidget(self.currentTime)
        player_layout.addWidget(self.slider)
        player_layout.addWidget(self.trackTime)
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setLayout(player_layout)
    
    def mediaEnd(self):
        self.currentTime.setText("0:00")
        self.slider.setDisabled(True)
        self.slider.setValue(0)
        self.leftButton.setDisabled(True)
        self.rightButton.setDisabled(True)
        self.playButton.setDisabled(True)
        self.playButton.setIcon(QIcon('resources/icons/play.svg'))

    def update_ui(self, length):
        self.currentTime.setText("0:00")
        self.trackTime.setText(str(length))
        self.slider.setDisabled(False)
        self.slider.setValue(0)
        self.leftButton.setDisabled(False)
        self.rightButton.setDisabled(False)
        self.playButton.setDisabled(False)
        self.playButton.setIcon(QIcon('resources/icons/pause.svg'))

class VolumePanel(RoundEdgesWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):

        self.setAutoFillBackground(False)
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor('#2F2F37'))
        self.setPalette(palette)
        self.setContentsMargins(0, 0, 0, 0)

        self.hLayout = QHBoxLayout()
        self.volumeSlider = ModernSlider()
        self.volumeSlider.setValue(50)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(100)

        self.muteButton = CircularButton('resources/icons/volume-x.svg')
        self.unmuteButton = CircularButton('resources/icons/volume1.svg')

        self.hLayout.setSpacing(20)
        self.hLayout.addWidget(self.unmuteButton)
        self.hLayout.addWidget(self.volumeSlider)
        self.hLayout.addWidget(self.muteButton)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setLayout(self.hLayout)

    def update_ui(self):
        self.volumeSlider.setValue(50)

class AlbumPanel(RoundEdgesWidget):
        
        track_liked = pyqtSignal(bool)

        def __init__(self, controller):
            super().__init__()

            self.controller = controller
            self.initUi(None)

        def initUi(self, audio):

            hLayout = QHBoxLayout()  
            h2Layout = QHBoxLayout()
            vLayout = QVBoxLayout()

            self.albumCover = QLabel()
            if audio != None: self.setAlbumCover(audio.get_album_cover(), 250)
            else: self.setDefaultCover(250)

            self.likeButton = CircularButton('resources/icons/heart.svg')
            self.likeButton.setEnabled(False)
            self.likeButton.clicked.connect(self.likeClick)
            self.likeButton.tagged = False

            self.extractButton = CircularButton('resources/icons/save.svg')
            self.extractButton.setEnabled(False)
            self.extractButton.clicked.connect(self.saveClick)

            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(20)
            shadow.setXOffset(5)
            shadow.setYOffset(5)
            shadow.setColor(Qt.black)
            shadow.setColor(QColor(0, 0, 0, 80)) 
            self.albumCover.setGraphicsEffect(shadow)

            self.spacer1 = QSpacerItem(20, 40, QSizePolicy.MinimumExpanding)
            self.spacer2 = QSpacerItem(20, 40, QSizePolicy.MinimumExpanding)

            hLayout.addItem(self.spacer1)
            hLayout.addWidget(self.albumCover)
            hLayout.addItem(self.spacer2)

            h2Layout.addItem(self.spacer1)
            h2Layout.addWidget(self.likeButton)
            h2Layout.addWidget(self.extractButton)
            h2Layout.addItem(self.spacer2)

            vLayout.setContentsMargins(0,0,0,20)
            vLayout.addLayout(hLayout)
            vLayout.addLayout(h2Layout)
            self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Preferred)
            self.setLayout(vLayout)

        def setAlbumCover(self, data, ratio):

            pixmap = QPixmap()
            pixmap.loadFromData(data)
            if pixmap.isNull():
                fallback_path = 'resources/no_media.png'
                pixmap.load(fallback_path)

            pixmap = pixmap.scaled(ratio, ratio, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.albumCover.setPixmap(pixmap)
            
        def setDefaultCover(self, ratio):

            pixmap = QPixmap()
            fallback_path = 'resources/no_media.png'
            pixmap.load(fallback_path)
            pixmap = pixmap.scaled(ratio, ratio, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.albumCover.setPixmap(pixmap)

        def likeClick(self):
            self.likeButton.tagged = not self.likeButton.tagged

            if self.likeButton.tagged:
                self.track_liked.emit(True)
                self.set_liked()
                self.controller._log_message('Track liked.')
            else: 
                self.track_liked.emit(False)
                self.set_default()
                self.controller._log_message('Track unliked.')
            
        def set_liked(self):
            self.likeButton.setStyleSheet(
                """
                QPushButton {
                    background-color: #BFe80c5c;  
                    border-radius: 25px; 
                    min-width: 50px; 
                    max-width: 50px; 
                    min-height: 50px; 
                    max-height: 50px;
                }
                QPushButton:hover {
                    background-color: #66e80c5c
                }
                QPushButton:pressed {
                    background-color: #80B34467;
                }
            """)
                
        def set_default(self):
            self.likeButton.setStyleSheet("""
                QPushButton {
                    background-color: #B3e06089;  
                    border-radius: 25px; 
                    min-width: 50px; 
                    max-width: 50px; 
                    min-height: 50px; 
                    max-height: 50px;
                }
                QPushButton:hover {
                    background-color: #66e06089;
                }
                QPushButton:pressed {
                    background-color: #38717184;
                }
                """)
            
        def saveClick(self):
            self.controller._requestAudio().extract_album_cover(self.controller.window.settingsView.extractPanel.path)
            self.controller._log_message(f'Album cover extracted to: {self.controller.window.settingsView.extractPanel.path}')
        
        def update_ui(self, audio, value):
            self.setAlbumCover(audio.get_album_cover(), 250)
            if value:
                self.set_liked()
                self.likeButton.tagged = True
            else: 
                self.set_default()
                self.likeButton.tagged = False
   
class MetaTablePanel(RoundEdgesWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):

        self.track_title_label = QLabel(f"Track Title: ")
        self.artist_name_label = QLabel(f"Artist Name: ")
        self.album_name_label = QLabel(f"Album Name: ")
        self.length_label = QLabel(f"Track Length: ")
        self.codec_label = QLabel(f"Track Codec: ")
        self.bitrate_label = QLabel(f'Track Bitrate:')

        self.artist_data = QLabel("Artist Data")
        self.album_data = QLabel("Album Data")
        self.length_data = QLabel("Length Data")
        self.codec_data = QLabel("Codec Data")

        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setLineWidth(2)

        layout = QGridLayout()
        layout.addWidget(self.track_title_label, 0, 0)
        layout.addWidget(self.artist_name_label, 0, 1)
        layout.addWidget(self.album_name_label, 0, 2)
        layout.addWidget(self.length_label, 0, 3)
        layout.addWidget(self.codec_label, 2, 0)
        layout.addWidget(self.bitrate_label, 2, 1)
        layout.addWidget(self.separator, 1, 0, 1, 4)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setLayout(layout)

    def update_ui(self, audio):
        self.track_title_label.setText(f"Track Title: {audio.title}")
        self.artist_name_label.setText(f"Artist Name: {audio.artist}")
        self.album_name_label.setText(f"Album Name: {audio.album}")
        self.length_label.setText(f"Track Length: {audio.length}")
        self.codec_label.setText(f"Track Codec: {audio.type}")
        self.bitrate_label.setText(f'Track Bitrate:{str(audio.bitrate)[:-2]} kbps')

class PathSelectPanel(RoundEdgesWidget):

    folderChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.path = 'resources\extracted'
        self.initUi()

    def initUi(self):
        
        icon = QIcon('resources/icons/folder.svg')
        pixmap = icon.pixmap(20, 20) 
        self.icon_label = QLabel(self)
        self.icon_label.setPixmap(pixmap)

        self.text = QLabel('Import music folder', self)
        self.text.setObjectName("PathSelectPanelLabel")

        self.button = CircularButton(QIcon('resources/icons/folder-plus.svg'))
        self.button.clicked.connect(self._onClick)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.pathLabel = QLabel('',self)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.pathLabel)
        vbox.addWidget(self.line)

        # Left Layout
        top_layout = QHBoxLayout()
        top_layout.setSpacing(10)
        top_layout.addWidget(self.icon_label)
        top_layout.addWidget(self.text)

        # Middle Layout
        bottom_layout = QHBoxLayout()
        horizontal_spacer = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        bottom_layout.addStretch(1)
        bottom_layout.addLayout(vbox)
        bottom_layout.addItem(horizontal_spacer)
        bottom_layout.addStretch(1)

        main_layout = QHBoxLayout()
        main_layout.setSpacing(5)
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)
        main_layout.addWidget(self.button)
        self.setLayout(main_layout)

    def _onClick(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder_path = QFileDialog.getExistingDirectory(self,"Select Folder", "", options=options)
        if folder_path:
            self.pathLabel.setText(f'Folder: {folder_path}')
            self.path = folder_path

            self.folderChanged.emit(self.path)
    
class ExtractPanel(PathSelectPanel):
    
    def __init__(self):
            super().__init__()
            self.text.setText('Album cover extract folder:')

    def _onClick(self):
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            folder_path = QFileDialog.getExistingDirectory(self,"Select Folder", "", options=options)
            if folder_path:
                self.pathLabel.setText(f'Folder: {folder_path}')
                self.path = folder_path

                self.folderChanged.emit(f'Extract folder changed to: {self.path}')

class EqualizerPanel(RoundEdgesWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.sliders = []

        layout = QVBoxLayout()
        frequencies = ["64 Hz", "125 Hz", "300 Hz", "800 Hz", "1.6 kHz", "3.2 kHz"]
        for i in range(6):

            label = QLabel(f"{frequencies[i]}")
            label.setObjectName("EqualizerLabel")

            slider = QSlider()
            slider.setObjectName("EqualizerSlider")
            slider.setOrientation(1)
            slider.setRange(-6, 6)
            slider.setValue(0)

            layout.addWidget(label)
            layout.addWidget(slider)

            self.sliders.append(slider)

        self.setLayout(layout)
        
    def get_equalizer_settings(self):
        settings = []
        for slider in self.sliders:
            value = slider.value()
            settings.append(value)
        return settings
    
class Notification(RoundEdgesWidget):

    def __init__(self, message):
        super().__init__()
        self.setObjectName("NotificationWidget")

        vlayout = QVBoxLayout()
        self.label = QLabel("")
        vlayout.addWidget(self.label)
        
        self.setLayout(vlayout)
        self.show_notification(message)

    def clear_message(self):
        self.label.setText('')

    def show_notification(self, message, duration=3000):
        self.label.setText(message) 
        QTimer.singleShot(duration, self.clear_message)

class SwitchPanel(RoundEdgesWidget):

    theme_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setObjectName("SwitchPanel")

        vLayout = QHBoxLayout()
        self.text = QLabel('Change theme:')
        self.mode_text = QLabel('Dark')
        self.mode_text2 = QLabel('Light')
        self.switchButton = SwitchControl(active_color= "#545463")
        vLayout.addWidget(self.text)
        vLayout.addStretch(1)
        vLayout.addWidget(self.mode_text)
        vLayout.addWidget(self.switchButton)
        vLayout.addWidget(self.mode_text2)
        self.setLayout(vLayout)

        self.switchButton.toggled.connect(self.on_toggle)

    def on_toggle(self, toggled):
        if toggled: 
            self.theme_changed.emit(1)
        else: 
            self.theme_changed.emit(0)
    
class TrackWidget(QWidget):

    trackSelected = pyqtSignal(str)

    def __init__(self, data, title, artist, album, codec, bitrate, length, path):
        super().__init__()
        self.setObjectName('TrackWidget')

        self.coverArtLabel = QLabel(self)
        pixmap = QPixmap()
        if data != None:
            pixmap.loadFromData(data)
        if pixmap.isNull():
            fallback_path = 'resources/no_media.png'
            pixmap.load(fallback_path)

        pixmap = pixmap.scaled(75, 75, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.coverArtLabel.setPixmap(pixmap)

        self.titleLabel = QLabel(title[:20])
        self.artistLabel = QLabel(artist[:20])
        self.albumLabel = QLabel(album[:20])
        self.codecLabel = QLabel(codec[:20])
        self.bitrateLabel = QLabel(bitrate[:20][:-2] + 'kbps')
        self.lengthLabel = QLabel(length[:20])
        self.path = path

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,5)
        self.layout.addWidget(self.coverArtLabel)
        self.layout.addWidget(self.titleLabel)
        self.layout.addWidget(self.artistLabel)
        self.layout.addWidget(self.albumLabel)
        self.layout.addWidget(self.codecLabel)
        self.layout.addWidget(self.bitrateLabel)
        self.layout.addWidget(self.lengthLabel)

        self.setLayout(self.layout)

        for label in [self.titleLabel, self.artistLabel, self.albumLabel,
                      self.codecLabel, self.bitrateLabel, self.lengthLabel]:
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
    def mousePressEvent(self, event):
        self.trackSelected.emit(self.path)
