from PySide6.QtWidgets import QApplication, QMainWindow, QListView, QVBoxLayout, QLabel, QWidget
from PySide6.QtCore import QStringListModel


class ListViewExample(QMainWindow):
    def __init__(self):
        super(ListViewExample, self).__init__()

        # Initialize UI components
        self.init_ui()

    def init_ui(self):
        # Create QListView
        list_view = QListView(self)

        # Create QLabel for displaying selected item
        label = QLabel("Selected Item: ", self)

        # Create a QStringListModel and set it as the model for the QListView
        list_model = QStringListModel(self)
        list_model.setStringList(["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"])
        list_view.setModel(list_model)

        # Connect selection change to update_label method
        list_view.selectionModel().selectionChanged.connect(lambda: self.update_label(list_view, label))

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(list_view)
        layout.addWidget(label)

        # Set up central widget
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Set up main window
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle("QListView Example")

    def update_label(self, list_view, label):
        selected_indexes = list_view.selectedIndexes()
        if selected_indexes:
            selected_item = selected_indexes[0].data()
            label.setText(f"Selected Item: {selected_item}")
        else:
            label.setText("No Item Selected")


if __name__ == '__main__':
    app = QApplication([])
    main_win = ListViewExample()
    main_win.show()
    app.exec()
