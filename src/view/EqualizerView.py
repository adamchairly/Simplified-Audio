# coding:utf-8
from PyQt5.QtWidgets import QVBoxLayout, QFrame
from PyQt5.QtGui import QIcon, QPainter, QBrush, QColor
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QBarCategoryAxis,QValueAxis
from PyQt5.QtCore import Qt
from util.CustomControls import EqualizerPanel, CircularButton

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

        # Create a value axis for the y-axis
        self.axisY = QValueAxis()
        self.axisY.setRange(-6, 6)
        #self.axisY.setTickCount(11)
        self.chart.addAxis(self.axisY, Qt.AlignLeft)

        # Create a category axis for the frequency labels
        self.axisX = QBarCategoryAxis()
        self.chart.addAxis(self.axisX, Qt.AlignBottom)

        # Now we add the series to the chart and attach the axes
        self.chart.addSeries(self.series)
        self.series.attachAxis(self.axisX)
        self.series.attachAxis(self.axisY)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setStyleSheet("background: transparent;")

        # Set the minimum height and width for the chart view
        self.chart_view.setMinimumHeight(150)
        self.chart_view.setMinimumWidth(500)

        vLayout.addWidget(self.chart_view, stretch=1)
        vLayout.addWidget(self.eqPanel, stretch=0)

        apply_button = CircularButton(QIcon('resources/icons/check.svg'))
        apply_button.clicked.connect(self._on_apply_button_clicked)
        vLayout.addWidget(apply_button)

        vLayout.addStretch(1)
        self.setLayout(vLayout)

    def _on_apply_button_clicked(self):
        settings = self.eqPanel.get_equalizer_settings()
        print(settings)
        self.controller._applyEq(settings)
        self.controller._log_message("Equalizer applied.")

    def paintEvent(self, event):
        super().paintEvent(event)
        self.update_spectrum()

    def update_spectrum(self):
        settings = self.eqPanel.get_equalizer_settings()
        frequencies = ["64 Hz", "125 Hz", "300 Hz", "800 Hz", "1.6 kHz", "3.2 kHz"]

        self.axisX.clear()
        self.axisX.append(frequencies)

        self.series.clear()

        for i, gain in enumerate(settings):
            self.series.append(i, gain)

        self.chart_view.update()





