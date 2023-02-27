import os

from abc import ABC, abstractmethod

class EnergyAntiPattern(ABC):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
