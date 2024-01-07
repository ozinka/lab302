from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class TabRun(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        # Create a frame in each tab
        frame_label = QLabel(f'Frame in Tab ')
        self.layout.addWidget(frame_label)

        # Add widgets to the frame
        self.plot_canvas = PlotCanvas(self)
        self.layout.addWidget(self.plot_canvas)

        button = QPushButton(f'Button in Frame ')
        self.layout.addWidget(button)


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        # Plot a simple linear graph
        x = np.linspace(0, 10, 100)
        y = x*x + 3
        self.axes.plot(x, y, label='Linear Graph')

        self.axes.set_title('Simple Linear Plot')
        self.axes.set_xlabel('X-axis')
        self.axes.set_ylabel('Y-axis')
        self.axes.legend()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
