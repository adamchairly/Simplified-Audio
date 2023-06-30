# coding:utf-8
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QTableWidget, QHeaderView, QTableWidgetItem, QAbstractItemView, QFrame
from PyQt5.QtCore import pyqtSignal
from util.CustomControls import RoundEdgesWidget

class LikedView(QFrame):

    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self._initUi()
        self._setQss()

    def _initUi(self):
        pass
    def _setQss(self):
        pass