from src.Analyzers.Analyzer import Analyzer

import subprocess
import os

class Lint(Analyzer):
    def __init__(self, apkName, path):
        super().__init__(apkName, path)

        self.outputPath = "output/" + self.apkName + "/lint/"

        if not os.path.exists(self.outputPath):
            os.makedirs(self.outputPath)

    def analyze(self):
        if not os.path.exists(f"{self.outputPath}logs/"):
            os.makedirs(f"{self.outputPath}logs/")
        stdoutFile = open(f"{self.outputPath}logs/out.txt", "w+")
        stderrFile = open(f"{self.outputPath}logs/err.txt", "w+")

        os.chdir(self.path)
        result = subprocess.run(["cmd", "/c", "gradle", "wrapper"], stdout=stdoutFile, stderr=stderrFile)
        result = subprocess.run(["cmd", "/c", "./gradlew", "lint"], stdout=stdoutFile, stderr=stderrFile)
        os.chdir("../../..")

        stdoutFile.close()
        stderrFile.close()
