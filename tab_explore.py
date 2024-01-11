from PySide6 import QtCharts, QtGui
from PySide6.QtWidgets import QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QSizePolicy, \
    QTreeView, QFileSystemModel, QTableWidget, QTableWidgetItem, QSplitter, QListView
from PySide6.QtCore import QCoreApplication, QDir, Qt, QStringListModel
from PySide6.QtGui import QPainter, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import fnmatch, os


class TabExplore(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout(self)

        # Create layout for File filter and File list
        file_widget = QWidget()
        file_layout = QVBoxLayout(file_widget)
        file_layout.setContentsMargins(0, 0, 0, 0)

        self.file_tree_model = QStringListModel()
        # self.file_model = QStringListModel()

        # Create Splitters
        h_left_splitter = QSplitter(Qt.Horizontal)  # Left: File list, File tree; Right: h_right_splitter
        h_right_splitter = QSplitter(Qt.Horizontal)  # Left: table; Right: Chart, Bottom table
        v_left_splitter = QSplitter(Qt.Vertical)  # Top: File Filter, File List; Bottom: File Tree
        v_right_splitter = QSplitter(Qt.Vertical)  # Top: Chart; Bottom: Stat Table

        # Fill splitter panels with other splitters and widgets
        h_left_splitter.addWidget(v_left_splitter)
        h_left_splitter.addWidget(h_right_splitter)
        self.create_stat_table(h_right_splitter)
        h_right_splitter.addWidget(v_right_splitter)
        self.create_filter_widget(file_layout)
        # File List
        self.file_list_widget = QListView()
        file_layout.addWidget(self.file_list_widget)

        v_left_splitter.addWidget(file_widget)
        self.create_plot(v_right_splitter)
        self.create_stat_table(v_right_splitter)
        self.create_file_tree(v_left_splitter)
        self.main_layout.addWidget(h_left_splitter)

        # Fix left splitter position on main window resize
        h_left_splitter.setStretchFactor(1, 1)
        h_right_splitter.setStretchFactor(1, 1)

    def create_filter_widget(self, parent):
        filter_widget = QComboBox()

        # Add filter options to the combo box
        filter_widget.addItems(
            ["All (*.*)", "Stat and CCD (*.sts,*.ccd)", "Stat and Data (*.sts, *.dat)", "CCD (*.ccd)"])

        parent.addWidget(filter_widget)

    def create_file_tree(self, parent):
        file_tree = QTreeView()
        file_tree.setContentsMargins(0, 0, 0, 0)
        # Add logic to populate the file tree, e.g., using QFileSystemModel
        # For simplicity, a placeholder directory is used here.
        model = QFileSystemModel()
        model.setRootPath('')
        model.setReadOnly(True)
        model.setNameFilters(['Name'])
        file_tree.setModel(model)
        file_tree.setRootIndex(model.index(''))
        file_tree.header().hide()
        file_tree.hideColumn(1)
        file_tree.hideColumn(2)
        file_tree.hideColumn(3)
        file_tree.selectionModel().selectionChanged.connect(self.update_file_list)
        # Set the filter to display only folders
        model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)
        parent.addWidget(file_tree)

        self.file_list_widget.setModel(self.file_tree_model)
        self.file_list_widget.selectionModel().currentChanged.connect(self.update_data_table)

    def update_file_list(self):
        # Get the selected folder from the file tree
        selected_index = self.sender().currentIndex()
        self.selected_folder_path = self.sender().model().filePath(selected_index)

        file_list = fnmatch.filter(os.listdir(self.selected_folder_path), '*.ccd')
        self.file_tree_model.setStringList(file_list)

    def update_data_table(self):
        file_name = self.file_list_widget.currentIndex().data()
        print(os.path.join(self.selected_folder_path, file_name))

    def create_data_table(self, parent):
        data_table = QTableWidget(10, 2)
        for row in range(10):
            for col in range(2):
                item = QTableWidgetItem(f'Row {row + 1}, Col {col + 1}')
                data_table.setItem(row, col, item)
        parent.addWidget(data_table)

    def create_stat_table(self, parent):
        stat_table = QTableWidget(10, 2)
        for row in range(10):
            for col in range(3):
                item = QTableWidgetItem(f'Row {row + 1}, Col {col + 1}')
                stat_table.setItem(row, col, item)
        # parent.addWidget(stat_table)
        parent.addWidget(stat_table)

    def create_plot(self, parent):
        # Create chart
        self.chart = QtCharts.QChart()
        # Create chart view
        chart_view = QtCharts.QChartView(self)
        # chart_view.setRenderHint(QtGui.QPainter.Antialiasing)

        # self.chart.setTitle("Spline Chart")

        # Create spline series
        # self.spline_series = QtCharts.QSplineSeries()
        # self.spline_series = QtCharts.QLineSeries()
        self.spline_series = QtCharts.QScatterSeries()
        # self.spline_series.setName("Spline Series")

        # Set Margins
        self.chart.layout().setContentsMargins(0, 4, 4, 0)

        # Set point style
        self.spline_series.setMarkerShape(QtCharts.QScatterSeries.MarkerShapeCircle)
        self.spline_series.setMarkerSize(5)  # Size in pixels
        self.spline_series.setColor(QColor("red"))

        # Add series to chart
        self.chart.addSeries(self.spline_series)
        self.chart.legend().hide()

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
        parent.addWidget(chart_view)
