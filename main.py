import sys
from PyQt5.QtWidgets import QApplication,QHBoxLayout, QStackedWidget,QSizePolicy
from PyQt5.QtGui import QIcon, QColor
from qframelesswindow import FramelessWindow
from qframelesswindow import FramelessWindow

from src.view.PlayerView import PlayerView
from src.view.SettingsView import SettingsView
from util.CustomControls import NavigationPanel, CustomTitleBar

class MainWindow(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))
        self.initWindow()

    def initWindow(self):

        self.resize(900, 700)
 
        self.setWindowIcon(QIcon('icons/icon.svg'))
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor('#2F2F37')) #bg
        self.setPalette(palette)

        self.navigationPanel = NavigationPanel()

        self.viewStack = QStackedWidget(self)
        self.viewStack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.viewStack.addWidget(PlayerView(self))
        self.viewStack.addWidget(SettingsView('ASD',self))

        
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, self.titleBar.height() + 10, 0, 10)
        self.main_layout.addWidget(self.navigationPanel)
        self.main_layout.addWidget(self.viewStack)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)

        #events
        self.navigationPanel.button1.clicked.connect(lambda: self.switchView(0))
        self.navigationPanel.button2.clicked.connect(lambda: self.switchView(1))

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
    
    def switchView(self, index):
        self.viewStack.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
