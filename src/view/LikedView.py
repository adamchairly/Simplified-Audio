# coding:utf-8
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QTableWidget, QHeaderView, QTableWidgetItem, QAbstractItemView, QFrame
from PyQt5.QtCore import pyqtSignal
from src.view.ImportView import ImportView

class LikedView(ImportView):

    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.table.hideColumn(5)
        self.table.hideColumn(6)
        self.table.hideColumn(7)