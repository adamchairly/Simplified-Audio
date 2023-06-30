from PyQt5.QtWidgets import QPushButton, QWidget, QSlider, QVBoxLayout, QLabel, QHBoxLayout, QSizePolicy, QSpacerItem, QGraphicsDropShadowEffect, QGridLayout, QFrame, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainterPath, QPainter, QPixmap, QIcon, QColor, QRegion, QPalette
from qframelesswindow import StandardTitleBar
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtCore import Qt, QStandardPaths
from PyQt5.QtWidgets import QWidget, QLabel, QFrame

class CircularButton(QPushButton):
    def __init__(self, icon):
        super().__init__()
        self.tagged = False
        self.initUI()
        self.setIcon(QIcon(icon))
        
    def initUI(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: #717184;  
                border-radius: 25px; 
                min-width: 50px; 
                max-width: 50px; 
                min-height: 50px; 
                max-height: 50px;
            }
            QPushButton:hover {
                background-color: #B3717184;
            }
            QPushButton:pressed {
                background-color: #80717184;
            }
            QPushButton:disabled {
                background-color: #B3717184;
            }
            """)
        
class RoundEdgesWidget(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 20, 20)
        
        pixmap = QPixmap(self.size())
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)  # Enable anti-aliasing
        painter.setBrush(QColor('#545463'))  # Set the background color
        painter.drawPath(path)
        painter.end()

        painter = QPainter(self)
        painter.drawPixmap(self.rect(), pixmap)

    def resizeEvent(self, event):
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 20, 20)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)
        
class ModernSlider(QSlider):

    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.setOrientation(Qt.Horizontal)
        height = 5

        slider = f'''
        QSlider {{
            margin-top: {height+1}px;
            margin-bottom: {height+1}px;
        }}

        QSlider::groove:horizontal {{
            border: #2F2F37;
            height: {height}px;
            background: #E9E9EC; 
            margin: {height // 4}px 0;
        }}

        QSlider::handle:horizontal {{
            background: white;

            border: {height} solid #2F2F37;
            width: {height * 3};
            margin: {height * 2 * -1} 0;
            border-radius: {height * 2 + height // 2}px;
        }}
        QSlider::add-page:horizontal {{
            background: #2F2F37;
            height: {height}px;
            margin: {height // 4}px 0;
        }}
        QSlider::handle:horizontal:disabled {{
            background: #bbbbbb;
        }}
        '''
        self.setStyleSheet(slider)

class NavigationPanel(RoundEdgesWidget):
    def __init__(self):
        super().__init__()
        self.initUi()
    
    def initUi(self):

        # Buttons
        self.button1 = CircularButton('icons/import.svg')
        self.button2 = CircularButton('icons/settings.svg')

        # Layout 
        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.addWidget(self.button1)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.button2)

        # Widget
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor('#545463'))

        self.setPalette(palette)
        self.setLayout(self.vBoxLayout)

class CustomTitleBar(StandardTitleBar):

    def __init__(self, parent):
        super().__init__(parent)

        self.minBtn.setHoverBackgroundColor(QColor('#33717184'))
        self.minBtn.setHoverColor(QColor('White'))
        self.minBtn.setNormalColor(QColor('Grey'))

        self.closeBtn.setNormalColor(QColor('Grey'))
        self.closeBtn.setHoverColor(QColor('White'))

        self.maxBtn.setNormalColor(QColor('Grey'))
        self.maxBtn.setHoverColor(QColor('White'))
        self.maxBtn.setHoverBackgroundColor(QColor('#33717184'))
        self.setTitle('Simplified Audio')  

class PlayerPanel(RoundEdgesWidget):
    def __init__(self):
        super().__init__()
        self.initUi()
    
    def initUi(self):

        # Play/Pause Button
        self.playButton = CircularButton('icons/pause.svg')
        self.playButton.setEnabled(True)

        # Left Button
        self.leftButton = CircularButton('icons/backward.svg')
        self.leftButton.setEnabled(True)

        # Right Button
        self.rightButton = CircularButton('icons/forward.svg')
        self.rightButton.setEnabled(True)

        # Slider
        self.slider = ModernSlider()
        self.slider.setRange(0, 100)
        
        # Minute markers
        self.currentTime = QLabel('0:00')
        self.currentTime.setStyleSheet('color: #E9E9EC;')
        self.currentTime.setFixedSize(25,10)

        self.trackTime = QLabel()
        self.trackTime.setStyleSheet('color: #E9E9EC;')
        self.trackTime.setFixedSize(25,10)
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
        
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor('#545463'))
        self.setPalette(palette)
        self.setLayout(player_layout)

class VolumePanel(RoundEdgesWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor('#2F2F37'))
        self.setPalette(palette)
        self.setContentsMargins(0, 0, 0, 0)

        self.hLayout = QHBoxLayout()
        self.volumeSlider = ModernSlider()
        self.volumeSlider.setValue(50)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(100)

        self.muteButton = CircularButton('icons/volume-x.svg')
        self.unmuteButton = CircularButton('icons/volume1.svg')

        self.hLayout.setSpacing(20)
        self.hLayout.addWidget(self.unmuteButton)
        self.hLayout.addWidget(self.volumeSlider)
        self.hLayout.addWidget(self.muteButton)
        self.setLayout(self.hLayout)

class AlbumPanel(RoundEdgesWidget):
        def __init__(self, controller):
            super().__init__()

            self.controller = controller
            self.initUi(controller._requestAudio())

        def initUi(self, audio):

            hLayout = QHBoxLayout()  
            h2Layout = QHBoxLayout()
            vLayout = QVBoxLayout()

            self.albumCover = QLabel()
            #self.setAlbumCover(audio.get_album_cover(), 250)
            self.setDefaultCover(250)

            self.likeButton = CircularButton('icons/heart.svg')
            self.likeButton.clicked.connect(self.likeClick)

            self.extractButton = CircularButton('icons/save.svg')
            self.extractButton.clicked.connect(self.saveClick)

            # Drop Shadow for cover
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(20)
            shadow.setXOffset(5)
            shadow.setYOffset(5)
            shadow.setColor(Qt.black)
            shadow.setColor(QColor(0, 0, 0, 80)) 
            self.albumCover.setGraphicsEffect(shadow)

            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            
            self.spacer1 = QSpacerItem(20, 40, QSizePolicy.Expanding)
            self.spacer2 = QSpacerItem(20, 40, QSizePolicy.Expanding)

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
            
            self.setLayout(vLayout)

        def setAlbumCover(self, data, ratio):

            pixmap = QPixmap()
            pixmap.loadFromData(data)
            if pixmap.isNull():
                fallback_path = 'icons/no_media.png'
                pixmap.load(fallback_path)

            pixmap = pixmap.scaled(ratio, ratio, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.albumCover.setPixmap(pixmap)
            
        
        def setDefaultCover(self, ratio):
            pixmap = QPixmap()

            fallback_path = 'icons/no_media.png'
            pixmap.load(fallback_path)
            pixmap = pixmap.scaled(ratio, ratio, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.albumCover.setPixmap(pixmap)

        def likeClick(self):
            self.likeButton.tagged = not self.likeButton.tagged
            
            if self.likeButton.tagged: self.likeButton.setStyleSheet(
                """
                QPushButton {
                    background-color: #B34467;  
                    border-radius: 25px; 
                    min-width: 50px; 
                    max-width: 50px; 
                    min-height: 50px; 
                    max-height: 50px;
                }
                QPushButton:hover {
                    background-color: #B34467
                }
                QPushButton:pressed {
                    background-color: #80B34467;
                }
            """)
            else: self.likeButton.setStyleSheet(
                """
                QPushButton {
                    background-color: #717184;  
                    border-radius: 25px; 
                    min-width: 50px; 
                    max-width: 50px; 
                    min-height: 50px; 
                    max-height: 50px;
                }
                QPushButton:hover {
                    background-color: #B3717184;
                }
                QPushButton:pressed {
                    background-color: #80717184;
                }
                """)

        def saveClick(self):
            self.controller._requestAudio().extract_album_cover('extracted')

            
class MetaTablePanel(RoundEdgesWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUi(controller._requestAudio())

    def initUi(self, audio):
        # Create labels
        self.artist_name_label = QLabel(f"Artist Name: ")
        self.album_name_label = QLabel(f"Album Name: ")
        self.length_label = QLabel(f"Track Length: ")
        self.codec_label = QLabel(f"Track Codec: ")

        self.artist_data = QLabel("Artist Data")
        self.album_data = QLabel("Album Data")
        self.length_data = QLabel("Length Data")
        self.codec_data = QLabel("Codec Data")

        # Create separators
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setLineWidth(2)
        self.separator.setStyleSheet("color: black")

        # Create layout and add widgets
        layout = QGridLayout()
        layout.addWidget(self.artist_name_label, 0, 0)
        layout.addWidget(self.album_name_label, 0, 1)
        layout.addWidget(self.length_label, 0, 2)
        layout.addWidget(self.codec_label, 0, 3)

        layout.addWidget(self.separator, 1, 0, 1, 4)

        layout.addWidget(self.artist_data, 2, 0)
        layout.addWidget(self.album_data, 2, 1)
        layout.addWidget(self.length_data, 2, 2)
        layout.addWidget(self.codec_data, 2, 3)

        self.setLayout(layout)

        # Apply Styles
        self.setStyleSheet('''
            QLabel {
                background-color: transparent;
                color: #E9E9EC;
                padding: 5px;
            }
        ''')

        def updateInfo(self, audio):
            self.artist_name_label = QLabel(f"Artist Name: {audio.artist}")
            self.album_name_label = QLabel(f"Album Name: {audio.album}")
            self.length_label = QLabel(f"Track Length: {audio.length}")
            self.codec_label = QLabel(f"Track Codec: {audio.type}")

class PathSelectPanel(RoundEdgesWidget):

    folderChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.path = ''
        self.initUi()

    def initUi(self):

        main_layout = QVBoxLayout()

        icon = QIcon('icons/folder.svg')
        pixmap = icon.pixmap(20, 20) 
        self.icon_label = QLabel(self)
        self.icon_label.setPixmap(pixmap)

        self.text = QLabel('Import music folder', self)

        self.button = CircularButton(QIcon('icons/folder-plus.svg'))
        self.button.clicked.connect(self._onClick)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.pathLabel = QLabel('',self)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.pathLabel)
        vbox.addWidget(self.line)

        # Top layout
        top_layout = QHBoxLayout()
        top_layout.setSpacing(10)
        top_layout.addWidget(self.icon_label)
        top_layout.addWidget(self.text)
        top_layout.addStretch(1)
        top_layout.addWidget(self.button)

        # Bottom Layout
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch(1)
        bottom_layout.addLayout(vbox)
        bottom_layout.addStretch(1)

        main_layout.setSpacing(5)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.line)
        main_layout.addLayout(bottom_layout)
        self.setLayout(main_layout)

        self.setStyleSheet("QLabel { color: #CCFFFFFF; }")

    def _onClick(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder_path = QFileDialog.getExistingDirectory(self,"Select Folder", "", options=options)
        if folder_path:
            self.pathLabel.setText(f'Folder: {folder_path}')
            self.path = folder_path
            self.folderChanged.emit(folder_path)

