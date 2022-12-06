from abc import ABC, abstractmethod

import hid
import numpy as np


class Thermometer(ABC):

    def open(self):
        pass

    def close(self):
        pass

    @abstractmethod
    def get(self) -> float:
        pass

    # TODO(Assignment 12)


class VirtualThermometer(Thermometer):

    def __init__(self, seed = 1):
        self.gen = np.random.RandomState(seed)

    def get(self) -> float:
        return self.gen.poisson(20)


class USBThermometer(Thermometer):

    def __init__(self):
        pass  # TODO(Assignment 15)

    def open(self):
        pass  # TODO(Assignment 15)

    def close(self):
        pass  # TODO(Assignment 15)

    def get(self) -> float:
        pass  # TODO(Assignment 15)
