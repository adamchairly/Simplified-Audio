# coding:utf-8
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QWidget, QFrame
from ..util.CustomControls import TrackWidget, RoundEdgesWidget

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


    

