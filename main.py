# ///////////////////////////////////////////////////////////////
#
# Created by Vitaliy Osidach for
#
# As base UI window was used sidebar UI created BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 6.1.0
#
# ///////////////////////////////////////////////////////////////

# IMPORT MODULES
import sys

import theme
import qdarkstyle

# IMPORT QT CORE
from qt_core import *

# IMPORT MAIN WINDOW
from gui.windows.main_window.ui_main_window import UI_MainWindow


# MAIN WINDOW
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: black;")

        self.setWindowTitle("Lab302")

        # SETUP MAIN WINDOW
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        # Toggle button
        self.ui.toggle_button.clicked.connect(self.toggle_button)

        # Btn home
        self.ui.btn_1.clicked.connect(self.show_home_page)

        # Btn widgets
        self.ui.btn_2.clicked.connect(self.show_work_page)

        # Btn settings
        self.ui.settings_btn.clicked.connect(self.show_page_3)

        # Settings
        self.settings = QSettings("KNU", "Lab302")
        # self.settings.objectName('settings')
        self.restoreSettings()

        # DISPLAY OUR APPLICATION
        self.show()

    # Reset BTN Selection
    def reset_selection(self):
        for btn in self.ui.left_menu.findChildren(QPushButton):
            try:
                btn.set_active(False)
            except:
                pass

    # Btn home function
    def show_home_page(self):
        self.reset_selection()
        self.ui.pages.setCurrentWidget(self.ui.ui_pages.page_home)
        self.ui.btn_1.set_active(True)
        self.ui.top_label_right.setText('| Home')

    # Btn widgets function
    def show_work_page(self):
        self.reset_selection()
        self.ui.pages.setCurrentWidget(self.ui.ui_pages.page_2)
        self.ui.btn_2.set_active(True)

    # Btn Settings
    def show_page_3(self):
        self.reset_selection()
        self.ui.pages.setCurrentWidget(self.ui.ui_pages.page_3)
        self.ui.settings_btn.set_active(True)

    # Toggle button
    def toggle_button(self):
        # Get menu width
        menu_width = self.ui.left_menu.width()

        # Check with
        width = 50
        if menu_width == 50:
            width = 150

        # Start animation
        self.animation = QPropertyAnimation(self.ui.left_menu, b"minimumWidth")
        self.animation.setStartValue(menu_width)
        self.animation.setEndValue(width)
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.InOutCirc)
        self.animation.start()

    def closeEvent(self, event):
        self.saveSettings()

    def saveSettings(self):
        # Splitters
        spl_left = self.findChild(QSplitter, 'spl_left')
        spl_main = self.findChild(QSplitter, 'spl_main')
        spl_right = self.findChild(QSplitter, 'spl_right')

        self.settings.setValue("spl_left", spl_left.sizes())
        self.settings.setValue("spl_main", spl_main.sizes())
        self.settings.setValue("spl_right", spl_right.sizes())

        # Main Window
        self.settings.setValue("main_window_geometry", self.saveGeometry())

    def restoreSettings(self):
        # Splitters
        spl_left = self.findChild(QSplitter, 'spl_left')
        spl_main = self.findChild(QSplitter, 'spl_main')
        spl_right = self.findChild(QSplitter, 'spl_right')

        spl_left_sizes = self.settings.value("spl_left", defaultValue=[100, 200], type=list)
        spl_main_sizes = self.settings.value("spl_main", defaultValue=[100, 200, 200], type=list)
        spl_right_sizes = self.settings.value("spl_right", defaultValue=[100, 200], type=list)

        spl_left.setSizes([int(i) for i in spl_left_sizes])
        spl_main.setSizes([int(i) for i in spl_main_sizes])
        spl_right.setSizes([int(i) for i in spl_right_sizes])

        # Main Window
        self.restoreGeometry(self.settings.value("main_window_geometry", QByteArray()))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("gui/images/icon.ico"))
    dark_stylesheet = qdarkstyle.load_stylesheet_pyqt6()
    app.setStyleSheet(dark_stylesheet)
    window = MainWindow()
    sys.exit(app.exec())
