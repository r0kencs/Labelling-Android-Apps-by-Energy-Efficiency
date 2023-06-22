import os
import argparse

class GreenalizeParser():
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("path")
        parser.add_argument("-categories", "-c", dest="categories", nargs="+", required=True)
        parser.add_argument("-analyzers", "-a", dest="analyzers", nargs="*", help="list of Analyzers to run", type=str, default=["Earmo", "Kadabra", "AndroidManifestAnalyzer", "Lint", "ADoctor", "Paprika", "Relda2"])
        parser.add_argument("-force", "-f", dest="forceExecution", help="force new execution", action="store_true")
        parser.add_argument("-update", "-u", dest="updateExecution", help="update previous result with new", action="store_true")
        parser.add_argument("-fixCategories", "-fc", dest="fixCategories", help="if there are previous results, only update categories", action="store_true")
        parser.add_argument("-fdroid", dest="fdroidPackageName", help="Package Name of a FDroid App", default=None)
        parser.add_argument("-aptoide", dest="aptoidePackageName", help="Package Name of an Aptoide App", default=None)
        self.parser = parser

        args = parser.parse_args()

        if not os.path.exists(args.path) and args.fdroidPackageName == None and args.aptoidePackageName == None:
            self.parsingError("Apk path does not exist!")

        analyzersNames = ["Earmo", "Kadabra", "AndroidManifestAnalyzer", "Lint", "ADoctor", "Paprika", "Relda2"]
        for analyzer in args.analyzers:
            if analyzer not in analyzersNames:
                self.parsingError(f"{analyzer} is not a valid Analyzer!")

        self.apkPath = args.path
        self.apkName = os.path.splitext(os.path.basename(self.apkPath))[0]
        self.apkCategories = args.categories
        self.analyzers = args.analyzers
        self.forceExecution = args.forceExecution
        self.updateExecution = args.updateExecution
        self.fixCategories = args.fixCategories
        self.fdroidPackageName = args.fdroidPackageName
        self.aptoidePackageName = args.aptoidePackageName

    def parsingError(self, message):
        print(f"GreenalizeParser Error: {message}\n")
        self.parser.print_help()
        exit()

    def getApkPath(self):
        return self.apkPath

    def getApkName(self):
        return self.apkName

    def getApkCategories(self):
        return self.apkCategories

    def getAnalyzers(self):
        return self.analyzers

    def getForceExecution(self):
        return self.forceExecution

    def getUpdateExecution(self):
        return self.updateExecution

    def getFixCategories(self):
        return self.fixCategories

    def getFdroidPackageName(self):
        return self.fdroidPackageName

    def getAptoidPackageName(self):
        return self.aptoidePackageName
