from PySide6.QtWidgets import QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QSizePolicy, \
    QTreeView, QSplitterHandle,\
    QFileSystemModel, \
    QTableWidget, QTableWidgetItem, QSplitter
from PySide6.QtCore import QCoreApplication, QDir, Qt
from PySide6.QtGui import QPainter, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import fnmatch, os
import numpy as np


class TabExplore(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.left_layout = QHBoxLayout()

        # Create layout for File filter and File list
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)

        # Create Splitters
        h_left_splitter = QSplitter(Qt.Horizontal)
        h_right_splitter = QSplitter(Qt.Horizontal)
        v_left_splitter = QSplitter(Qt.Vertical)
        v_right_splitter = QSplitter(Qt.Vertical)

        # Fill splitter panels with other splitters and widgets
        h_left_splitter.addWidget(v_left_splitter)
        h_left_splitter.addWidget(h_right_splitter)
        self.create_stat_table(h_right_splitter)
        h_right_splitter.addWidget(v_right_splitter)
        self.create_filter_widget(top_layout)
        self.file_list_widget = QListWidget()
        top_layout.addWidget(self.file_list_widget)
        v_left_splitter.addWidget(top_widget)
        self.create_plot(v_right_splitter)
        self.create_stat_table(v_right_splitter)
        self.create_file_tree(v_left_splitter)
        self.layout.addWidget(h_left_splitter)

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

    def update_file_list(self):
        # Get the selected folder from the file tree
        selected_index = self.sender().currentIndex()
        selected_folder_path = self.sender().model().filePath(selected_index)

        file_list = fnmatch.filter(os.listdir(selected_folder_path), '*.ccd')

        # Add files to the file list
        self.file_list_widget.addItems(file_list)

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
        parent.addWidget(stat_table)

    def create_plot(self, parent):
        plot_canvas = PlotCanvas(self)
        parent.addWidget(plot_canvas)


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        # Plot y=x*x
        x = np.linspace(0, 10, 100)
        y = x * x
        self.axes.plot(x, y, label='y=x*x')

        self.axes.set_title('Matplotlib Plot: y=x*x')
        self.axes.set_xlabel('X-axis')
        self.axes.set_ylabel('Y-axis')
        self.axes.legend()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)



