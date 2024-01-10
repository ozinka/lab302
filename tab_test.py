from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QLabel, QSizePolicy, QTreeView, QTableWidget, \
    QTableWidgetItem, \
    QSplitter, QHeaderView
from PySide6.QtCore import Qt, QCoreApplication, QDir
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QListWidget, QTreeView, QFileSystemModel, QSplitter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import os


class TabTest(QWidget):
    def __init__(self):
        super(FileTab, self).__init__()

        # File Tree
        self.file_tree = QTreeView(self)
        self.file_tree.setRootIsDecorated(False)
        self.file_tree.setSortingEnabled(True)
        self.file_tree.setHeaderHidden(True)

        # File List
        self.file_list = QTableWidget(self)
        self.file_list.setColumnCount(1)
        self.file_list.setHorizontalHeaderLabels(["Files"])
        self.file_list.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.file_list.setColumnWidth(0, 200)

        # Matplotlib Plot
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.file_tree)
        layout.addWidget(self.file_list)
        layout.addWidget(self.canvas)

        # Set up connections
        self.file_tree.selectionModel().selectionChanged.connect(self.update_file_list)
        self.file_list.itemSelectionChanged.connect(self.plot_selected_file)

        # Initialize the file tree
        self.setup_file_tree()

    def setup_file_tree(self):
        model = QFileSystemModel()
        model.setRootPath(QDir.rootPath())
        model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)

        self.file_tree.setModel(model)
        self.file_tree.setRootIndex(model.index(QDir.rootPath()))

    def update_file_list(self):
        selected_index = self.file_tree.currentIndex()
        current_path = self.file_tree.model().filePath(selected_index)

        file_model = QStandardItemModel()
        file_list = [f for f in os.listdir(current_path) if f.endswith(".ccd")]

        for file_name in file_list:
            item = QStandardItem(file_name)
            file_model.appendRow(item)

        self.file_list.setModel(file_model)

    def plot_selected_file(self):
        selected_items = self.file_list.selectedItems()

        if selected_items:
            selected_file = selected_items[0].text()
            file_path = os.path.join(self.file_tree.model().filePath(self.file_tree.currentIndex()), selected_file)

            with open(file_path, 'r') as file:
                content = file.readlines()
                x_values = [float(line.split()[0]) for line in content]
                y_values = [float(line.split()[1]) for line in content]

                # Clear previous plot
                self.ax.clear()

                # Plot new data
                self.ax.plot(x_values, y_values)
                self.ax.set_xlabel('X')
                self.ax.set_ylabel('Y')
                self.ax.set_title(f'Plot for {selected_file}')

                # Redraw canvas
                self.canvas.draw()


class PlotTab(QWidget):
    def __init__(self):
        super().__init__()

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)

    def update_plot(self, selected_file):
        # Read data from the selected file
        file_path = os.path.join(selected_folder, selected_file)
        data = np.loadtxt(file_path)

        # Plot the data
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(data[:, 0], data[:, 1])

        # Update the canvas
        self.canvas.draw()
