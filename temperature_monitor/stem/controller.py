from dataclasses import dataclass
from datetime import datetime

from PySide2.QtCore import QObject, Signal

from .database import Point
from .device import Thermometer
import logging

@dataclass
class ControllerConfig:
    period: int = 1000


class ThermometerController(QObject):

    measurement = Signal(float)

    def __init__(self, device: Thermometer, config: ControllerConfig):
        self.device = device
        self.config = config
        self.timer = QTimer()
        self.timer.timeout.connect(get_measurement)
    
    def get_measurement(self):
        temperature = self.device.get()
        self.measurement.emit(temperature)
        logging.info(temperature)

    def start(self):
        self.timer.start(self.config.period)    

    def stop(self):
        self.timer.stop()

