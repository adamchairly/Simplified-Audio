from PyQt5.QtWidgets import QApplication,QHBoxLayout, QStackedWidget,QSizePolicy, QVBoxLayout
from PyQt5.QtGui import QIcon, QColor
from qframelesswindow import FramelessWindow

from src.view.PlayerView import PlayerView
from src.view.SettingsView import SettingsView
from src.view.ImportView import ImportView
from src.view.EqualizerView import EqualizerView
from util.CustomControls import NavigationPanel, CustomTitleBar
from util.CustomControls import Notification

class MainWindow(FramelessWindow):

    def __init__(self, controller):
        super(MainWindow, self).__init__()

        self.controller = controller
        self.initWindow()
        self.initGui()

    def initWindow(self):

        self.setTitleBar(CustomTitleBar(self))
        self.setWindowIcon(QIcon('resources/icons/icon.svg'))
        self.setMinimumSize(900,700)

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
        self.eqView = EqualizerView(self.controller)
        self.messagePanel = Notification('Welcome to Simplified Audio!')

        self.viewStack = QStackedWidget(self)
        self.viewStack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.viewStack.addWidget(self.playerView)
        self.viewStack.addWidget(self.importView)
        self.viewStack.addWidget(self.settingsView)
        self.viewStack.addWidget(self.eqView)

        
        self.upper_layout = QHBoxLayout()
        self.upper_layout.addWidget(self.navigationPanel)
        self.upper_layout.addWidget(self.viewStack)
        self.upper_layout.setSpacing(0)
    
        self.vertical_main = QVBoxLayout()
        self.vertical_main.setContentsMargins(10, self.titleBar.height(), 10, 10)
        self.vertical_main.addLayout(self.upper_layout)
        self.vertical_main.addWidget(self.messagePanel)
        self.vertical_main.setSpacing(10)
        self.setLayout(self.vertical_main)

        # Events
        self.navigationPanel.button1.clicked.connect(lambda: self.switchView(0))
        self.navigationPanel.button2.clicked.connect(lambda: self.switchView(2))
        self.navigationPanel.button4.clicked.connect(lambda: self.switchView(3))
        self.navigationPanel.button3.clicked.connect(lambda: self.switchView(1))
    
    def switchView(self, index):
        self.viewStack.setCurrentIndex(index)

