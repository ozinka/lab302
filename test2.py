import sys, os
from PySide6.QtWidgets import  QApplication, QMainWindow, QTreeView, QFileSystemModel, QListView, QVBoxLayout, QWidget, \
    QSizePolicy
from PySide6.QtCore import QDir, QStringListModel


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
        model.setRootPath("/")
        model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)
        self.file_tree.setModel(model)
        self.file_tree.setRootIndex(model.index("/"))

        # File List
        self.file_list = QListView(self)
        self.file_list.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.file_tree)
        layout.addWidget(self.file_list)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Set up connections
        self.file_tree.selectionModel().selectionChanged.connect(self.update_file_list)

    def update_file_list(self):
        selected_index = self.file_tree.currentIndex()
        current_path = self.file_tree.model().filePath(selected_index)

        file_list = [f for f in os.listdir(current_path) if os.path.isfile(os.path.join(current_path, f))]

        file_model = QStringListModel()
        file_model.setStringList(file_list)

        self.file_list.setModel(file_model)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = FileExplorerApp()
    mainWin.setGeometry(100, 100, 600, 400)
    mainWin.setWindowTitle("File Explorer")
    mainWin.show()
    sys.exit(app.exec())
