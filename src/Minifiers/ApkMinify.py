import subprocess
import os

from src.Minifiers.Minifier import Minifier

class ApkMinify(Minifier):
    def __init__(self, apkPath):
        super().__init__(apkPath)

    def minify(self):
        result = subprocess.run(["cmd", "/c", "apkanalyzer", "apk", "summary", self.apkPath], stdout=subprocess.PIPE)

        packageName = "L" + result.stdout.decode("utf-8").split()[0].replace(".", "/")

        result = subprocess.run(["cmd", "/c", "java", "-jar", "tools/ApkMinify/apkMinify.jar", self.apkPath, "-o", self.outputPath, "-p", packageName])

        self.status = True
