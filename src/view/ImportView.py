# coding:utf-8
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QWidget, QFrame, QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from util.CustomControls import RoundEdgesWidget

class ImportView(QFrame):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.trackWidgets = []
        self._initUi()

    def add_track(self, data, title, artist, album, codec, path):
        self.trackWidget = TrackWidget(data, title, artist, album, codec, path)
        self.trackWidgets.append(self.trackWidget)
        self.trackWidget.trackSelected.connect(self.on_track_selected)
        self.scrollAreaLayout.addWidget(self.trackWidget)

    def on_track_selected(self, path):
        self.controller._requestLoadTrack(path)

    def _initUi(self):
        self.vlayout = QVBoxLayout()
        self.qscroll = QScrollArea()
        self.qscroll.setWidgetResizable(True)

        self.mainWidget = RoundEdgesWidget()
        self.scrollAreaWidget = QWidget()
        self.scrollAreaWidget.setObjectName("ScrollArea")
        self.scrollAreaLayout = QVBoxLayout(self.scrollAreaWidget)
        self.scrollAreaWidget.setLayout(self.scrollAreaLayout)

        self.qscroll.setWidget(self.scrollAreaWidget)
        self.qscroll.setFrameShape(QFrame.NoFrame)

        self.mainLayout = QVBoxLayout(self.mainWidget)
        self.mainLayout.addWidget(self.qscroll)
        self.mainLayout.setContentsMargins(20,20,20,20) 
        self.mainWidget.setLayout(self.mainLayout)

        self.vlayout.addWidget(self.mainWidget)
        self.setLayout(self.vlayout)

class TrackWidget(QWidget):

    trackSelected = pyqtSignal(str)

    def __init__(self, data, title, artist, album, codec, path):
        super().__init__()
        self.setObjectName('TrackWidget')

        self.coverArtLabel = QLabel(self)
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        if pixmap.isNull():
            fallback_path = 'resources/no_media.png'
            pixmap.load(fallback_path)

        pixmap = pixmap.scaled(75, 75, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.coverArtLabel.setPixmap(pixmap)

        self.titleLabel = QLabel(title[:20])
        self.artistLabel = QLabel(artist[:20])
        self.albumLabel = QLabel(album[:20])
        self.codecLabel = QLabel(codec[:5])
        self.path = path

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,5)
        self.layout.addWidget(self.coverArtLabel)
        self.layout.addWidget(self.titleLabel)
        self.layout.addWidget(self.artistLabel)
        self.layout.addWidget(self.albumLabel)
        self.layout.addWidget(self.codecLabel)

        self.setLayout(self.layout)

    def mousePressEvent(self, event):
        self.trackSelected.emit(self.path)
    

