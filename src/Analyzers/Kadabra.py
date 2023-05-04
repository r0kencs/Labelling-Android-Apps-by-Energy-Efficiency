from src.Analyzers.Analyzer import Analyzer

from src.EnergyAntiPatterns.EnergyAntiPattern import EnergyAntiPattern
from src.EnergyAntiPatterns.ExcessiveMethodCalls import ExcessiveMethodCalls
from src.EnergyAntiPatterns.HashMapUsage import HashMapUsage
from src.EnergyAntiPatterns.InternalGetter import InternalGetter
from src.EnergyAntiPatterns.MemberIgnoringMethod import MemberIgnoringMethod

from src.EnergyAntiPatterns.UnknownAntiPattern import UnknownAntiPattern

import subprocess
import os
import shutil
import json

class Kadabra(Analyzer):
    def __init__(self, apkName, path):
        super().__init__(apkName, path)

        self.outputPath = "output/" + self.apkName + "/kadabra/"

        if not os.path.exists(self.outputPath):
            os.makedirs(self.outputPath)

        self.antiPatternTypes = {
            "ExcessiveMethodCalls": ExcessiveMethodCalls,
            "HashMapUsage": HashMapUsage,
            "InternalGetter": InternalGetter,
            "MemberIgnoringMethod": MemberIgnoringMethod
        }

        self.patterns = []

    def analyze(self):
        if not os.path.exists(f"{self.outputPath}logs/"):
            os.makedirs(f"{self.outputPath}logs/")
        stdoutFile = open(f"{self.outputPath}logs/out.txt", "w+")
        stderrFile = open(f"{self.outputPath}logs/err.txt", "w+")

        result = subprocess.run(["cmd", "/c", "java", "-jar", "tools/kadabra/kadabra.jar", "tools/kadabra/main.js", "-p", self.path, "-WC", "-APF", "package!", "-o", self.outputPath, "-s", "-X", "-C"], stdout=stdoutFile, stderr=stderrFile)
        self.extractResults()

        stdoutFile.close()
        stderrFile.close()

        self.status = True

    def toReport(self):
        return f"Kadabra: {len(self.patterns)}\n"

    def getResult(self):
        return len(self.patterns)

    def extractResults(self):
        shutil.copy2("tools/kadabra/results.json", self.outputPath)

        patterns = []

        with open(self.outputPath + "results.json", "r") as resultsFile:
            data = json.load(resultsFile)

            for detector in data['detectors']:
                patternType = detector.replace(" ", "").replace("Detector", "")
                patternList = data['detectors'][detector]

                for _ in patternList:
                    pattern = self.antiPatternTypes.get(patternType, UnknownAntiPattern)()
                    patterns.append(pattern)

        self.patterns = patterns
