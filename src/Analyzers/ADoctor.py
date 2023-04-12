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

class ADoctor(Analyzer):
    def __init__(self, apkName, path):
        super().__init__(apkName, path)

        self.outputPath = "output/" + self.apkName + "/aDoctor/"

        self.outputFile = self.outputPath + "results.csv"

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
        result = subprocess.run(["cmd", "/c", "java", "-cp", "tools/aDoctor/aDoctor.jar", "it.unisa.aDoctor.process.RunAndroidSmellDetection", self.path, self.outputFile, "111111111111111"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        #self.extractResults()

    #def extractResults(self):
