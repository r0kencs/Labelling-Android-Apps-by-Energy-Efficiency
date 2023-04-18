import subprocess
import os

from src.Decompilers.Decompiler import Decompiler

class Dex2jar(Decompiler):
    def __init__(self, apkPath, outputFolder="dex2jar/"):
        super().__init__(apkPath, outputFolder)

    def decompile(self):
        if not os.path.exists(f"{self.outputFolder}logs/"):
            os.makedirs(f"{self.outputFolder}logs/")
        stdoutFile = open(f"{self.outputFolder}logs/out.txt", "w+")
        stderrFile = open(f"{self.outputFolder}logs/err.txt", "w+")

        result = subprocess.run(["cmd", "/c", "d2j-dex2jar", self.apkPath, "-o", self.outputFolder+self.apkName+"-dex2jar.jar", "-f"], stdout=stdoutFile, stderr=stderrFile)

        stdoutFile.close()
        stderrFile.close()
