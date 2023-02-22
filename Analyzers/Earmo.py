from Analyzers.Analyzer import Analyzer

import subprocess
import os
import shutil

class Earmo(Analyzer):
    def __init__(self, apkName, path):
        super().__init__(apkName, path)

        outputPath = "output/" + self.apkName + "/earmo/"

        if not os.path.exists(outputPath):
            os.makedirs(outputPath)

    def analyze(self):
        self.prepare()
        os.chdir("tools/earmo")
        result = subprocess.run(["cmd", "/c", "java", "-jar", "RefactoringStandarStudyAndroid.jar", "../../output/" + self.apkName + "/earmo/conf.prop"])

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
        "generateFromSourceCode=2\n",
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
        "independentRuns=5\n",
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
