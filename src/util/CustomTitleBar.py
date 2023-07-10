from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QPoint, Qt, QSize

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super(CustomTitleBar, self).__init__(parent)

        self.setMaximumHeight(40)
        self._parent = parent
        self.startMovePos = QPoint()

        
        self.iconLabel = QLabel(self)
        pixmap = QPixmap('resources/icons/icon.svg')
        self.iconLabel.setPixmap(pixmap)
        self.iconLabel.setStyleSheet('background-color: transparent;')
        self.iconLabel.setMaximumSize(50,50)

        self.titleLabel = QLabel("Simplified Audio")
        self.titleLabel.setObjectName('titleLabel')
        self.titleLabel.setStyleSheet('background-color: transparent;')

        self.left_layout = QHBoxLayout()
        self.left_layout.addWidget(self.iconLabel)
        self.left_layout.addWidget(self.titleLabel)
        self.left_layout.setSpacing(0)
        self.left_layout.setContentsMargins(0, 0, 0, 0)

        self.minimizeButton = QPushButton(self)
        self.minimizeButton.setObjectName("titlebutton")
        self.minimizeButton.setIcon(QIcon('resources/icons/minimize.svg'))
        self.minimizeButton.clicked.connect(self.showSmall)
        self.minimizeButton.setMaximumSize(50, 50)

        self.maximizeButton = QPushButton(self)
        self.maximizeButton.setObjectName("titlebutton")
        self.maximizeButton.setIcon(QIcon('resources/icons/maximize.svg'))
        self.maximizeButton.clicked.connect(self.showMaxRestore)
        self.maximizeButton.setMaximumSize(50, 50)

        self.closeButton = QPushButton(self)
        self.closeButton.setObjectName("titlebutton")
        self.closeButton.setIcon(QIcon('resources/icons/close.svg'))
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setMaximumSize(50, 50)


        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5,0,5,0)
        self.layout.setSpacing(15)
        self.layout.addLayout(self.left_layout)
        self.layout.addStretch(1)
        self.layout.addWidget(self.minimizeButton)
        self.layout.addWidget(self.maximizeButton)
        self.layout.addWidget(self.closeButton)
        

        self.setStyleSheet('styles/dark.qss')
        self.setContentsMargins(5,0,0,5)

    def showSmall(self):
        self._parent.showMinimized()

    def showMaxRestore(self):
        if self._parent.isMaximized():
            self._parent.showNormal()
        else:
            self._parent.showMaximized()

    def close(self):
        self._parent.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startMovePos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and not self.startMovePos.isNull():
            diff = event.globalPos() - self.startMovePos
            self.startMovePos = event.globalPos()
            self._parent.move(self._parent.pos() + diff)

class FramelessWindow(QMainWindow):
    def __init__(self):
        super(FramelessWindow, self).__init__()

        self._drag_pos = None
        self._resize_drag = False

    def mousePressEvent(self, event):
        self._drag_pos = event.globalPos()
        if self._border_hover(event.pos()):
            self._resize_drag = True
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._resize_drag and event.buttons() & Qt.LeftButton:
            diff = event.globalPos() - self._drag_pos
            self._drag_pos = event.globalPos()
            new_size = self.size() + QSize(diff.x(), diff.y())
            self.resize(new_size)
        else:
            self._resize_drag = False
            self._drag_pos = event.globalPos()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._resize_drag = False
        self._drag_pos = None
        super().mouseReleaseEvent(event)

    def _border_hover(self, pos):
        border_margin = 10
        return pos.x() < border_margin or self.width() - pos.x() < border_margin or pos.y() < border_margin or self.height() - pos.y() < border_margin