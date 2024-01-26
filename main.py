from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QStatusBar
from tab_explore import TabExplore
from tab_run import TabRun
from tab_test import TabTest
from PySide6.QtCore import Qt

from theme import set_theme

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

        # Create a status bar
        self.status_bar = CustomStatusBar()
        self.setStatusBar(self.status_bar)
        # self.status_bar.showMessage("Ready", 3000)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


class CustomStatusBar(QStatusBar):
    def __init__(self):
        super(CustomStatusBar, self).__init__()

        self.showMessage("This is a status message.")

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.currentMessage())

            # Optionally, show a notification or perform any other actions
            print("Text copied to clipboard:", self.currentMessage())


if __name__ == '__main__':
    app = QApplication([])
    set_theme(app, 'light')
    # set_matplotlib_dark_theme()

    window = MyGUI()
    window.setGeometry(200, 200, 1200, 800)
    window.show()
    app.exec()
