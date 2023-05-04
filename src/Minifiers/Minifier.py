import os

from abc import ABC, abstractmethod

class Minifier(ABC):
    def __init__(self, apkPath):
        self.apkPath = apkPath
        self.apkName = os.path.splitext(os.path.basename(apkPath))[0]

        outputPath = "./output/" + self.apkName + "/minified/"

        if not os.path.exists(outputPath):
            os.makedirs(outputPath)

        self.outputPath = outputPath + self.apkName + ".apk"

        self.status = False

    @abstractmethod
    def minify(self):
        print("@Minifier minifying...")

    def getStatus(self):
        return self.status
