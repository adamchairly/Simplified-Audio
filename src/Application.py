from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtNetwork import *
from src.MainWindow import MainWindow
from util.Controller import Controller
from src.model.Database import MusicDatabase
from src.model.Player import Player
import sys

class Application(QApplication):

    def __init__(self, argv):
        QApplication.__init__(self, argv)

        self.controller = Controller()
        self.mediaPlayer = Player('D:/Zene/cloducore/Sloucho, Rory Sweeney - Watching Us.mp3')
        self.controller.setMedia(self.mediaPlayer)

        self.window = MainWindow(self.controller)
        self.db = MusicDatabase(self.controller)

        self.controller.setWindow(self.window)
        self.controller.setDB(self.db)
        

        self.window.show()
        sys.exit(self.exec_())