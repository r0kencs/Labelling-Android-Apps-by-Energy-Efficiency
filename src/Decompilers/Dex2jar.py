import subprocess
import os

from src.Decompilers.Decompiler import Decompiler

class Dex2jar(Decompiler):
    def __init__(self, apkPath, outputFolder="/dex2jar/"):
        super().__init__(apkPath, outputFolder)

    def decompile(self):
        result = subprocess.run(["cmd", "/c", "d2j-dex2jar", self.apkPath, "-o", self.outputFolder+self.apkName+"-dex2jar.jar", "-f"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        #print(result.stdout)
