import os
import argparse

class GreenalizeParser():
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("path")
        parser.add_argument("category")
        parser.add_argument("-analyzers", "-a", dest="analyzers", nargs="*", help="list of Analyzers to run", type=str, default=["Earmo", "Kadabra", "AndroidManifestAnalyzer", "Lint", "ADoctor", "Paprika", "Relda2"])
        parser.add_argument("-force", "-f", dest="forceExecution", help="force new execution", action="store_true")
        parser.add_argument("-update", "-u", dest="updateExecution", help="update previous result with new", action="store_true")
        self.parser = parser

        args = parser.parse_args()

        if not os.path.exists(args.path):
            self.parsingError("Apk path does not exist!")

        analyzersNames = ["Earmo", "Kadabra", "AndroidManifestAnalyzer", "Lint", "ADoctor", "Paprika", "Relda2"]
        for analyzer in args.analyzers:
            if analyzer not in analyzersNames:
                self.parsingError(f"{analyzer} is not a valid Analyzer!")

        self.apkPath = args.path
        self.apkName = os.path.splitext(os.path.basename(self.apkPath))[0]
        self.apkCategory = args.category
        self.analyzers = args.analyzers

        if os.path.exists(f"output/{self.apkName}/report.json") and not (args.forceExecution or args.updateExecution):
            self.parsingError("Report already exists!")

    def parsingError(self, message):
        print(f"GreenalizeParser Error: {message}\n")
        self.parser.print_help()
        exit()

    def getApkPath(self):
        return self.apkPath

    def getApkName(self):
        return self.apkName

    def getApkCategory(self):
        return self.apkCategory

    def getAnalyzers(self):
        return self.analyzers
