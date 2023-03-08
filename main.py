import time
import os

from ProgressBar import ProgressBar

from Minifiers.ApkMinify import ApkMinify

from Decompilers.Dex2jar import Dex2jar
from Decompilers.Jadx import Jadx

from Analyzers.Earmo import Earmo
from Analyzers.Kadabra import Kadabra
from Analyzers.AndroidManifestAnalyzer import AndroidManifestAnalyzer

print("")
t1 = time.time()

progressBar = ProgressBar()

apkPath = "apks/stopthefire.apk"
apkName = os.path.splitext(os.path.basename(apkPath))[0]

progressBar.smoothUpdate(0, "ApkMinify Minifying APK!")
task_t1 = time.time()
apkMinify = ApkMinify(apkPath)
apkMinify.minify();
task_t2 = time.time() - task_t1
progressBar.finishMessage(f"[✓] apkMinify - {task_t2:.2f} s")
progressBar.smoothUpdate(10, "ApkMinify Minifying APK!")

minifiedApkPath = "output/" + apkName + "/minified/" + apkName + ".apk"

progressBar.smoothUpdate(10, "Dex2Jar Decompiling APK!")
task_t1 = time.time()
dex2jar = Dex2jar(minifiedApkPath)
dex2jar.decompile()
task_t2 = time.time() - task_t1
progressBar.finishMessage(f"[✓] Dex2Jar - {task_t2:.2f} s")
progressBar.smoothUpdate(20, "Dex2Jar Decompiling APK!")

progressBar.smoothUpdate(20, "Jadx Decompiling APK!")
task_t1 = time.time()
jadx = Jadx(apkPath)
jadx.decompile()
task_t2 = time.time() - task_t1
progressBar.finishMessage(f"[✓] Jadx - {task_t2:.2f} s")
progressBar.smoothUpdate(30, "Jadx Decompiling APK!!")

dex2jarOutputPath = "output/" + apkName + "/dex2jar/" + apkName + "-dex2jar.jar"
jadxOutputPath = "output/" + apkName + "/jadx/"

progressBar.smoothUpdate(30, "EARMO Analyzing!")
task_t1 = time.time()
earmo = Earmo(apkName, dex2jarOutputPath)
#earmo.analyze()
task_t2 = time.time() - task_t1
progressBar.finishMessage(f"[⨯] EARMO - {task_t2:.2f} s")
progressBar.smoothUpdate(40, "EARMO Analyzing!")

progressBar.smoothUpdate(40, "Kadabra Analyzing!")
task_t1 = time.time()
kadabra = Kadabra(apkName, apkPath)
#kadabra.analyze()
task_t2 = time.time() - task_t1
progressBar.finishMessage(f"[⨯] Kadabra - {task_t2:.2f} s")
progressBar.smoothUpdate(50, "Kadabra Analyzing!")

progressBar.smoothUpdate(50, "AndroidManifestAnalyzer Analyzing!")
task_t1 = time.time()
androidManifestAnalyzer = AndroidManifestAnalyzer(apkName, jadxOutputPath)
androidManifestAnalyzer.analyze()
task_t2 = time.time() - task_t1
progressBar.finishMessage(f"[✓] AndroidManifestAnalyzer - {task_t2:.2f} s")
progressBar.smoothUpdate(60, "AndroidManifestAnalyzer Analyzing!")

t2 = time.time() - t1
print(f"\n\nElapsed time: {t2:.2f} s\n")
