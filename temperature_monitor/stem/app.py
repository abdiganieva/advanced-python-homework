import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Union
from PySide2.Qt import Qt
from PySide2.QtCore import QSettings, QSize, QPoint
from PySide2.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QApplication, QPushButton, QDockWidget, QTextEdit
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
    #sqlite: SqliteConfig = field(default_factory=SqliteConfig)
    controller: ControllerConfig = field(default_factory=ControllerConfig)
    oscilloscope: OscilloscopeConfig = field(default_factory=OscilloscopeConfig)



class RunButton(QPushButton):
    def __init__(self, parent, controller : ThermometerController):
        super().__init__(parent)
        self.run = False
        self.update()
        self.clicked.connect(self.onClick)
        self.controller = controller
        
    def onClick(self):
        self.run = not self.run
        if self.run:
            self.controller.start()
        else:
            self.controller.stop()
        self.update()
        logging.info("Button was pressed.")
        
    def update(self):
        self.setText("Run" if self.run else "Stop")
        color = "green" if self.run else "red"
        self.setStyleSheet(f"QPushButton {{ background-color: {color}; }}")

    

class Central(QWidget):
    def __init__(self, parent, controller : ThermometerController, database: Database, config: Config):
        super().__init__(parent)
        button = RunButton(self, controller)


class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        logging.root.addHandler(self)
        self.widget = QTextEdit(parent)
        self.widget.setReadOnly(True)
        
    def emit(self, record):
        msg = self.format(record)
        self.widget.setPlainText(msg)

class Main(QMainWindow):

    def __init__(self, controller: ThermometerController, database: Database, config: Config):
        super().__init__()
        central = Central(self, controller, None, config)
        self.setCentralWidget(central)
        self.setWindowTitle("Serious TEmperature Monitor")
        # Default settings on first run
        self.settings = QSettings('SPC-NPM', 'stem')
        self.resize(self.settings.value("size", QSize(300, 300)))
        self.move(self.settings.value("pos", QPoint(1024, 512)))
        
        dock = QDockWidget("Log", self)
        self.addDockWidget(Qt.TopDockWidgetArea, dock)
        logs = QTextEditLogger(self)
        dock.setWidget(logs.widget)
        toolbar = self.addToolBar('Log')
        toolbar.addAction(dock.toggleViewAction())


    def closeEvent(self, e):
        # Save win geometry
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())

def run():
    config = resolve_config(Config, "config.yaml",
                            ""  # TODO(Assignment 14)
                            )
    #database = Database.create_or_connect_sqlite(config.sqlite)
    # Create the Qt Application
    app = QApplication([])
    thermometer_factory =  VirtualThermometer if config.fake_device else USBThermometer
    with thermometer_factory() as thermometer:
        controller = ThermometerController(thermometer, config.controller)
        # Create and show the main window
        MainWindow = Main(controller, database, config)
        MainWindow.show()
        return app.exec_()
        # Run the main Qt loop
        # TODO(Assignment 12)