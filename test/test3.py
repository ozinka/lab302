import sys
import random
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6 import QtCharts
from PySide6 import QtGui


class DateTimeDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(DateTimeDelegate, self).initStyleOption(option, index)
        value = index.data()
        option.text = QDateTime.fromMSecsSinceEpoch(value).toString("dd.MM.yyyy")


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setGeometry(0, 0, 1280, 400)
        self.chart_table()

        self.populate()

    def chart_table(self):
        self.table = QTableWidget(0, 2)
        delegate = DateTimeDelegate(self.table)
        self.table.setItemDelegateForColumn(0, delegate)
        chart = QtCharts.QChart()
        chart.layout().setContentsMargins(0, 0, 0, 0)
        self.chartView = QtCharts.QChartView(chart)
        self.chartView.setRenderHint(QtGui.QPainter.Antialiasing)
        self.chartView.setFixedSize(800, 430)

        splitter = QSplitter(self)
        splitter.addWidget(self.table)
        splitter.addWidget(self.chartView)
        self.setCentralWidget(splitter)

        series = QtCharts.QSplineSeries(name="Odoslané")
        mapper = QtCharts.QVXYModelMapper(self, xColumn=0, yColumn=1)
        mapper.setModel(self.table.model())
        mapper.setSeries(series)
        chart.addSeries(mapper.series())

        self.axis_X = QtCharts.QDateTimeAxis()
        self.axis_X.setFormat("MMM yyyy")
        self.axis_Y = QtCharts.QValueAxis()

        chart.setAxisX(self.axis_X, series)
        chart.setAxisY(self.axis_Y, series)
        self.axis_Y.setRange(-0.1, 2.1)
        # self.axis_Y.setLabelFormat("%d")
        self.axis_Y.setMinorTickCount(2)
        chart.setTitle("Chart")

    def addRow(self, dt, value):
        self.table.insertRow(0)
        for col, v in enumerate((dt.toMSecsSinceEpoch(), value)):
            it = QTableWidgetItem()
            it.setData(Qt.DisplayRole, v)
            self.table.setItem(0, col, it)

        if self.table.rowCount() == 1:
            self.axis_X.setRange(dt, dt.addDays(1))
            self.axis_Y.setRange(v, v)

        else:
            t_m, t_M = self.axis_X.min(), self.axis_X.max()
            t_m = min(t_m, dt)
            t_M = max(t_M, dt)

            m, M = self.axis_Y.min(), self.axis_Y.max()
            m = min(m, value)
            M = max(M, value)

            self.axis_X.setRange(t_m, t_M)
            self.axis_Y.setRange(m, M)

    def populate(self):
        for i in range(100):
            # simulate filling table with data as I get them from database.
            value = random.uniform(1, 40)
            fake_dt_str = QDate.currentDate().addDays(i).toString("dd.MM.yyyy")
            fake_value_str = str(random.uniform(0, 2))

            # Convert simulated data
            dt = QDateTime.fromString(fake_dt_str, "dd.MM.yyyy")
            value = float(fake_value_str)
            self.addRow(dt, value)

def main():
    app = QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())


main()