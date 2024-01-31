import os
import sys
from pathlib import Path
from fnmatch import fnmatch

from PySide6.QtCharts import QChart, QLineSeries, QChartView
from PySide6.QtCore import QDir, QStringListModel, Qt, QSettings, QCoreApplication
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QFrame, QWidget, QApplication, QFileSystemModel, QTreeView, QListView, QComboBox, \
    QVBoxLayout, QTableWidgetItem, QTableWidget, QTextEdit, QSplitter, QMainWindow
from qtpy.uic import loadUi
from PySide6 import QtCharts, QtGui


class TabHome(QFrame):
    def __init__(self):
        super().__init__()
        loadUi("gui/pages/tab_home.ui", self)

        self.settings = QSettings("KNU", "Lab302")

        # Files list
        self.lst_files = self.findChild(QListView, 'lst_files')
        self.lst_files_model = QStringListModel()
        self.lst_files.setModel(self.lst_files_model)
        self.selected_folder_path = None
        self.lst_files.selectionModel().currentChanged.connect(self.update_data_table)

        # Dirs tree
        self.tree_dirs = self.findChild(QTreeView, "tree_dirs")
        self.tree_dirs_model = QFileSystemModel()
        self.tree_dirs_model.setRootPath(QDir.rootPath())
        self.tree_dirs_model.setReadOnly(True)
        self.tree_dirs_model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)
        self.tree_dirs.setModel(self.tree_dirs_model)
        self.tree_dirs.header().hide()
        self.tree_dirs.hideColumn(1)
        self.tree_dirs.hideColumn(2)
        self.tree_dirs.hideColumn(3)
        self.tree_dirs.selectionModel().selectionChanged.connect(self.update_file_list)

        # Chart
        self.fr_chart = self.findChild(QFrame, 'fr_chart')
        self.chart = self.create_chart(self.fr_chart)

        # Text Data
        self.txt_stat = self.findChild(QTextEdit, 'txt_stat')

        # Filter
        self.cb_filter = self.findChild(QComboBox, 'cb_filter')
        self.cb_filter.addItems(
            ["All (*.*)",
             "CCD and Stat (*.ccd, *.sts)",
             "Data and Stat (*.dat, *.sts)",
             "CCD (*.ccd)"])
        self.cb_filter.currentIndexChanged.connect(self.update_file_list)

        # Table of Data
        self.tbl_data = self.findChild(QTableWidget, 'tbl_data')

        # Restore Tree Dirs current path
        tab_home_dir_path = self.settings.value("tab_home_dir_path", defaultValue="", type=str)
        self.tree_dirs.setExpanded(self.tree_dirs_model.index(tab_home_dir_path), True)
        self.tree_dirs.setCurrentIndex(self.tree_dirs_model.index(tab_home_dir_path))

    def update_text(self, file_name: str):
        try:
            with open(file_name, "r") as file:
                file_contents = file.read()
                self.txt_stat.setPlainText(file_contents)
        except FileNotFoundError:
            print(f"Error: The specified file '{file_name}' does not exist.")

    def create_chart(self, parent) -> QtCharts:
        chart = QChart()
        chart.legend().hide()
        chart.layout().setContentsMargins(0, 0, 0, 0)
        series = QLineSeries()
        series.append(0, 0)
        series.append(1, 1)
        series.append(2, 2)
        series.append(3, 0)
        chart.addSeries(series)

        chart_view = QChartView(chart)
        layout = QVBoxLayout(parent)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(chart_view)
        chart.setTheme(QChart.ChartThemeDark)

        return chart

    def update_chart(self):
        # Clear all series
        self.clear_chart(self.chart)

        serie = QtCharts.QSplineSeries()
        serie.setMarkerSize(2)  # Size in pixels
        serie.setColor(QColor("red"))

        for row in range(self.tbl_data.rowCount()):
            x_item = self.tbl_data.item(row, 0)
            y_item = self.tbl_data.item(row, 1)

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

    def clear_chart(self, chart):
        while chart.series():
            series = chart.series()[0]  # Get the first series
            chart.removeSeries(series)
            del series
        while chart.axes():
            axis = chart.axes()[0]  # Get the first axis
            chart.removeAxis(axis)
            del axis

    def update_data_table(self):
        file_name = self.lst_files.currentIndex().data()
        file_path = os.path.join(self.selected_folder_path, file_name)

        try:
            with open(file_path, "r") as file:
                lines = file.readlines()
                # Set the number of rows and columns in the table
                self.tbl_data.setRowCount(len(lines))
                self.tbl_data.setColumnCount(2)

                # Populate the table with data
                for row, line in enumerate(lines):
                    values = line.split()
                    if len(values) == 2:
                        self.tbl_data.setItem(row, 0, QTableWidgetItem(values[0]))
                        self.tbl_data.setItem(row, 1, QTableWidgetItem(values[1]))
                    if len(values) == 1:
                        self.tbl_data.setItem(row, 0, QTableWidgetItem(values[0]))
        except FileNotFoundError:
            print(f"Error: The specified file '{file_name}' does not exist.")

        self.update_chart()
        self.update_text(file_path)

        # Add file name to status bar
        QApplication.activeWindow().status_bar.showMessage(str(Path(str(file_path))), 0)

    def update_file_list(self):
        # Get the selected folder from the file tree
        selected_index = self.tree_dirs.currentIndex()
        self.selected_folder_path = self.tree_dirs_model.filePath(selected_index)

        exts = self.cb_filter.currentText()
        exts = exts[exts.find('(') + 1:exts.find(')')].replace(' ', '').split(',')

        file_list = os.listdir(self.selected_folder_path)
        filtered = [f for f in file_list if any([fnmatch(f, e) for e in exts])]
        self.lst_files_model.setStringList(filtered)

        self.spl_left = self.findChild(QSplitter, 'spl_left')
        self.spl_main = self.findChild(QSplitter, 'spl_main')
        self.spl_right = self.findChild(QSplitter, 'spl_right')
        print(f'left: {self.spl_left.sizes()}')
        print(f'main: {self.spl_main.sizes()}')
        print(f'right: {self.spl_right.sizes()}')
        print('*' * 40)

        # Save current Tree Dir path
        self.settings.setValue("tab_home_dir_path", self.selected_folder_path)
        print(f'Saved Path: {self.selected_folder_path}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    windows = TabHome()
    windows.show()
    app.exec_()
