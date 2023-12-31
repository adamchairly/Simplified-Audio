import sys
from PyQt5.QtWidgets import QApplication
from src.MainWindow import MainWindow
from src.model.Database import MusicDatabase
from src.model.Player import Player
from src.util.Controller import Controller


class Application(QApplication):

    def __init__(self, argv):
        QApplication.__init__(self, argv)

        self.controller = Controller()

        self.mediaPlayer = Player("D:\Zene\garage-break\Bicep - Glue.mp3")
        self.controller.setMedia(self.mediaPlayer)

        self.db = MusicDatabase()
        self.controller.setDB(self.db)

        self.window = MainWindow(self.controller)
        self.controller.setWindow(self.window)
        
        self.window.show()
        sys.exit(self.exec_())

        
    
    