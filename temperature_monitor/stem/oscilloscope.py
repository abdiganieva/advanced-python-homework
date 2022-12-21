from dataclasses import dataclass
import time

import numpy as np
from PySide2.QtWidgets import QVBoxLayout, QWidget

from matplotlib.backends.backend_qt5agg import (FigureCanvas,  NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

from .database import Point


@dataclass
class OscilloscopeConfig:
    time_delta: int = 15


class Oscilloscope(FigureCanvas):
    N = 300

    def __init__(self):
        super().__init__(Figure(figsize=(20,20)))
        x = np.linspace(0, 10, 100)
        self.autoscale = True
        self.figure.tight_layout()
        self.ax1 = self.figure.add_subplot(2,1,1)
        self.ax2 = self.figure.add_subplot(2,1,2)
        #self._static_ax = self.figure.subplots()
        self.ax1.set_ylabel('Temperature')
        self.ax1.set_xlabel('Time')
        self.ax2.set_ylabel('Counts')
        self.ax2.set_xlabel('Temperature')
        self.ax10 = self.ax1.twinx()
        self.ax20 = self.ax2.twinx()
        self.ax10.set_ylabel('Secondary Y axis', color='g')
        self.ax20.set_ylabel('Secondary Y axis', color='b')
        self.x = np.array([])
        self.y = np.array([])
        self.ax1.plot(self.x, self.y)
        self.ax2.hist([])

    def update_data(self, point: Point):
        self.ax1.cla()
        self.x = np.append(self.x, x)[-self.N:]
        self.y = np.append(self.y, y)[-self.N:]
        self.ax1.plot(self.x, self.y)
        self.ax1.relim()
        self.ax1.autoscale_view()

        self.figure.canvas.draw_idle()

