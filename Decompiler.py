import subprocess
import os

from ProgressBar import ProgressBar

class Decompiler:
    def __init__(self, apkPath, outputFolder="./output/"):
        self.apkPath = apkPath
        self.apkName = os.path.splitext(apkPath)[0]
        self.outputFolder = outputFolder

    def decompile(self):
        result = subprocess.run(["cmd", "/c", "d2j-dex2jar", self.apkPath, "-o", self.outputFolder+self.apkName+"-dex2jar.jar", "-f"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        #print(result.stdout)
