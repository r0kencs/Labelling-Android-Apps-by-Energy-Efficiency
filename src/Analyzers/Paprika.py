from src.Analyzers.Analyzer import Analyzer

import subprocess
import os
import glob
import polars as pl

from src.EnergyAntiPatterns.EnergyAntiPattern import EnergyAntiPattern

from src.EnergyAntiPatterns.HashMapUsage import HashMapUsage
from src.EnergyAntiPatterns.InternalGetterAndSetter import InternalGetterAndSetter
from src.EnergyAntiPatterns.InitOnDraw import InitOnDraw
from src.EnergyAntiPatterns.InvalidateWithoutRect import InvalidateWithoutRect
from src.EnergyAntiPatterns.LeakingInnerClass import LeakingInnerClass
from src.EnergyAntiPatterns.MemberIgnoringMethod import MemberIgnoringMethod
from src.EnergyAntiPatterns.NoLowMemoryResolver import NoLowMemoryResolver
from src.EnergyAntiPatterns.UnsupportedHardwareAcceleration import UnsupportedHardwareAcceleration
from src.EnergyAntiPatterns.UIOverdraw import UIOverdraw

from src.EnergyAntiPatterns.UnknownAntiPattern import UnknownAntiPattern

class Paprika(Analyzer):
    def __init__(self, apkName, path):
        super().__init__(apkName, path)

        self.outputPath = "output/" + self.apkName + "/paprika/"

        if not os.path.exists(self.outputPath):
            os.makedirs(self.outputPath)

        self.antiPatternTypes = {
            "HMU": HashMapUsage,
            "IGS": InternalGetterAndSetter,
            "IOD": InitOnDraw,
            "IWR": InvalidateWithoutRect,
            "LIC": LeakingInnerClass,
            "MIM": MemberIgnoringMethod,
            "NLMR": NoLowMemoryResolver,
            "THI": UnknownAntiPattern,
            "UCS": UnknownAntiPattern,
            "UHA": UnsupportedHardwareAcceleration,
            "UIO": UIOverdraw
        }

        self.patterns = []

    def analyze(self):
        if not os.path.exists(f"{self.outputPath}logs/"):
            os.makedirs(f"{self.outputPath}logs/")
        stdoutFile = open(f"{self.outputPath}logs/out.txt", "w+")
        stderrFile = open(f"{self.outputPath}logs/err.txt", "w+")

        os.chdir(f"{self.outputPath}")
        result = subprocess.run(["cmd", "/c", "java", "-jar", "../../../tools/paprika/paprika.jar", "analyse", "-a", "../../../tools/paprika", "-db", "database", "-n", self.apkName, "-p", self.apkName, "-k", "sha256oftheAPK", "-dev", "mydev", "-cat", "mycat", "-nd", "100", "-d", "2017-01-001 10:23:39.050315", "-r", "1.0", "-s", "1024", "-u", "unsafe mode", f"../../../{self.path}"], stdout=stdoutFile, stderr=stderrFile)
        result = subprocess.run(["cmd", "/c", "java", "-jar", "../../../tools/paprika/paprika.jar", "query", "-db", "database", "-d", "TRUE", "-r", "ALLAP"], stdout=stdoutFile, stderr=stderrFile)
        os.chdir("../../..")

        self.extractResults()

        stdoutFile.close()
        stderrFile.close()

        self.status = 1

    def toReport(self):
        return f"Paprika: {len(self.patterns)}\n"

    def toJson(self):
        data = { "Paprika": len(self.patterns) }
        return data

    def getResult(self):
        return len(self.patterns)

    def extractResults(self):
        patterns = []

        results = glob.glob(f"{self.outputPath}*.csv")
        for r in results:
            patternName = os.path.basename(r).split("_")[-1].split(".")[0]
            pattern = self.antiPatternTypes.get(patternName, UnknownAntiPattern)()

            lzdf = pl.scan_csv(r)
            lzdf.select(pl.count()).collect()
            nr = lzdf.select(pl.count()).collect().item()

            for i in range(nr):
                patterns.append(pattern)

        self.patterns = patterns
