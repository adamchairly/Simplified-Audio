from PyQt5.QtWidgets import QFrame, QVBoxLayout
from ..util.CustomControls import PathSelectPanel, ExtractPanel, SwitchPanel

class SettingsView(QFrame):

    def __init__(self, controller, parent=None):
        super().__init__(parent= parent)

        self.controller = controller
        self.initUi()
        
    def initUi(self):
        self.importPanel = PathSelectPanel()
        self.switch_panel = SwitchPanel()

        vLayout = QVBoxLayout()
        vLayout.setContentsMargins(10,0,10,0)
        vLayout.addWidget(self.importPanel)
        vLayout.setStretchFactor(self.importPanel, 0)
        vLayout.addStretch(1)
        vLayout.addWidget(self.switch_panel)
        self.setLayout(vLayout)
    


        
