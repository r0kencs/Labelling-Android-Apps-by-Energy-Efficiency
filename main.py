import time
import os
import sys
import shutil
import polars as pl


from threading import Thread
from multiprocessing import Process
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

from src.Greenalize.Greenalize import Greenalize

def threadedTimer(p, duration):
    startDate = datetime.now()
    while True:
        currentDate = datetime.now()
        diff = currentDate - startDate
        diffInHours = diff.total_seconds() / 3600

        if not p.is_alive():
            p.terminate()
            p.join()
            return

        if diffInHours >= duration:
            print(f"\n{greenalizeParser.apkName} analysis is taking too long... Aborting!\n")
            if p.is_alive():
                p.terminate()
            p.join()
            return

        time.sleep(1)

def greenalizeTask():
    greenalize.run()

"""
thread = Thread(target = greenalize.run, daemon=True)
thread.start()


"""

greenalizeParser = GreenalizeParser()
greenalize = Greenalize(greenalizeParser)

if __name__ == '__main__':
    p = Process(target=greenalizeTask, name="Greenalize Execution")
    p.start()

    threadedTimer(p, 5)

#greenalize.run()
