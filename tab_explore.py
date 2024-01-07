from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QTreeView, QFileSystemModel, \
    QTableWidget, QTableWidgetItem, QSplitter
from PySide6.QtCore import QCoreApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import os
import numpy as np


class TabExplore(QWidget):
    def __init__(self):
        super().__init__()

        self.page_layout = QHBoxLayout(self)
        self.left_layout = QVBoxLayout()
        self.page_layout.addLayout(self.left_layout)

        # Add widgets to the frame
        self.create_file_tree()
        self.create_table()
        self.create_matplotlib_plot()

        button_exit = QPushButton('Exit')
        button_exit.clicked.connect(self.on_exit_clicked)


        self.left_layout.addWidget(button_exit)


    def create_file_tree(self):
        file_tree = QTreeView()
        # Add logic to populate the file tree, e.g., using QFileSystemModel
        # For simplicity, a placeholder directory is used here.
        model = QFileSystemModel()
        model.setRootPath(os.path.expanduser('~'))
        file_tree.setModel(model)
        file_tree.setRootIndex(model.index(os.path.expanduser('~')))
        self.left_layout.addWidget(file_tree)

    def create_table(self):
        table = QTableWidget(10, 3)
        for row in range(10):
            for col in range(3):
                item = QTableWidgetItem(f'Row {row + 1}, Col {col + 1}')
                table.setItem(row, col, item)
        self.page_layout.addWidget(table)

    def create_matplotlib_plot(self):
        plot_canvas = PlotCanvas(self)
        self.page_layout.addWidget(plot_canvas)

    def on_next_clicked(self):
        print("Next button clicked")

    def on_exit_clicked(self):
        QCoreApplication.instance().quit()
        print("Exit button clicked")


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
