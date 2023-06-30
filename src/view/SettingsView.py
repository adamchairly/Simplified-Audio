from PyQt5.QtWidgets import QFrame, QLabel,QVBoxLayout, QSizePolicy, QFileDialog
from PyQt5.QtCore import pyqtSignal
from util.CustomControls import PathSelectPanel

class SettingsView(QFrame):

    # Fires when a new folder is added
    musicFoldersChanged = pyqtSignal(str)

    def __init__(self, controller, parent=None):
        super().__init__(parent= parent)

        self.controller = controller
        
        self.importPanel = PathSelectPanel()
        vLayout = QVBoxLayout()
        vLayout.setContentsMargins(10,0,10,0)
        vLayout.addWidget(self.importPanel)
        vLayout.setStretchFactor(self.importPanel, 0)
        vLayout.addStretch(1)
        self.setLayout(vLayout)

        # Upon folder change
        self.musicFoldersChanged.connect(self.importPanel.folderChanged)

        
