# Імпортуємо необхідні модулі
from PySide6.QtCharts import QChart, QLineSeries, QChartView
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QStyleFactory, QPlainTextEdit, QTableView
from PySide6.QtCore import Qt, QAbstractTableModel
from PySide6.QtGui import QPalette, QColor
import numpy as np # для створення даних для qchart
import numpy as np # для створення даних для qchart

# Створюємо клас для нашої моделі таблиці
class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = dataw

    # Метод для повернення кількості рядків
    def rowCount(self, parent):
        return len(self._data)

    # Метод для повернення кількості стовпців
    def columnCount(self, parent):
        return len(self._data[0])

    # Метод для повернення значення в комірці
    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

# Створюємо клас для нашого вікна
class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Встановлюємо заголовок вікна
        self.setWindowTitle("Приклад UI з pyside6")

        # Створюємо кнопку для перемикання теми
        self.button = QPushButton("Перемкнути тему")
        self.button.clicked.connect(self.toggle_theme) # Приєднуємо сигнал до слота

        # Створюємо текстове поле
        self.text_edit = QPlainTextEdit()
        self.text_edit.setPlaceholderText("Введіть текст тут")

        # Створюємо таблицю
        self.table_view = QTableView()
        # Створюємо деякі дані для таблиці
        data = [[np.random.randint(0, 100) for _ in range(4)] for _ in range(10)]
        # Встановлюємо модель для таблиці
        self.model = TableModel(data)
        self.table_view.setModel(self.model)

        # Створюємо графік
        self.chart = QChart()
        # Створюємо деякі дані для графіка
        series = QLineSeries()
        series.append(0, 6)
        series.append(2, 4)
        series.append(3, 8)
        series.append(7, 4)
        series.append(10, 5)
        # Додаємо серію до графіка
        self.chart.addSeries(series)
        # Встановлюємо назву графіка
        self.chart.setTitle("Приклад графіка")
        # Створюємо віджет для відображення графіка
        self.chart_view = QChartView(self.chart)

        # Додаємо віджети до вікна
        self.button.setParent(self)
        self.text_edit.setParent(self)
        self.table_view.setParent(self)
        self.chart_view.setParent(self)

        # Встановлюємо початкову тему
        self.theme = "light"
        self.set_theme()

    # Метод для перемикання теми
    def toggle_theme(self):
        # Змінюємо значення теми
        if self.theme == "light":
            self.theme = "dark"
        else:
            self.theme = "light"

        # Встановлюємо тему
        self.set_theme()

    # Метод для встановлення теми
    def set_theme(self):
        # Вибираємо стиль відповідно до теми
        if self.theme == "light":
            style = QStyleFactory.create("Fusion")
        else:
            style = QStyleFactory.create("Windows")

        # Застосовуємо стиль до додатку
        QApplication.setStyle(style)

        # Змінюємо колір фону відповідно до теми
        if self.theme == "light":
            self.setStyleSheet("background-color: white;")
        else:
            self.setStyleSheet("background-color: black;")

        # Змінюємо кольори інтерфейсу відповідно до теми
        palette = QPalette()
        if self.theme == "light":
            # Використовуємо стандартні кольори для світлої теми
            palette = QApplication.palette()
        else:
            # Встановлюємо кольори для темної теми
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)

        # Застосовуємо палітру до додатку
        QApplication.setPalette(palette)

# Створюємо додаток
app = QApplication([])

# Створюємо вікно
window = Window()

# Показуємо вікно
window.show()

# Запускаємо додаток
app.exec_()