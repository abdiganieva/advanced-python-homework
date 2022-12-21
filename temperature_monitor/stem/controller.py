from dataclasses import dataclass
from datetime import datetime

from PyQt5.QtCore import QObject, pyqtSignal, QTimer

from .database import Point
from .device import Thermometer
import logging

@dataclass
class ControllerConfig:
    period: int = 1000


class ThermometerController(QObject):

    measurement = pyqtSignal(float, float)
   

    def __init__(self, device: Thermometer, config: ControllerConfig):
        self.device = device
        self.config = config
        self.timer = QTimer()
        self.timer.timeout.connect(self.get_measurement)
        self.time = 0
    
    def get_measurement(self):
        self.time += self.config.period
        temperature = self.device.get()
        self.measurement.emit(self.time, temperature)
        logging.info(self.time, temperature)

    def start(self):
        self.timer.start(self.config.period)    

    def stop(self):
        self.timer.stop()

