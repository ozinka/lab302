from PySide6.QtWidgets import QApplication, QMainWindow, QSplitter, QTextEdit
import sys
from PySide6.QtCore import QCoreApplication, QDir, Qt
class SplitterExample(QMainWindow):
    def __init__(self):
        super(SplitterExample, self).__init__()

        self.setWindowTitle("Splitter Example")
        self.setGeometry(100, 100, 800, 600)

        # Create a splitter
        splitter = QSplitter(Qt.Horizontal, self)

        # Create widgets for the left and right areas
        left_widget = QTextEdit("Left Area", self)
        right_widget = QTextEdit("Right Area", self)

        # Add widgets to the splitter
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        # Set the right area as collapsible
        splitter.setCollapsible(1, True)

        # Collapse the right area
        splitter.setSizes([300, 0])

        # Set the splitter as the central widget
        self.setCentralWidget(splitter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplitterExample()
    window.show()
    sys.exit(app.exec())
