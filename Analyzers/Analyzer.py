from abc import ABC, abstractmethod

class Analyzer(ABC):
    def __init__(self, path):
        self.path = path

    @abstractmethod
    def analyze(self):
        print("@Analyzer analyzing...")
