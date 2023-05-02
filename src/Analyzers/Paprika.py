from src.Analyzers.Analyzer import Analyzer

import subprocess
import os

class Paprika(Analyzer):
    def __init__(self, apkName, path):
        super().__init__(apkName, path)

        self.outputPath = "output/" + self.apkName + "/paprika/"

        if not os.path.exists(self.outputPath):
            os.makedirs(self.outputPath)

    def analyze(self):
        if not os.path.exists(f"{self.outputPath}logs/"):
            os.makedirs(f"{self.outputPath}logs/")
        stdoutFile = open(f"{self.outputPath}logs/out.txt", "w+")
        stderrFile = open(f"{self.outputPath}logs/err.txt", "w+")

        result = subprocess.run(["cmd", "/c", "java", "-jar", "tools/paprika/paprika.jar", "analyse", "-a", "tools/paprika", "-db", f"{self.outputPath}/database", "-n", self.apkName, "-p", self.apkName, "-k", "sha256oftheAPK", "-dev", "mydev", "-cat", "mycat", "-nd", "100", "-d", "2017-01-001 10:23:39.050315", "-r", "1.0", "-s", "1024", "-u", "unsafe mode", self.path], stdout=stdoutFile, stderr=stderrFile)

        stdoutFile.close()
        stderrFile.close()
