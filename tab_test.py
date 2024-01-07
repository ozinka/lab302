from PySide6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QLabel, QSizePolicy, QTreeView, QTableWidget, QTableWidgetItem, \
    QSplitter
from PySide6.QtCore import Qt, QCoreApplication, QDir
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QListWidget, QTreeView, QFileSystemModel, QSplitter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class TabTest(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        # Add widgets directly to the tab
        self.create_file_explorer()

    def create_file_explorer(self):
        # Create a vertical layout for the file explorer
        explorer_layout = QVBoxLayout()

        # Create a file tree
        file_tree = QTreeView()
        file_tree_model = QFileSystemModel()
        file_tree_model.setRootPath('')
        file_tree.setModel(file_tree_model)
        file_tree.setRootIndex(file_tree_model.index(''))

        # Connect the selectionChanged signal to update the file list
        file_tree.selectionModel().selectionChanged.connect(self.update_file_list)

        explorer_layout.addWidget(file_tree)

        # Create a file list
        file_list_widget = QListWidget()
        explorer_layout.addWidget(file_list_widget)

        self.layout.addLayout(explorer_layout)

    def update_file_list(self):
        # Get the selected folder from the file tree
        selected_index = self.sender().currentIndex()
        selected_folder_path = self.sender().model().filePath(selected_index)

        # Update the file list with the files in the selected folder
        file_list_widget = self.layout.itemAt(0).itemAt(1).widget()  # Get the file list widget
        file_list_widget.clear()  # Clear the existing items

        # Add files to the file list
        file_list_widget.addItems(QDir(selected_folder_path).entryList())
