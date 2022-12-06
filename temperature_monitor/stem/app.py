import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Union

from PySide2.QtCore import QSettings, QSize
from PySide2.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QApplication, QPushButton
from appdirs import user_config_dir
from dataclasses import dataclass, field
from .config import resolve_config
from .controller import ControllerConfig, ThermometerController
from .database import SqliteConfig, Database
from .device import VirtualThermometer, USBThermometer
from .oscilloscope import OscilloscopeConfig, Oscilloscope


@dataclass
class Config:
    fake_device: bool = False
    logging_level: Union[str, int] = logging.INFO
    sqlite: SqliteConfig = field(default_factory=SqliteConfig)
    controller: ControllerConfig = field(default_factory=ControllerConfig)
    oscilloscope: OscilloscopeConfig = field(default_factory=OscilloscopeConfig)


class RunButton(QPushButton):
    def __init__(self):
        pass  # TODO(Assignment 12)


class Central(QWidget):
    def __init__(self, controller : ThermometerController, database: Database, config: Config):
        pass  # TODO(Assignment 12)


class Main(QMainWindow):

    def __init__(self, controller: ThermometerController, database: Database, config: Config):
        pass  # TODO(Assignment 12)


def run():
    config = resolve_config(Config, "config.yaml",
                            ""  # TODO(Assignment 14)
                            )
    database = Database.create_or_connect_sqlite(config.sqlite)
    # Create the Qt Application
    # TODO(Assignment 12)
    thermometer_factory =  VirtualThermometer if config.fake_device else USBThermometer
    with thermometer_factory() as thermometer:
        controller = ThermometerController(thermometer, config.controller)
        # Create and show the main window
        # TODO(Assignment 12)
        # Run the main Qt loop
        # TODO(Assignment 12)