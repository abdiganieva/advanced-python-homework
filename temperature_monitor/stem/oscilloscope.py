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


class Oscilloscope(QWidget):
    N = 300

    def __init__(self, init_points = None):
        pass  # TODO(Assignment 13)

    def update_data(self, point: Point):
        pass  # TODO(Assignment 13)
