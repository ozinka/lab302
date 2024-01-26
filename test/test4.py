import sys

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
from PySide6 import QtCharts
from PySide6 import QtGui
from PySide6.QtCore import Qt, QTimer, QPointF
from random import randint
import time


class ChartApp(QMainWindow):
    def __init__(self):
        super(ChartApp, self).__init__()

        # Initialize UI components
        self.init_ui()

    def init_ui(self):
        # Create chart view
        chart_view = QtCharts.QChartView(self)
        chart_view.setRenderHint(QtGui.QPainter.Antialiasing)

        # Create chart
        self.chart = QtCharts.QChart()
        self.chart.setTitle("Spline Chart")

        # Create spline series
        # self.spline_series = QtCharts.QSplineSeries()
        # self.spline_series = QtCharts.QLineSeries()
        self.spline_series = QtCharts.QScatterSeries()
        self.spline_series.setName("Spline Series")

        # Set point style
        self.spline_series.setMarkerShape(QtCharts.QScatterSeries.MarkerShapeCircle)
        self.spline_series.setMarkerSize(5)  # Size in pixels
        self.spline_series.setColor(QColor("red"))

        # Add series to chart
        self.chart.addSeries(self.spline_series)

        # Create X-axis and Y-axis
        axis_x = QtCharts.QValueAxis()
        axis_x.setRange(0, 3000)
        axis_x.setTickCount(11)
        axis_x.setLabelFormat("%d")
        self.chart.addAxis(axis_x, Qt.AlignBottom)
        self.spline_series.attachAxis(axis_x)

        axis_y = QtCharts.QValueAxis()
        axis_y.setRange(0, 30)
        axis_y.setTickCount(11)
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        self.spline_series.attachAxis(axis_y)

        # Set chart on the chart view
        chart_view.setChart(self.chart)

        # Create buttons
        button_spline1 = QPushButton("Spline y=x*x", self)
        button_spline1.clicked.connect(self.show_spline1)

        button_spline2 = QPushButton("Spline y=1/x", self)
        button_spline2.clicked.connect(self.show_spline2)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(button_spline1)
        layout.addWidget(button_spline2)
        layout.addWidget(chart_view)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Set up main window
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("QtChart Example")

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_series)
        self.timer.start(0)

    def show_spline1(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(0)

    def show_spline2(self):
        self.spline_series.clear()
        for x in range(1, 6):
            self.spline_series.append(x, 1 / x)
        self.chart.setTitle("Spline y=1/x")

    def update_series(self):
        start = time.time()
        points = []
        for x in range(3000):
            points.append(QPointF(x, randint(0, 10)))  # filling points with my prepared data
        self.spline_series.replace(points)  # fill list of points in one call
        end = time.time()
        print(end - start)

        # start = time.time()
        # self.spline_series.clear()
        # for x in range(3000):
        #     self.spline_series.append(x, randint(0, 10))
        # end = time.time()
        # print(end - start)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = ChartApp()
    mainWin.show()
    sys.exit(app.exec())
