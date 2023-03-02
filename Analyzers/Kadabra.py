from Analyzers.Analyzer import Analyzer

from EnergyAntiPatterns.EnergyAntiPattern import EnergyAntiPattern
from EnergyAntiPatterns.ExcessiveMethodCalls import ExcessiveMethodCalls
from EnergyAntiPatterns.HashMapUsage import HashMapUsage
from EnergyAntiPatterns.InternalGetter import InternalGetter
from EnergyAntiPatterns.MemberIgnoringMethod import MemberIgnoringMethod

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

    def analyze(self):
        result = subprocess.run(["cmd", "/c", "java", "-jar", "tools/kadabra/kadabra.jar", "tools/kadabra/main.js", "-p", self.path, "-WC", "-APF", "package!", "-o", self.outputPath, "-s", "-X", "-C"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.extractResults()

    def extractResults(self):
        shutil.copy2("tools/kadabra/results.json", self.outputPath)

        patterns = []

        with open(self.outputPath + "results.json", "r") as resultsFile:
            data = json.load(resultsFile)

            for detector in data['detectors']:
                patternType = detector.replace(" ", "").replace("Detector", "")
                patternList = data['detectors'][detector]

                for _ in patternList:
                    pattern = self.antiPatternTypes.get(patternType)()
                    patterns.append(pattern)

        self.patterns = patterns
