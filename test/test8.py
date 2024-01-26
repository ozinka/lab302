from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem
from PySide6 import QtCharts
import sys
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt


class DataPlotter(QMainWindow):
    def __init__(self):
        super(DataPlotter, self).__init__()

        self.setWindowTitle("Data Plotter")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Vertical layout
        layout = QVBoxLayout(central_widget)

        # Create a table widget
        table_widget = QTableWidget(self)
        layout.addWidget(table_widget)

        # Create a chart view
        chart_view = QtCharts.QChartView(self)
        chart_view.setRenderHint(QPainter.Antialiasing)

        # Add the chart view to the layout
        layout.addWidget(chart_view)

        # Read data from the file and populate the table
        file_path = "C:/interferogram/interferogram/4480\Work_CuI_interferogram_4480_01.ccd"  # Replace with your file path
        self.populate_table(table_widget, file_path)

        # Create and set up the chart
        chart = self.create_chart(table_widget)
        chart_view.setChart(chart)

    def populate_table(self, table_widget, file_path):
        try:
            with open(file_path, "r") as file:
                # Read lines from the file
                lines = file.readlines()

                # Set the number of rows and columns in the table
                table_widget.setRowCount(len(lines))
                table_widget.setColumnCount(2)

                # Populate the table with data
                for row, line in enumerate(lines):
                    values = line.split()
                    if len(values) >= 2:
                        table_widget.setItem(row, 0, QTableWidgetItem(values[0]))
                        table_widget.setItem(row, 1, QTableWidgetItem(values[1]))

        except FileNotFoundError:
            print(f"Error: The specified file '{file_path}' does not exist.")

    def create_chart(self, table_widget):
        chart = QtCharts.QChart()

        # Create a series to hold the data
        series = QtCharts.QLineSeries()

        # Get data from the table and add it to the series
        for row in range(table_widget.rowCount()):
            x_item = table_widget.item(row, 0)
            y_item = table_widget.item(row, 1)

            if x_item and y_item:
                x = float(x_item.text())
                y = float(y_item.text())
                series.append(x, y)

        # Add the series to the chart
        chart.addSeries(series)

        # Set up the chart axes
        axis_x = QtCharts.QValueAxis()
        axis_x.setTitleText("X Axis")
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QtCharts.QValueAxis()
        axis_y.setTitleText("Y Axis")
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        return chart


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataPlotter()
    window.show()
    sys.exit(app.exec())
