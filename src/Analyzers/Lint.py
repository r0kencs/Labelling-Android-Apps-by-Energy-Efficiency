from src.Analyzers.Analyzer import Analyzer

import subprocess
import os
import shutil
from xml.dom.minidom import parse, parseString

from src.EnergyAntiPatterns.EnergyAntiPattern import EnergyAntiPattern

from src.EnergyAntiPatterns.BluetoothLowEnergy import BluetoothLowEnergy
from src.EnergyAntiPatterns.DarkUI import DarkUI
from src.EnergyAntiPatterns.FusedLocationProvider import FusedLocationProvider
from src.EnergyAntiPatterns.KeepCPUOn import KeepCPUOn
from src.EnergyAntiPatterns.KeepScreenOn import KeepScreenOn
from src.EnergyAntiPatterns.RigidAlarm import RigidAlarm
from src.EnergyAntiPatterns.SensorCoalesce import SensorCoalesce
from src.EnergyAntiPatterns.SensorLeak import SensorLeak
from src.EnergyAntiPatterns.UncompressedDataTransmission import UncompressedDataTransmission

from src.EnergyAntiPatterns.UnknownAntiPattern import UnknownAntiPattern

class Lint(Analyzer):
    def __init__(self, apkName, path):
        super().__init__(apkName, path)

        self.outputPath = "output/" + self.apkName + "/lint/"

        if not os.path.exists(self.outputPath):
            os.makedirs(self.outputPath)

        self.antiPatternTypes = {
            "BluetoothLowEnergy": BluetoothLowEnergy,
            "DarkUI": DarkUI,
            "FusedLocationProvider": FusedLocationProvider,
            "KeepCPUOn": KeepCPUOn,
            "KeepScreenOn": KeepScreenOn,
            "RigidAlarm": RigidAlarm,
            "SensorCoalesce": SensorCoalesce,
            "SensorLeak": SensorLeak,
            "UncompressedDataTransmission": UncompressedDataTransmission
        }

        self.patterns = []

    def analyze(self):
        self.prepare()

        if not os.path.exists(f"{self.outputPath}logs/"):
            os.makedirs(f"{self.outputPath}logs/")
        stdoutFile = open(f"{self.outputPath}logs/out.txt", "w+")
        stderrFile = open(f"{self.outputPath}logs/err.txt", "w+")

        result = subprocess.run(["cmd", "/c", "lint", "--resources", f"{self.outputPath}resources", "--sources", f"{self.outputPath}sources", "--lint-rule-jars", "tools/lint/greenchecks.jar", "--xml", f"{self.outputPath}report.xml", f"{self.outputPath}"], stdout=stdoutFile, stderr=stderrFile)

        self.extractResults()

        stdoutFile.close()
        stderrFile.close()

        self.status = 1

    def toReport(self):
        return f"Lint: {len(self.patterns)}\n"

    def getResult(self):
        return len(self.patterns)

    def prepare(self):
        shutil.copytree(f"{self.path}minified", f"{self.outputPath}sources")
        shutil.copytree(f"{self.path}resources", f"{self.outputPath}resources")
        shutil.copy2("files/lint.xml", f"{self.outputPath}lint.xml")

    def extractResults(self):
        patterns = []

        with open(f"{self.outputPath}report.xml") as file:
            document = parse(file)

            nodes = document.getElementsByTagName('issue')
            for node in nodes:
                pattern = self.antiPatternTypes.get(node.getAttribute("id"), UnknownAntiPattern)()
                patterns.append(pattern)

        self.patterns = patterns
