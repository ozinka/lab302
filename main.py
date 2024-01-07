from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget
from tab_explore import TabExplore
from tab_run import TabRun
from tab_test import TabTest

tabs = {'Explore': TabExplore, 'Run': TabRun, 'Test': TabTest}

class MyGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Lab302')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)

        # Create three tabs using the TabModule
        for k, v in tabs.items():
            self.central_widget.addTab(v(), k)

if __name__ == '__main__':
    app = QApplication([])
    window = MyGUI()
    window.show()
    app.exec()
