# coding:utf-8
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QTableWidget, QHeaderView, QTableWidgetItem, QAbstractItemView, QFrame, QStyle
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon, QPalette, QColor
from util.CustomControls import EqualizerPanel, CircularButton

from PyQt5.QtChart import QChart, QChartView, QLineSeries, QBarCategoryAxis
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter


from PyQt5.QtChart import QChart, QChartView, QLineSeries, QBarCategoryAxis
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

from PyQt5.QtChart import QChart, QChartView, QLineSeries, QBarCategoryAxis, QValueAxis
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

class EqualizerView(QFrame):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self._initUi()

    def _initUi(self):
        self.eqPanel = EqualizerPanel()
        vLayout = QVBoxLayout()
        vLayout.setContentsMargins(10, 0, 10, 0)

        # Create the chart for spectrum visualization
        self.chart = QChart()
        self.chart.legend().hide()
        self.chart.setBackgroundVisible(False)

        # Add a line series for the spectrum
        self.series = QLineSeries()
        self.chart.addSeries(self.series)

        # Create a category axis for the frequency labels
        self.axisX = QBarCategoryAxis()
        self.chart.addAxis(self.axisX, Qt.AlignBottom)
        self.series.attachAxis(self.axisX)

        # Create a value axis for the y-axis
        self.axisY = QValueAxis()
        self.chart.addAxis(self.axisY, Qt.AlignLeft)
        self.series.attachAxis(self.axisY)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # Set the minimum height and width for the chart view
        self.chart_view.setMinimumHeight(200)
        self.chart_view.setMinimumWidth(500)

        # Adjust the y-axis range and tick count
        self.axisY.setRange(-50, 50)
        self.axisY.setTickCount(11)

        vLayout.addWidget(self.chart_view, stretch=1)
        vLayout.addWidget(self.eqPanel, stretch=0)

        apply_button = CircularButton(QIcon('resources/icons/check.svg'))
        apply_button.clicked.connect(self._on_apply_button_clicked)
        vLayout.addWidget(apply_button)

        vLayout.addStretch(1)
        self.setLayout(vLayout)

    def _on_apply_button_clicked(self):
        settings = self.eqPanel.get_equalizer_settings()
        self.controller._applyEq(settings)

    def paintEvent(self, event):
        super().paintEvent(event)
        self.update_spectrum()

    def update_spectrum(self):
        settings = self.eqPanel.get_equalizer_settings()
        frequencies = ["32 Hz", "64 Hz", "125 Hz", "250 Hz", "500 Hz", "1 kHz", "2 kHz", "4 kHz", "8 kHz", "16 kHz"]

        # Set the categories on the category axis
        self.axisX.clear()
        self.axisX.append(frequencies)

        self.series.clear()
        for i, gain in enumerate(settings):
            self.series.append(i, gain)

        self.chart_view.update()





