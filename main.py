from Decompiler import Decompiler
from ProgressBar import ProgressBar

import time

from Earmo import Earmo

progressBar = ProgressBar()

progressBar.smoothUpdate(0, "Decompiling APK!")
decompiler = Decompiler('apks/stopthefire.apk')
decompiler.decompile()
progressBar.smoothUpdate(10, "Decompiling APK!")

progressBar.smoothUpdate(10, "EARMO Analyzing!")
earmo = Earmo('apks/stopthefire.apk')
earmo.analyze()
progressBar.smoothUpdate(20, "EARMO Analyzing!")
