from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QLogValueAxis, QValueAxis
from PySide6.QtCore import Qt
from PySide6 import QtGui
import sys
import math


def series_to_chart(chart):
    series = QLineSeries(chart)
    for i in range(-100, 200):
        series.append(i**2, math.exp(i/20.0))

    chart.addSeries(series)

    axis_x = QValueAxis()
    axis_y = QLogValueAxis()

    axis_x.setTickCount(10)
    axis_y.setBase(10)
    axis_y.setMinorTickCount(-1)
    axis_y.setMax(100000)
    axis_y.setMin(.1)
    axis_y.setLabelFormat("%0.0e")
    axis_y.setRange(-1, 1.8e+6)

    chart.addAxis(axis_x, Qt.AlignBottom)
    chart.addAxis(axis_y, Qt.AlignLeft)

    series.attachAxis(axis_x)
    series.attachAxis(axis_y)

    return chart


if __name__ == "__main__":
    app = QApplication(sys.argv)

    chart = series_to_chart(QChart())

    view = QChartView(chart)
    view.setRenderHint(QtGui.QPainter.Antialiasing)

    window = QMainWindow()
    window.setCentralWidget(view)
    window.resize(400, 300)
    window.show()

    sys.exit(app.exec())