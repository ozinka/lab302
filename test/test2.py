import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCharts import QChart, QChartView, QLineSeries
import qdarkstyle

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create layout
        layout = QVBoxLayout(central_widget)

        # Create a button to switch between light and dark themes
        self.theme_button = QPushButton("Switch Theme", self)
        self.theme_button.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_button)

        # Create a QChart
        chart = QChart()
        series = QLineSeries()
        series.append(0, 0)
        series.append(1, 1)
        series.append(2, 2)
        series.append(3, 0)
        chart.addSeries(series)

        chart_view = QChartView(chart)
        layout.addWidget(chart_view)

        # Variable to track the current theme
        self.dark_theme = True

    def toggle_theme(self):
        # Toggle between light and dark themes using qdarkstyle
        qApp = QApplication.instance()

        if self.dark_theme:
            qApp.setStyleSheet("")
        else:
            qApp.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())

        # Apply the theme to the QChart
        for widget in qApp.allWidgets():
            if isinstance(widget, QChartView):
                widget.chart().setTheme(QChart.ChartThemeLight if self.dark_theme else QChart.ChartThemeDark)

        # Invert the theme status
        self.dark_theme = not self.dark_theme

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Apply a dark theme by default
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())

    window = MyMainWindow()
    window.show()

    sys.exit(app.exec())
