import subprocess
import os
import shutil
import glob

from pathlib import Path

from src.Decompilers.Decompiler import Decompiler

class Jadx(Decompiler):
    def __init__(self, apkPath, outputFolder="jadx/"):
        super().__init__(apkPath, outputFolder)

    def decompile(self):
        if not os.path.exists(f"{self.outputFolder}logs/"):
            os.makedirs(f"{self.outputFolder}logs/")
        stdoutFile = open(f"{self.outputFolder}logs/out.txt", "w+")
        stderrFile = open(f"{self.outputFolder}logs/err.txt", "w+")

        result = subprocess.run(["cmd", "/c", "jadx", self.apkPath, "-d", self.outputFolder, "-j", "8"], stdout=stdoutFile, stderr=stderrFile)

        stdoutFile.close()
        stderrFile.close()

        self.minify()

        self.status = True

    def minify(self):
        if os.path.exists(f"{self.outputFolder}minified") and os.path.isdir(f"{self.outputFolder}minified"):
            shutil.rmtree(f"{self.outputFolder}minified")

        shutil.copytree(f"{self.outputFolder}sources", f"{self.outputFolder}minified")

        ignorePackages = ["android", "androidx", "com/google", "kotlin", "kotlinx", "org/intellij", "org/jetbrains"]

        for ignorePackage in ignorePackages:
            path = f"{self.outputFolder}minified/{ignorePackage}"
            if os.path.exists(path) and os.path.isdir(path):
                shutil.rmtree(path)

        files = glob.glob(f"{self.outputFolder}minified/*/*.java")
        for file in files:
            os.remove(file)

        all_directories = list(os.walk(f"{self.outputFolder}minified"))
        for path, a, b in all_directories:
            if len(os.listdir(path)) == 0:
                shutil.rmtree(path)

    def clean(self):
        if os.path.exists(f"{self.outputFolder}/minified"):
            shutil.rmtree(f"{self.outputFolder}/minified")

        if os.path.exists(f"{self.outputFolder}/resources"):
            shutil.rmtree(f"{self.outputFolder}/resources")

        if os.path.exists(f"{self.outputFolder}/sources"):
            shutil.rmtree(f"{self.outputFolder}/sources")

    def getNumberOfFiles(self):
        files = glob.glob(f"{self.outputFolder}minified/**/*.java", recursive=True)

        return len(files)

    def getSizeOfFiles(self):
        rootDir = Path(f"{self.outputFolder}minified/")
        filesSize = sum(f.stat().st_size for f in rootDir.glob("**/*.java") if f.is_file())
        filesSizeMB = round(filesSize / 1024**2, 2)
        print(f"{filesSize} - {filesSizeMB}")

        return filesSizeMB
