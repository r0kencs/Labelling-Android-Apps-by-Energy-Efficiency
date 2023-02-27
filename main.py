import time
import os

from ProgressBar import ProgressBar

from Minifiers.ApkMinify import ApkMinify

from Decompilers.Dex2jar import Dex2jar
from Decompilers.Jadx import Jadx

from Analyzers.Earmo import Earmo

progressBar = ProgressBar()

apkPath = "apks/stopthefire.apk"
apkName = os.path.splitext(os.path.basename(apkPath))[0]

progressBar.smoothUpdate(0, "ApkMinify Minifying APK!")
apkMinify = ApkMinify(apkPath)
apkMinify.minify();
progressBar.smoothUpdate(10, "ApkMinify Minifying APK!")

minifiedApkPath = "output/" + apkName + "/minified/" + apkName + ".apk"

progressBar.smoothUpdate(10, "Dex2Jar Decompiling APK!")
dex2jar = Dex2jar(minifiedApkPath)
#dex2jar.decompile()
progressBar.smoothUpdate(20, "Dex2Jar Decompiling APK!")

progressBar.smoothUpdate(20, "Jadx Decompiling APK!")
jadx = Jadx(apkPath)
#jadx.decompile()
progressBar.smoothUpdate(30, "Jadx Decompiling APK!!")

dex2jarOutputPath = "output/" + apkName + "/dex2jar/" + apkName + "-dex2jar.jar"

progressBar.smoothUpdate(30, "EARMO Analyzing!")
earmo = Earmo(apkName, dex2jarOutputPath)
earmo.analyze()
progressBar.smoothUpdate(40, "EARMO Analyzing!")
