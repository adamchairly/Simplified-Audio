from PyQt5.QtWidgets import QApplication,QHBoxLayout, QStackedWidget,QSizePolicy
from PyQt5.QtGui import QIcon, QColor
from qframelesswindow import FramelessWindow

from src.view.PlayerView import PlayerView
from src.view.SettingsView import SettingsView
from src.view.ImportView import ImportView
from util.CustomControls import NavigationPanel, CustomTitleBar

class MainWindow(FramelessWindow):

    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        self.initWindow()
        self.initGui()

        # Folder imported -> database 
        #self.settingsView.importPanel.folderChanged.connect(self.db.import_folder)

    def initWindow(self):

        self.resize(900, 700)
        self.setTitleBar(CustomTitleBar(self))
        self.setWindowIcon(QIcon('icons/icon.svg'))
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor('#2F2F37')) #bg
        self.setPalette(palette)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def initGui(self):

        self.navigationPanel = NavigationPanel()
        self.playerView =  PlayerView(self.controller)
        self.settingsView = SettingsView(self.controller)
        self.importView = ImportView(self.controller)
        
        self.viewStack = QStackedWidget(self)
        self.viewStack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.viewStack.addWidget(self.playerView)
        self.viewStack.addWidget(self.importView)
        self.viewStack.addWidget(self.settingsView)


        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, self.titleBar.height(), 0, 10)
        self.main_layout.addWidget(self.navigationPanel)
        self.main_layout.addWidget(self.viewStack)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)

        # Events
        self.navigationPanel.button1.clicked.connect(lambda: self.switchView(0))
        self.navigationPanel.button2.clicked.connect(lambda: self.switchView(2))
        self.navigationPanel.button3.clicked.connect(lambda: self.switchView(1))
    
    def switchView(self, index):
        self.viewStack.setCurrentIndex(index)

