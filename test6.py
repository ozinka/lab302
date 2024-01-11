import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6 import QtCharts, QtGui
from PySide6.QtCore import Qt


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
        chart = QtCharts.QChart()
        # chart.setTitle("Simple Chart")

        # Create line series
        series = QtCharts.QLineSeries()
        series.setName("Data Series")

        # Add data points to the series
        series.append(0, 1)
        series.append(1, 3)
        series.append(2, 2)
        series.append(3, 4)
        series.append(4, 1)

        # Add series to chart
        chart.addSeries(series)

        # Create X-axis and Y-axis
        axis_x = QtCharts.QValueAxis()
        axis_x.setTickCount(5)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QtCharts.QValueAxis()
        axis_y.setTickCount(5)
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        # Set minimal padding
        chart.layout().setContentsMargins(0, 0, 0, 0)
        chart.legend().hide()

        # Set chart on the chart view
        chart_view.setChart(chart)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(chart_view)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Set up main window
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("QtChart Example")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = ChartApp()
    mainWin.show()
    sys.exit(app.exec())
