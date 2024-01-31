# test qdarkstyle

import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
import qdarkstyle

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Create the main layout
        layout = QVBoxLayout()

        # Create a button to switch themes
        self.theme_button = QPushButton('Switch Theme', self)
        self.theme_button.clicked.connect(self.toggle_theme)

        # Add the button to the layout
        layout.addWidget(self.theme_button)

        # Set the layout for the main window
        self.setLayout(layout)

        # Set the initial theme
        self.dark_theme = True
        self.apply_theme()

        # Set up the main window
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('Theme Switcher')
        self.show()

    def toggle_theme(self):
        # Toggle between dark and light themes
        self.dark_theme = not self.dark_theme
        self.apply_theme()

    def apply_theme(self):
        # Apply the chosen theme using qdarkstyle
        if self.dark_theme:
            self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt6())
        else:
            self.setStyleSheet('')  # Reset stylesheet to default (light theme)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec())
