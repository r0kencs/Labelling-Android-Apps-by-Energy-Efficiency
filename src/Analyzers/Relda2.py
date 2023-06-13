from src.Analyzers.Analyzer import Analyzer

import subprocess
import os

from src.EnergyAntiPatterns.EnergyAntiPattern import EnergyAntiPattern

from src.EnergyAntiPatterns.ResourceLeak import ResourceLeak

class Relda2(Analyzer):
    def __init__(self, apkName, path):
        super().__init__(apkName, path)

        self.outputPath = "output/" + self.apkName + "/relda2/"

        if not os.path.exists(self.outputPath):
            os.makedirs(self.outputPath)

        self.patterns = []

    def analyze(self):

        if not os.path.exists(f"{self.outputPath}logs/"):
            os.makedirs(f"{self.outputPath}logs/")
        stdoutFile = open(f"{self.outputPath}logs/out.txt", "w+")
        stderrFile = open(f"{self.outputPath}logs/err.txt", "w+")

        os.chdir("tools/relda2")

        result = subprocess.run(["cmd", "/c", "python2", "Relda2.py", "-r", f"../../{self.outputPath}", f"../../{self.path}"], stdout=stdoutFile, stderr=stderrFile)

        os.chdir("../..")

        self.extractResults()

        stdoutFile.close()
        stderrFile.close()

        self.status = 1

    def toReport(self):
        return f"Relda2: {len(self.patterns)}\n"

    def toJson(self):
        data = { "Relda2": len(self.patterns) }
        return data

    def getResult(self):
        return len(self.patterns)

    def extractResults(self):
        f = open(f"{self.outputPath}{self.apkName}", "r")
        lines = f.readlines()
        f.close()

        totalLeaks = 0
        for line in lines:
            if len(line) > 1:
                aux = line.rstrip().split(" has ")
                if len(aux) == 2:
                    leaksText = aux[1]
                    leaks = int(leaksText.replace(" resource leak(s)", ""))
                    totalLeaks = totalLeaks + leaks

        patterns = []
        for i in range(totalLeaks):
            pattern = ResourceLeak()
            patterns.append(pattern)

        self.patterns = patterns
