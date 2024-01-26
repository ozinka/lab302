from fnmatch import fnmatch
import os
from pathlib import Path

from PySide6 import QtCharts, QtGui
from PySide6.QtCharts import QChart
from PySide6.QtCore import QDir, Qt, QStringListModel
from PySide6.QtGui import QColor, QBrush
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QApplication, \
    QTreeView, QFileSystemModel, QTableWidget, QTableWidgetItem, QSplitter, QListView


class TabExplore(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_folder_path = None
        self.main_layout = QVBoxLayout(self)

        # Create layout for File filter and File list
        file_widget = QWidget()
        file_layout = QVBoxLayout(file_widget)
        file_layout.setContentsMargins(0, 0, 0, 0)

        self.file_list_model = QStringListModel()
        self.file_tree_model = QFileSystemModel()

        # Create Splitters
        h_left_splitter = QSplitter(Qt.Horizontal)  # Left: File list, File tree; Right: h_right_splitter
        h_right_splitter = QSplitter(Qt.Horizontal)  # Left: table; Right: Chart, Bottom table
        v_left_splitter = QSplitter(Qt.Vertical)  # Top: File Filter, File List; Bottom: File Tree
        v_right_splitter = QSplitter(Qt.Vertical)  # Top: Chart; Bottom: Stat Table

        # Fill splitter panels with other splitters and widgets
        h_left_splitter.addWidget(v_left_splitter)
        h_left_splitter.addWidget(h_right_splitter)
        self.data_table = self.create_data_table(h_right_splitter)
        h_right_splitter.addWidget(v_right_splitter)
        self.file_filter = self.create_filter(file_layout)
        # File List
        self.file_list = QListView()
        file_layout.addWidget(self.file_list)

        v_left_splitter.addWidget(file_widget)
        self.chart = self.create_chart(v_right_splitter)
        self.create_stat_table(v_right_splitter)
        self.file_tree = self.create_file_tree(v_left_splitter)
        self.main_layout.addWidget(h_left_splitter)

        # Fix left splitter position on main window resize
        h_left_splitter.setStretchFactor(1, 1)
        h_right_splitter.setStretchFactor(1, 1)
        v_right_splitter.setSizes([200, 0])  # Collapse stat table

        self.file_filter.currentIndexChanged.connect(self.update_file_list)

        self.file_tree.setExpanded(self.file_tree_model.index("C:\\interferogram\\interferogram\\4480"), True)
        self.file_tree.setCurrentIndex(self.file_tree_model.index("C:\\interferogram\\interferogram\\4480"))

    def create_file_tree(self, parent):
        file_tree = QTreeView(parent)
        file_tree.setContentsMargins(0, 0, 0, 0)

        self.file_tree_model.setRootPath(QDir.rootPath())
        self.file_tree_model.setReadOnly(True)
        file_tree.setModel(self.file_tree_model)

        self.file_list.setModel(self.file_list_model)
        self.file_list.selectionModel().currentChanged.connect(self.update_data_table)
        file_tree.selectionModel().selectionChanged.connect(self.update_file_list)

        self.file_tree_model.setNameFilters(['Name'])
        file_tree.header().hide()
        file_tree.hideColumn(1)
        file_tree.hideColumn(2)
        file_tree.hideColumn(3)
        # Set the filter to display only folders
        self.file_tree_model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)
        return file_tree

    def clear_chart(self, chart):
        while chart.series():
            series = chart.series()[0]  # Get the first series
            chart.removeSeries(series)
            del series
        while chart.axes():
            axis = chart.axes()[0]  # Get the first axis
            chart.removeAxis(axis)
            del axis

    def create_data_table(self, parent):
        data_table = QTableWidget(10, 2)
        parent.addWidget(data_table)
        return data_table

    def create_stat_table(self, parent):
        stat_table = QTableWidget(10, 2)
        for row in range(10):
            for col in range(3):
                item = QTableWidgetItem(f'Row {row + 1}, Col {col + 1}')
                stat_table.setItem(row, col, item)
        parent.addWidget(stat_table)

    def create_chart(self, parent):
        chart = QtCharts.QChart()
        chart_view = QtCharts.QChartView(parent)
        chart.layout().setContentsMargins(0, 4, 4, 0)
        chart_view.setRenderHint(QtGui.QPainter.Antialiasing)
        # self.chart.setTitle("Spline Chart")

        # Create spline series
        # self.spline_series = QtCharts.QSplineSeries()
        # self.spline_series = QtCharts.QLineSeries()
        # self.spline_series.setName("Spline Series")

        # Set Margins

        # Set point style

        # Add series to chart

        chart.legend().hide()

        # Set chart on the chart view
        chart_view.setChart(chart)
        chart_view.chart().setTheme(QChart.ChartThemeDark)
        # QChart::ChartThemeLight
        # QChart::ChartThemeBlueCerulean
        # QChart::ChartThemeDark
        # QChart::ChartThemeBrownSand
        # QChart::ChartThemeBlueNcs
        # QChart::ChartThemeHighContrast
        # QChart::ChartThemeBlueIcy
        # QChart::ChartThemeQt
        return chart

    def create_filter(self, parent):
        filter = QComboBox()
        filter.addItems(
            ["All (*.*)",
             "CCD and Stat (*.ccd, *.sts)",
             "Data and Stat (*.dat, *.sts)",
             "CCD (*.ccd)"])

        parent.addWidget(filter)
        return filter

    def update_data_table(self):
        file_name = self.file_list.currentIndex().data()
        file_path = os.path.join(self.selected_folder_path, file_name)
        try:
            with open(file_path, "r") as file:
                lines = file.readlines()
                # Set the number of rows and columns in the table
                self.data_table.setRowCount(len(lines))
                self.data_table.setColumnCount(2)

                # Populate the table with data
                for row, line in enumerate(lines):
                    values = line.split()
                    if len(values) == 2:
                        self.data_table.setItem(row, 0, QTableWidgetItem(values[0]))
                        self.data_table.setItem(row, 1, QTableWidgetItem(values[1]))
                    if len(values) == 1:
                        self.data_table.setItem(row, 0, QTableWidgetItem(values[0]))
        except FileNotFoundError:
            print(f"Error: The specified file '{file_name}' does not exist.")

        self.update_chart()

        # Add file name to status bar
        QApplication.activeWindow().status_bar.showMessage(str(Path(str(file_path))), 0)

    def update_chart(self):
        # Clear all series
        self.clear_chart(self.chart)

        # serie = QtCharts.QScatterSeries()
        # serie = QtCharts.QLineSeries()
        serie = QtCharts.QSplineSeries()
        # serie.setMarkerShape(QtCharts.QScatterSeries.MarkerShapeCircle)
        serie.setMarkerSize(2)  # Size in pixels
        serie.setColor(QColor("red"))
        # serie.setBorderColor(QColor("red"))

        for row in range(self.data_table.rowCount()):
            x_item = self.data_table.item(row, 0)
            y_item = self.data_table.item(row, 1)

            if x_item and y_item:
                x = float(x_item.text())
                y = float(y_item.text())
                serie.append(x, y)

        self.chart.addSeries(serie)

        # Create X-axis and Y-axis
        axis_x = QtCharts.QValueAxis()
        axis_x.setRange(0, 21)
        axis_x.setTickCount(11)
        axis_x.setLabelFormat("%d")
        self.chart.addAxis(axis_x, Qt.AlignBottom)
        serie.attachAxis(axis_x)

        axis_y = QtCharts.QValueAxis()
        axis_y.setRange(0, 200)
        axis_y.setTickCount(11)
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        serie.attachAxis(axis_y)

    def update_file_list(self):
        # Get the selected folder from the file tree
        selected_index = self.file_tree.currentIndex()
        self.selected_folder_path = self.file_tree_model.filePath(selected_index)

        exts = self.file_filter.currentText()
        exts = exts[exts.find('(') + 1:exts.find(')')].replace(' ', '').split(',')

        file_list = os.listdir(self.selected_folder_path)
        filtered = [f for f in file_list if any([fnmatch(f, e) for e in exts])]
        self.file_list_model.setStringList(filtered)


if __name__ == "__main__":
    pass
