import subprocess
import os

from src.Decompilers.Decompiler import Decompiler

class Jadx(Decompiler):
    def __init__(self, apkPath, outputFolder="jadx/"):
        super().__init__(apkPath, outputFolder)

    def decompile(self):
        if not os.path.exists(f"{self.outputFolder}logs/"):
            os.makedirs(f"{self.outputFolder}logs/")
        stdoutFile = open(f"{self.outputFolder}logs/out.txt", "w+")
        stderrFile = open(f"{self.outputFolder}logs/err.txt", "w+")
        result = subprocess.run(["cmd", "/c", "jadx", self.apkPath, "-d", self.outputFolder, "-e", "--no-imports"], stdout=stdoutFile, stderr=stderrFile)
        #print(result.stdout)
