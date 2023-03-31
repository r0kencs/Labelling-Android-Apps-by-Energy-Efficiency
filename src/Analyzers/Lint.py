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
        self.prepare()
        result = subprocess.run(["cmd", "/c", "./gradlew", "lint"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.chdir("../../..")

    def prepare(self):
        os.chdir(self.path)
        result = subprocess.run(["cmd", "/c", "gradle", "wrapper"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
