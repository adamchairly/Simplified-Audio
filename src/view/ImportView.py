# coding:utf-8
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QTableWidget, QHeaderView, QTableWidgetItem, QAbstractItemView, QFrame
from PyQt5.QtCore import pyqtSignal
from util.CustomControls import RoundEdgesWidget

class ImportView(QFrame):

    trackSelected = pyqtSignal(str)

    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self._initUi()
        self._setQss()

    def add_track(self, id, title, artist, album, codec, path, liked):

        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 0, QTableWidgetItem(str(id)))
        self.table.setItem(row, 1, QTableWidgetItem(title))
        self.table.setItem(row, 2, QTableWidgetItem(artist))
        self.table.setItem(row, 3, QTableWidgetItem(album))
        self.table.setItem(row, 4, QTableWidgetItem(codec))
        self.table.setItem(row, 5, QTableWidgetItem(path))
        self.table.setItem(row, 6, QTableWidgetItem(liked))

    def cell_clicked(self, row, column):
        path_item = self.table.item(row, 5)

        if path_item is not None:
            path = path_item.text()
            self.trackSelected.emit(path)
            self.controller._requestLoadTrack(path)
    
    def _setQss(self):
        self.setStyleSheet("""
            QTableWidget {
                background-color: #717184;
                color: #E9E9EC;
                gridline-color: #2F2F37;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #717184;
                color: #E9E9EC;
                padding: 5px;
            }
            QHeaderView::corner {
                background-color: #717184;
            }
            """)
    
    def _initUi(self):
        self.vlayout = QVBoxLayout()
        self.qscroll = QScrollArea()
        self.qscroll.setWidgetResizable(True)

        self.scrollAreaWidget = RoundEdgesWidget()
        self.scrollAreaWidget.setStyleSheet("background-color: #717184")  # Set the background color
        self.scrollAreaLayout = QVBoxLayout(self.scrollAreaWidget)

        self.table = QTableWidget()
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setColumnCount(7)
        self.table.hideColumn(5)
        self.table.hideColumn(6)
        self.table.setHorizontalHeaderLabels(["ID", "Title","Artist", "Album", "Codec", "Path"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.table.cellClicked.connect(self.cell_clicked)

        self.scrollAreaLayout.addWidget(self.table)
        self.vlayout.addWidget(self.scrollAreaWidget)
        self.vlayout.setStretchFactor(self.scrollAreaWidget, 0)
        self.vlayout.setContentsMargins(10,0,10,0)
        self.setLayout(self.vlayout) 