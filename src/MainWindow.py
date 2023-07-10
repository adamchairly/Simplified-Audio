from PyQt5.QtWidgets import QApplication,QHBoxLayout, QStackedWidget,QSizePolicy, QVBoxLayout,QMainWindow, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from src.view.PlayerView import PlayerView
from src.view.SettingsView import SettingsView
from src.view.ImportView import ImportView
from src.view.EqualizerView import EqualizerView
from src.view.LikedView import LikedView
from src.util.CustomControls import NavigationPanel
from src.util.CustomControls import Notification, Theme, RoundEdgesWidget
from src.util.CustomTitleBar import FramelessWindow, CustomTitleBar



class MainWindow(FramelessWindow):

    def __init__(self, controller):
        super(MainWindow, self).__init__()

        self.controller = controller
        self.theme = Theme.MAIN_BLACK

        self.initWindow()
        self.initGui()
        self._set_default_theme()

    def _set_theme_dark(self):

        self.switch_theme()
    
    def _set_theme_light(self):

        self.switch_theme()

    def _set_default_theme(self):
        try:
            with open('styles/dark.qss', 'r') as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print("QSS file not found.")

    def initWindow(self):

        self.title_bar = CustomTitleBar(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon('resources/icons/icon.svg'))

        self.setMinimumSize(900,700)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), self.theme.value) #bg
        self.setPalette(palette)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def paintEvent(self, event):
        super().paintEvent(event)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), self.theme.value)
        self.setPalette(palette)

    def initGui(self):

        self.navigationPanel = NavigationPanel()
        self.likedView = LikedView(self.controller)
        self.playerView =  PlayerView(self.controller)
        self.settingsView = SettingsView(self.controller)
        self.importView = ImportView(self.controller)
        self.eqView = EqualizerView(self.controller)
        self.messagePanel = Notification('Welcome!')

        self.viewStack = QStackedWidget(self)
        self.viewStack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.viewStack.addWidget(self.playerView)
        self.viewStack.addWidget(self.importView)
        self.viewStack.addWidget(self.settingsView)
        self.viewStack.addWidget(self.eqView)
        self.viewStack.addWidget(self.likedView)
        
        self.upper_layout = QHBoxLayout()
        self.upper_layout.addWidget(self.navigationPanel)
        self.upper_layout.addWidget(self.viewStack)
        self.upper_layout.setSpacing(0)
    
        self.vertical_main = QVBoxLayout()
        self.vertical_main.setContentsMargins(10, 0 ,10, 10)
        self.vertical_main.addLayout(self.upper_layout)
        self.vertical_main.addWidget(self.messagePanel)
        self.vertical_main.setSpacing(10)

        self.vertical_bar = QVBoxLayout()
        self.vertical_bar.setContentsMargins(0, 0, 0, 0)
        self.vertical_bar.setSpacing(0)
        self.vertical_bar.addWidget(self.title_bar)
        self.vertical_bar.addLayout(self.vertical_main)

        central_widget = QWidget()
        central_widget.setLayout(self.vertical_bar)
        central_widget.setContentsMargins(0,0,0,0)
        self.setCentralWidget(central_widget)

        self.navigationPanel.button1.clicked.connect(lambda: self.switchView(0))
        self.navigationPanel.button2.clicked.connect(lambda: self.switchView(2))
        self.navigationPanel.button4.clicked.connect(lambda: self.switchView(3))
        self.navigationPanel.button5.clicked.connect(lambda: self.switchView(4))
        self.navigationPanel.button3.clicked.connect(lambda: self.switchView(1))
    
    def switchView(self, index):
        self.viewStack.setCurrentIndex(index)

    def switch_theme(self):

        if self.theme == Theme.MAIN_BLACK:
            self.theme = Theme.MAIN_WHITE
            value = 'light'
        elif self.theme == Theme.MAIN_WHITE:
            self.theme = Theme.MAIN_BLACK
            value = 'dark'
        else:
            raise ValueError(f'Unsupported theme: {self.theme}')
        
        try:
            with open(f'styles/{value}.qss', 'r') as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print("QSS file not found.")

        widgets = [
            self.navigationPanel,
            self.playerView,
            self.settingsView,
            self.importView,
            self.eqView,
            self.likedView,
            self.messagePanel
        ]
        for widget in widgets:
            if isinstance(widget, RoundEdgesWidget):
                widget.switch_theme()  
            else: 
                for child in widget.findChildren(RoundEdgesWidget):
                    child.switch_theme()

        self.update()
    

    

