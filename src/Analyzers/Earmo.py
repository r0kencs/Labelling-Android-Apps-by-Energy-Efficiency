from src.Analyzers.Analyzer import Analyzer

from src.EnergyAntiPatterns.EnergyAntiPattern import EnergyAntiPattern

from src.EnergyAntiPatterns.BindingResources2Early import BindingResources2Early
from src.EnergyAntiPatterns.Blob import Blob
from src.EnergyAntiPatterns.HashMapUsage import HashMapUsage
from src.EnergyAntiPatterns.InlineGetterAndSetters import InlineGetterAndSetters
from src.EnergyAntiPatterns.LargeClassLowCohesion import LargeClassLowCohesion
from src.EnergyAntiPatterns.LazyClass import LazyClass
from src.EnergyAntiPatterns.LongParameterList import LongParameterList
from src.EnergyAntiPatterns.RefusedParentBequest import RefusedParentBequest
from src.EnergyAntiPatterns.ReleasingResources2Late import ReleasingResources2Late
from src.EnergyAntiPatterns.SpaghettiCode import SpaghettiCode
from src.EnergyAntiPatterns.SpeculativeGenerality import SpeculativeGenerality

from src.EnergyAntiPatterns.UnknownAntiPattern import UnknownAntiPattern

import subprocess
import os
import shutil
import glob

class Earmo(Analyzer):
    def __init__(self, apkName, path):
        super().__init__(apkName, path)

        self.outputPath = "output/" + self.apkName + "/earmo/"

        if not os.path.exists(self.outputPath):
            os.makedirs(self.outputPath)

        self.antiPatternTypes = {
            "BindingResources2Early": BindingResources2Early,
            "Blob": Blob,
            "HashMapUsage": HashMapUsage,
            "InlineGetterAndSetters": InlineGetterAndSetters,
            "LargeClassLowCohesion": LargeClassLowCohesion,
            "LazyClass": LazyClass,
            "LongParameterList": LongParameterList,
            "RefusedParentBequest": RefusedParentBequest,
            "ReleasingResources2Late": ReleasingResources2Late,
            "SpaghettiCode": SpaghettiCode,
            "SpeculativeGenerality": SpeculativeGenerality
        }

        self.patterns = []

    def analyze(self):
        if not os.path.exists(f"{self.outputPath}logs/"):
            os.makedirs(f"{self.outputPath}logs/")
        stdoutFile = open(f"{self.outputPath}logs/out.txt", "w+")
        stderrFile = open(f"{self.outputPath}logs/err.txt", "w+")

        self.prepare()
        os.chdir("tools/earmo")
        #result = subprocess.run(["cmd", "/c", "java", "-jar", "RefactoringStandarStudyAndroid.jar", "../../output/" + self.apkName + "/earmo/conf.prop"], stdout=stdoutFile, stderr=stderrFile)
        self.extractResults()
        self.clean()
        os.chdir("../..")

        stdoutFile.close()
        stderrFile.close()

    def toReport(self):
        return f"EARMO: {len(self.patterns)}\n"

    def getResult(self):
        return len(self.patterns)

    def getStatus(self):
        return self.status

    def extractResults(self):
        patterns = []

        filePatterns = {
            "BindingResources2Early": "DetectionResults in  for BindingResources2Early.ini",
            "Blob": "DetectionResults in  for Blob.ini",
            "HashMapUsage": "DetectionResults in  for HashMapUsageAndroid.ini",
            "InternalGetterAndSetters": "DetectionResults in  for InternalGetterAndSettersAndroid.ini",
            "LargeClassLowCohesion": "DetectionResults in  for LargeClassLowCohesion.ini",
            "LazyClass": "DetectionResults in  for LazyClass.ini",
            "LongParameterList": "DetectionResults in  for LongParameterList.ini",
            "RefusedParentBequest": "DetectionResults in  for RefusedParentBequest.ini",
            "ReleasingResources2Late": "DetectionResults in  for ReleasingResources2Late.ini",
            "SpaghettiCode": "DetectionResults in  for SpaghettiCode.ini",
            "SpeculativeGenerality": "DetectionResults in  for SpeculativeGenerality.ini"
        }

        try:
            for patternName, patternFile in filePatterns.items():
                with open(patternFile) as f:
                    last_line = f.readlines()[-1]
                    n = int(last_line.split(":")[1])
                    for i in range(n):
                        pattern = self.antiPatternTypes.get(patternName, UnknownAntiPattern)()
                        patterns.append(pattern)
            self.status = True
        except Exception as e:
            self.status = False

        self.patterns = patterns

    def clean(self):
        otherFiles = [
            "FUN_MOCell",
            "FUN_NSGAII",
            "IR_MinBound",
            "METHOD_LOC_MaxBound",
            "NMD_NAD_MinBound",
            "NOParam_MaxBound",
            "refactoringList-.txt"
        ]

        files = glob.glob("*.ini")
        for file in files:
            os.remove(file)

        files = glob.glob("*.ser")
        for file in files:
            os.remove(file)

        files = glob.glob("FitnessReport*.txt")
        for file in files:
            os.remove(file)

        for file in otherFiles:
            if os.path.exists(file):
                os.remove(file)

    def prepare(self):
        f = open("output/" + self.apkName + "/earmo/conf.prop", "w+")

        confText = [
        "pathProjecttoAnalize = " + "../../" + self.path + "\n",
        "##/CH/ifa/draw\n",
        "populationSize =100\n",
        "maxEvaluations =1000\n",
        "initialSizeRefactoringSequence =0\n",
        "##329\n",
        "crossOverProbability=0.8\n",
        "mutationProbability=0.8\n",
        "maxTimeExecutionMs=0\n",
        "qmood =0\n",
        "\n",
        "#modes 0 class files; 1 java files; 2 jar files\n",
        "generateFromSourceCode=1\n",
        "\n",
        "\n",
        "generateAllRefOpp=1\n",
        "initialcountAntipatterns=1\n",
        "copyRelevantDirs=0\n",
        "#for linux to fix the problem of Wilcoxon R files with wrong path\n",
        "#ResultsTesting/\n",
        "outputDirectory = " + "../../output/" + self.apkName + "/earmo/output/" + "\n",
        "#./ResultsTesting/\n",
        "Trace=1\n",
        "Threads=1\n",
        "initialSizeRefactoringSequencePerc=50\n",
        "independentRuns=3\n",
        "\n",
        "## Joules expresed in double format.  This value has to be >0 if not the Energy usage of an app will be 0\n",
        "\n",
        "originalAppEnergyUsage=21.28127\n",
        "\n",
        "detectedAntipatterns=LargeClassLowCohesion,Blob,RefusedParentBequest,LazyClass,LongParameterList,SpaghettiCode,SpeculativeGenerality,BindingResources2Early,ReleasingResources2Late,InternalGetterAndSettersAndroid,HashMapUsageAndroid\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "#RefusedParentBequest,LazyClass,LongParameterList,SpaghettiCode,LargeClassLowCohesion,Blob,SpeculativeGenerality,BindingResources2Early,ReleasingResources2Late,InternalGetterAndSettersAndroid,HashMapUsageAndroid\n",
        "\n",
        "androidEnergyDeltas=deltas.txt\n"
        ]

        f.writelines(confText)

        f.close()
