import subprocess
import os

from Decompilers.Decompiler import Decompiler

class Jadx(Decompiler):
    def __init__(self, apkPath, outputFolder="/jadx/"):
        super().__init__(apkPath, outputFolder)

    def decompile(self):
        result = subprocess.run(["cmd", "/c", "jadx", self.apkPath, "-d", self.outputFolder], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        #print(result.stdout)
