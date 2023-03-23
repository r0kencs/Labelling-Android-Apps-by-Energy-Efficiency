import os

from abc import ABC, abstractmethod

class Decompiler(ABC):
    def __init__(self, apkPath, outputFolder):
        self.apkPath = apkPath
        self.apkName = os.path.splitext(os.path.basename(apkPath))[0]

        outputSrc = "./output/" + self.apkName + "/" + outputFolder
        self.outputFolder = outputSrc

    @abstractmethod
    def decompile(self):
        print("@Decompiler decompiling...")
