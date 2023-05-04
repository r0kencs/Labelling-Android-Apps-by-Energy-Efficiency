from src.Analyzers.Analyzer import Analyzer

import subprocess
import os
import shutil

class Lint(Analyzer):
    def __init__(self, apkName, path):
        super().__init__(apkName, path)

        self.outputPath = "output/" + self.apkName + "/lint/"

        if not os.path.exists(self.outputPath):
            os.makedirs(self.outputPath)

    def analyze(self):
        self.prepare()

        if not os.path.exists(f"{self.outputPath}logs/"):
            os.makedirs(f"{self.outputPath}logs/")
        stdoutFile = open(f"{self.outputPath}logs/out.txt", "w+")
        stderrFile = open(f"{self.outputPath}logs/err.txt", "w+")

        result = subprocess.run(["cmd", "/c", "lint", "--resources", f"{self.outputPath}resources", "--sources", f"{self.outputPath}sources", "--lint-rule-jars", "tools/lint/greenchecks.jar", "--xml", f"{self.outputPath}report.xml", f"{self.outputPath}"], stdout=stdoutFile, stderr=stderrFile)

        stdoutFile.close()
        stderrFile.close()

        self.status = True

    def prepare(self):
        shutil.copytree(f"{self.path}minified", f"{self.outputPath}sources")
        shutil.copytree(f"{self.path}resources", f"{self.outputPath}resources")
        shutil.copy2("files/lint.xml", f"{self.outputPath}lint.xml")
