import time

from ProgressBar import ProgressBar

from Decompilers.Dex2jar import Dex2jar
from Decompilers.Jadx import Jadx

from Analyzers.Earmo import Earmo

progressBar = ProgressBar()

apkPath = "apks/com.neumorphic.calculator_1.apk"

progressBar.smoothUpdate(0, "Dex2Jar Decompiling APK!")
dex2jar = Dex2jar(apkPath)
dex2jar.decompile()
progressBar.smoothUpdate(10, "Dex2Jar Decompiling APK!")

progressBar.smoothUpdate(10, "Jadx Decompiling APK!")
jadx = Jadx(apkPath)
jadx.decompile()
progressBar.smoothUpdate(20, "Jadx Decompiling APK!!")

progressBar.smoothUpdate(20, "EARMO Analyzing!")
earmo = Earmo('apks/husky.apk')
earmo.analyze()
progressBar.smoothUpdate(30, "EARMO Analyzing!")
