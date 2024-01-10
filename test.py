import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileSystemModel, QTreeView, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QSizePolicy
from PySide6.QtCore import QDir
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class FileExplorerApp(QMainWindow):
    def __init__(self):
        super(FileExplorerApp, self).__init__()

        # Initialize UI components
        self.init_ui()

    def init_ui(self):
        # File Tree
        self.file_tree = QTreeView(self)
        self.file_tree.setRootIsDecorated(False)
        self.file_tree.setSortingEnabled(True)
        self.file_tree.setHeaderHidden(True)

        # Set up file tree model
        model = QFileSystemModel()
        model.setRootPath(QDir.rootPath())
        model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)
        self.file_tree.setModel(model)
        self.file_tree.setRootIndex(model.index(QDir.rootPath()))

        # File List
        self.file_list = QTableWidget(self)
        self.file_list.setColumnCount(1)
        self.file_list.setHorizontalHeaderLabels(["Files"])
        self.file_list.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.file_list.setColumnWidth(0, 200)

        # Table
        self.data_table = QTableWidget(self)
        self.data_table.setColumnCount(2)
        self.data_table.setHorizontalHeaderLabels(["X", "Y"])

        # Matplotlib Plot
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.file_tree)
        layout.addWidget(self.file_list)
        layout.addWidget(self.data_table)
        layout.addWidget(self.canvas)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Set up connections after the file tree is properly set up
        self.file_tree.selectionModel().selectionChanged.connect(self.update_file_list)
        self.file_list.itemSelectionChanged.connect(self.load_data_from_file)

    def update_file_list(self):
        selected_index = self.file_tree.currentIndex()
        current_path = self.file_tree.model().filePath(selected_index)

        file_model = self.file_list.model()
        # file_model.clear()
        # file_model.setHorizontalHeaderLabels(["Files"])

        file_list = [f for f in os.listdir(current_path) if f.endswith(".ccd")]

        for file_name in file_list:
            item = QTableWidgetItem(file_name)
            file_model.setItem(file_model.rowCount(), 0, item)

    def load_data_from_file(self):
        selected_items = self.file_list.selectedItems()

        if selected_items:
            selected_file = selected_items[0].text()
            file_path = os.path.join(self.file_tree.model().filePath(self.file_tree.currentIndex()), selected_file)

            with open(file_path, 'r') as file:
                content = file.readlines()

                # Clear previous data in the table
                self.data_table.setRowCount(0)

                for line in content:
                    x, y = map(float, line.split())
                    row_position = self.data_table.rowCount()
                    self.data_table.insertRow(row_position)
                    self.data_table.setItem(row_position, 0, QTableWidgetItem(str(x)))
                    self.data_table.setItem(row_position, 1, QTableWidgetItem(str(y)))

                # Update Matplotlib plot
                self.update_matplotlib_plot()

    def update_matplotlib_plot(self):
        self.ax.clear()

        x_values = [float(self.data_table.item(row, 0).text()) for row in range(self.data_table.rowCount())]
        y_values = [float(self.data_table.item(row, 1).text()) for row in range(self.data_table.rowCount())]

        self.ax.plot(x_values, y_values)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_title('Linear Plot')

        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = FileExplorerApp()
    mainWin.setGeometry(100, 100, 800, 600)
    mainWin.setWindowTitle("File Explorer and Plotter")
    mainWin.show()
    sys.exit(app.exec())
