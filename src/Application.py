import sys
from PyQt5.QtWidgets import QApplication
from src.MainWindow import MainWindow
from util.Controller import Controller
from src.model.Database import MusicDatabase
from src.model.Player import Player


class Application(QApplication):

    def __init__(self, argv):
        QApplication.__init__(self, argv)
        self._setQss()

        self.controller = Controller()

        self.mediaPlayer = Player('')
        self.controller.setMedia(self.mediaPlayer)

        self.db = MusicDatabase(self.controller)
        self.controller.setDB(self.db)

        self.window = MainWindow(self.controller)
        self.controller.setWindow(self.window)
        
        self.window.show()
        sys.exit(self.exec_())
    
    def _setQss(self):
        try:
            with open('styles/dark.qss', 'r') as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print("QSS file not found.")