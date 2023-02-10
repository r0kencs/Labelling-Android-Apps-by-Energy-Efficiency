import subprocess
import os

class Decompiler:
    def __init__(self, apkPath, outputFolder="./output/"):
        self.apkPath = apkPath
        self.apkName = os.path.basename(apkPath).split("/")[-1]
        self.outputFolder = outputFolder

    def decompile(self):
        result = subprocess.run(["cmd", "/c", "d2j-dex2jar", self.apkPath, "-o", self.outputFolder+self.apkName+"-dex2jar.jar", "-f"])
        #print(result.stdout)
        print("|██████████| " + self.apkName + " successfully decompiled!")
