import time
import os
import sys
import shutil
import polars as pl
import numpy as np
from enum import Enum
import requests
import urllib.request

from threading import Thread
from datetime import datetime

from src.GreenalizeParser.GreenalizeParser import GreenalizeParser

from src.ProgressBar.ProgressBar import ProgressBar

from src.Minifiers.ApkMinify import ApkMinify

from src.Decompilers.Dex2jar import Dex2jar
from src.Decompilers.Jadx import Jadx

from src.Analyzers.Earmo import Earmo
from src.Analyzers.Kadabra import Kadabra
from src.Analyzers.AndroidManifestAnalyzer import AndroidManifestAnalyzer
from src.Analyzers.Lint import Lint
from src.Analyzers.ADoctor import ADoctor
from src.Analyzers.Paprika import Paprika
from src.Analyzers.Relda2 import Relda2

from src.AppInfo.AppInfo import AppInfo

from src.Reports.TextReportWriter import TextReportWriter
from src.Reports.JsonReportWriter import JsonReportWriter

from src.Stats.Stats import Stats

import json

class GreenalizeStage(Enum):
    NORMAL = 1
    FIX_CATEGORIES = 2
    COMPLETE = 3
    FORCE = 4

class Greenalize():
    def __init__(self, greenalizeParser):
        self.greenalizeParser = greenalizeParser
        self.status = False

        self.apkPath = self.greenalizeParser.getApkPath()
        self.apkName = self.greenalizeParser.getApkName()
        self.apkCategories = self.greenalizeParser.getApkCategories()

        self.index = -1
        self.loaded = False

    def download(self, fdroidName):
        print("Downloading App...")
        response = requests.get(f"https://f-droid.org/api/v1/packages/{fdroidName}")
        responseJson = response.json()
        #versionCode = responseJson.get("suggestedVersionCode")
        versionCode = responseJson.get("packages")[0].get("versionCode")

        if versionCode == None:
            return False

        try:
            urllib.request.urlretrieve(f"https://f-droid.org/repo/{fdroidName}_{versionCode}.apk", f"testApks/{fdroidName}.apk")
        except Exception as e:
            print(e)
            return False

        return True

    def downloadAptoide(self, aptoideName):
        print("Downloading App...")
        response = requests.get(f"http://ws75.aptoide.com/api/7/apps/search/query={aptoideName}/limit=1")
        responseJson = response.json()
        responsePath = responseJson.get("datalist").get("list")[0].get("file").get("path")

        try:
            urllib.request.urlretrieve(f"{responsePath}", f"testApks/{aptoideName}.apk")
        except Exception as e:
            print(e)
            return False

        return True

    def run(self):

        self.createFolder()

        self.loadResultsDict()
        self.loaded = self.load()
        self.downloaded = False

        if self.greenalizeParser.getForceExecution():
            stage = GreenalizeStage.FORCE
        elif self.loaded:
            stage = GreenalizeStage.FIX_CATEGORIES
        else:
            stage = GreenalizeStage.NORMAL

        fdroidPackageName = self.greenalizeParser.getFdroidPackageName()
        aptoidePackageName = self.greenalizeParser.getAptoidPackageName()

        match stage:
            case GreenalizeStage.NORMAL:
                if fdroidPackageName != None:
                    if not self.download(fdroidPackageName):
                        print("Couldn't download app from FDroid! Aborting!")
                        self.status = True
                        return
                    self.downloaded = True
                elif aptoidePackageName != None:
                    if not self.downloadAptoide(aptoidePackageName):
                        print("Couldn't download app from FDroid! Aborting!")
                        self.status = True
                        return
                    self.downloaded = True

                self.apkSize = round(os.path.getsize(self.apkPath) / 1024**2, 2)

                self.analyze()
                self.computeClassifications()
                self.computeFinalClassification()
                self.computeLabel()
                self.save()

            case GreenalizeStage.FIX_CATEGORIES:
                self.computeClassifications()
                self.computeFinalClassification()
                self.computeLabel()
                self.save()

            case GreenalizeStage.FORCE:
                if fdroidPackageName != None:
                    if not self.download(fdroidPackageName):
                        print("Couldn't download app from FDroid! Aborting!")
                        self.status = True
                        return
                    self.downloaded = True

                self.apkSize = round(os.path.getsize(self.apkPath) / 1024**2, 2)

                self.analyze()
                self.computeClassifications()
                self.computeFinalClassification()
                self.computeLabel()
                self.save()

            case _:
                print("Stage _!")

        if self.downloaded:
            print(f"Deleting Apk...")
            os.remove(f"testApks/{fdroidPackageName}.apk")

        print(f"Classification: {self.finalClassification}")
        print(f"Label: {self.label}")

        self.status = True

    def createFolder(self):
        if not os.path.exists(f"output/{self.apkName}"):
            os.makedirs(f"output/{self.apkName}")

    def parseLoad(self, data):
        self.numberOfFiles = data.get("files")
        self.sizeOfFiles = data.get("filesSize")
        self.time = data.get("time")
        self.apkSize = data.get("size")

        self.permissions = data.get("Permissions")
        self.activities = data.get("Activities")
        self.services = data.get("Services")
        self.providers = data.get("Providers")
        self.androidManifestAnalyzerTime = data.get("AndroidManifestAnalyzerTime")

        self.earmoResult = data.get("Earmo")
        self.earmoTime = data.get("EarmoTime")
        self.kadabraResult = data.get("Kadabra")
        self.kadabraTime = data.get("KadabraTime")
        self.lintResult = data.get("Lint")
        self.lintTime = data.get("LintTime")
        self.aDoctorResult = data.get("ADoctor")
        self.aDoctorTime = data.get("ADoctorTime")
        self.paprikaResult = data.get("Paprika")
        self.paprikaTime = data.get("PaprikaTime")
        self.relda2Result = data.get("Relda2")
        self.relda2Time = data.get("Relda2Time")

        self.classifications = data.get("Classifications")
        self.finalClassification = data.get("FinalClassification")
        self.label = data.get("Label")

        s = set(data["categories"])
        temp = [x for x in self.apkCategories if x not in s]
        self.apkCategories = data["categories"] + temp

    def loadResultsDict(self):
        allResults = open("results.json", "r")
        self.resultsDict = json.load(allResults)
        allResults.close()

    def load(self):
        for idx, item in enumerate(self.resultsDict):
            if item["name"] == self.apkName:
                self.parseLoad(item)
                self.index = idx

                print("Loaded from results dictionary!")

                return True

        if os.path.exists(f"output/{self.apkName}/report.json"):
            report = open("output/" + self.apkName + "/report.json", "r")
            item = json.load(report)
            report.close()

            self.parseLoad(item)

            print("Loaded from report!")

            return True

        return False

    def save(self):
        appData = {
            "name": self.apkName,
            "size": self.apkSize,
            "categories": self.apkCategories,
            "files": self.numberOfFiles,
            "filesSize": self.sizeOfFiles,
            "time": self.time,
            "Permissions": self.permissions,
            "Activities": self.activities,
            "Services": self.services,
            "Providers": self.providers,
            "AndroidManifestAnalyzerTime": self.androidManifestAnalyzerTime,
            "Earmo": self.earmoResult,
            "EarmoTime": self.earmoTime,
            "Kadabra": self.kadabraResult,
            "KadabraTime": self.kadabraTime,
            "Lint": self.lintResult,
            "LintTime": self.lintTime,
            "ADoctor": self.aDoctorResult,
            "ADoctorTime": self.aDoctorTime,
            "Paprika": self.paprikaResult,
            "PaprikaTime": self.paprikaTime,
            "Relda2": self.relda2Result,
            "Relda2Time": self.relda2Time,
            "Classifications": self.classifications,
            "FinalClassification": self.finalClassification,
            "Label": self.label
        }

        report = open("output/" + self.apkName + "/report.json", "w")
        report.write(json.dumps(appData))
        report.close()

        if self.index != -1:
            self.resultsDict[self.index] = appData
        else:
            self.resultsDict.append(appData)

        allResults = open("results.json", "w")
        allResults.write(json.dumps(self.resultsDict))
        allResults.close()

    def decideClassification(self, value, thresholds):
        for i, threshold in enumerate(thresholds):
            if value <= threshold:
                return len(thresholds)-i+1

        return 1

    def computeClassificationsAux(self, category, tool, result):
        f = open(f"thresholds2/{category}_{tool}.json")
        data = json.load(f)
        f.close()
        thresholds = data["thresholds"]
        classification = self.decideClassification(result, thresholds)

        return classification

    def computeClassifications(self):
        classifications = []

        for category in self.apkCategories:
            earmoClassification = self.computeClassificationsAux(category, "Earmo", self.earmoResult)
            kadabraClassification = self.computeClassificationsAux(category, "Kadabra", self.kadabraResult)
            lintClassification = self.computeClassificationsAux(category, "Lint", self.lintResult)
            aDoctorClassification = self.computeClassificationsAux(category, "ADoctor", self.aDoctorResult)
            paprikaClassification = self.computeClassificationsAux(category, "Paprika", self.paprikaResult)
            Relda2Classification = self.computeClassificationsAux(category, "Relda2", self.relda2Result)

            categoryClassifications = {
                "Category": category,
                "EarmoClassification": earmoClassification,
                "KadabraClassification": kadabraClassification,
                "LintClassification": lintClassification,
                "ADoctorClassification": aDoctorClassification,
                "PaprikaClassification": paprikaClassification,
                "Relda2Classification": Relda2Classification
            }

            classifications.append(categoryClassifications)

        self.classifications = classifications

    def computeFinalClassification(self):
        classificationsSum = 0
        categorySum = 0
        for categoryClassifications in self.classifications:
            categorySum = categorySum + 1
            classificationsSum = classificationsSum + categoryClassifications["EarmoClassification"] + categoryClassifications["KadabraClassification"] + categoryClassifications["LintClassification"] + categoryClassifications["ADoctorClassification"] + categoryClassifications["PaprikaClassification"] + categoryClassifications["Relda2Classification"]

        finalClassification = round(classificationsSum / (categorySum * 6), 2)

        self.finalClassification = finalClassification

    def computeLabel(self):
        f = open(f"thresholds/labels.json")
        data = json.load(f)
        f.close()
        thresholds = data["thresholds"]

        c = []
        for classifications in self.classifications:
            c.append(classifications["EarmoClassification"])
            c.append(classifications["KadabraClassification"])
            c.append(classifications["LintClassification"])
            c.append(classifications["ADoctorClassification"])
            c.append(classifications["PaprikaClassification"])
            c.append(classifications["Relda2Classification"])

        value = np.array(c).mean()

        classification = self.decideClassification(value, thresholds)

        labels = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G" }

        self.label = labels.get(classification)

    def analyze(self):
        print("")
        t1 = time.time()

        progressBar = ProgressBar()

        analyzers = self.greenalizeParser.getAnalyzers()

        progressBar.smoothUpdate(20, "Jadx Decompiling APK!")
        task_t1 = time.time()
        jadx = Jadx(self.apkPath)
        jadx.decompile()
        self.numberOfFiles = jadx.getNumberOfFiles()
        self.sizeOfFiles = jadx.getSizeOfFiles()
        task_t2 = time.time() - task_t1
        progressBar.finishMessage(f"Jadx - {task_t2:.2f} s", jadx.getStatus())
        progressBar.smoothUpdate(30, "Jadx Decompiling APK!!")
        self.jadxTime = task_t2

        dex2jarOutputPath = "output/" + self.apkName + "/dex2jar/" + self.apkName + "-dex2jar.jar"
        jadxOutputPath = "output/" + self.apkName + "/jadx/"

        appInfo = AppInfo(self.apkName, self.apkCategories, self.apkSize, self.numberOfFiles)

        progressBar.smoothUpdate(30, "EARMO Analyzing!")
        task_t1 = time.time()
        earmo = Earmo(self.apkName, f"{jadxOutputPath}minified")
        if "Earmo" in analyzers:
            earmo.analyze()
        task_t2 = time.time() - task_t1
        progressBar.finishMessage(f"EARMO - {task_t2:.2f} s", earmo.getStatus())
        progressBar.smoothUpdate(40, "EARMO Analyzing!")
        if "Earmo" in analyzers:
            self.earmoTime = task_t2

        progressBar.smoothUpdate(40, "Kadabra Analyzing!")
        task_t1 = time.time()
        kadabra = Kadabra(self.apkName, f"{jadxOutputPath}minified")
        if "Kadabra" in analyzers:
            kadabra.analyze()
        task_t2 = time.time() - task_t1
        progressBar.finishMessage(f"Kadabra - {task_t2:.2f} s", kadabra.getStatus())
        progressBar.smoothUpdate(50, "Kadabra Analyzing!")
        if "Kadabra" in analyzers:
            self.kadabraTime = task_t2

        progressBar.smoothUpdate(50, "AndroidManifestAnalyzer Analyzing!")
        task_t1 = time.time()
        androidManifestAnalyzer = AndroidManifestAnalyzer(self.apkName, jadxOutputPath)
        if "AndroidManifestAnalyzer" in analyzers:
            androidManifestAnalyzer.analyze()
        task_t2 = time.time() - task_t1
        progressBar.finishMessage(f"AndroidManifestAnalyzer - {task_t2:.2f} s", androidManifestAnalyzer.getStatus())
        progressBar.smoothUpdate(60, "AndroidManifestAnalyzer Analyzing!")
        if "AndroidManifestAnalyzer" in analyzers:
            self.androidManifestAnalyzerTime = task_t2

        progressBar.smoothUpdate(60, "Lint Analyzing!")
        task_t1 = time.time()
        lint = Lint(self.apkName, jadxOutputPath)
        if "Lint" in analyzers:
            lint.analyze()
        task_t2 = time.time() - task_t1
        progressBar.finishMessage(f"Lint - {task_t2:.2f} s", lint.getStatus())
        progressBar.smoothUpdate(70, "Lint Analyzing!")
        if "Lint" in analyzers:
            self.lintTime = task_t2

        progressBar.smoothUpdate(70, "aDoctor Analyzing!")
        task_t1 = time.time()
        aDoctor = ADoctor(self.apkName, f"{jadxOutputPath}minified")
        if "ADoctor" in analyzers:
            aDoctor.analyze()
        task_t2 = time.time() - task_t1
        progressBar.finishMessage(f"aDoctor - {task_t2:.2f} s", aDoctor.getStatus())
        progressBar.smoothUpdate(80, "aDoctor Analyzing!")
        if "ADoctor" in analyzers:
            self.aDoctorTime = task_t2

        progressBar.smoothUpdate(80, "Paprika Analyzing!")
        task_t1 = time.time()
        paprika = Paprika(self.apkName, self.apkPath)
        if "Paprika" in analyzers:
            paprika.analyze()
        task_t2 = time.time() - task_t1
        progressBar.finishMessage(f"Paprika - {task_t2:.2f} s", paprika.getStatus())
        progressBar.smoothUpdate(90, "Paprika Analyzing!")
        if "Paprika" in analyzers:
            self.paprikaTime = task_t2

        progressBar.smoothUpdate(90, "Relda2 Analyzing!")
        task_t1 = time.time()
        relda2 = Relda2(self.apkName, self.apkPath)
        if "Relda2" in analyzers:
            relda2.analyze()
        task_t2 = time.time() - task_t1
        progressBar.finishMessage(f"Relda2 - {task_t2:.2f} s", relda2.getStatus())
        progressBar.smoothUpdate(100, "Relda2 Analyzing!")
        if "Relda2" in analyzers:
            self.relda2Time = task_t2

        jadx.clean()

        t2 = time.time() - t1
        print(f"\n\nElapsed time: {t2:.2f} s\n")

        appInfo.setTime(t2)

        if analyzers == ["Earmo", "Kadabra", "AndroidManifestAnalyzer", "Lint", "ADoctor", "Paprika", "Relda2"]:
            self.time = t2

        if "Earmo" in analyzers:
            self.earmoResult = earmo.getResult()

        if "Kadabra" in analyzers:
            self.kadabraResult = kadabra.getResult()

        if "Lint" in analyzers:
            self.lintResult = lint.getResult()

        if "ADoctor" in analyzers:
            self.aDoctorResult = aDoctor.getResult()

        if "Paprika" in analyzers:
            self.paprikaResult = paprika.getResult()

        if "Relda2" in analyzers:
            self.relda2Result = relda2.getResult()

        if "AndroidManifestAnalyzer" in analyzers:
            data_aux = androidManifestAnalyzer.getResult()
            self.activities, self.permissions, self.services, self.providers = data_aux["activities"], data_aux["permissions"], data_aux["services"], data_aux["providers"]

        textReportWriter = TextReportWriter(appInfo, androidManifestAnalyzer, earmo, kadabra, lint, aDoctor, paprika, relda2)
        textReportWriter.write()

    def getStatus(self):
        return self.status
