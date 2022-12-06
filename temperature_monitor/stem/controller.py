from dataclasses import dataclass
from datetime import datetime

from PySide2.QtCore import QObject, Signal

from .database import Point
from .device import Thermometer


@dataclass
class ControllerConfig:
    period: int = 1000


class ThermometerController(QObject):

    measurement = ...  # TODO(Assignment 12)

    def __init__(self, device: Thermometer, config: ControllerConfig):
        pass  # TODO(Assignment 12)

    def start(self):
        pass  # TODO(Assignment 12)

    def stop(self):
        pass  # TODO(Assignment 12)

