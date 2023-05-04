from abc import ABC, abstractmethod

class Analyzer(ABC):
    def __init__(self, apkName, path):
        self.apkName = apkName
        self.path = path
        self.status = False

    @abstractmethod
    def analyze(self):
        print("@Analyzer analyzing...")

    def getStatus(self):
        return self.status
