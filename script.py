import subprocess

import glob

"""
apps = [
    "stopthefire.apk",
    "1_CS_app-debug.apk",
    "2_CS_app-debug.apk",
    "3_CS_app-debug.apk",
    "4_CS_app-debug.apk",
    "5_CS_app-debug.apk",
    "6_CS_app-debug.apk",
    "7_CS_app-debug.apk",
    "arity.apk",
    "btcmap.apk",
    "calculator.apk",
    "challenge1.apk",
    "com.fsck.k9_35009.apk",
    "com.simondalvai.ball2box_44.apk",
    "fastnfitness.apk",
    "husky.apk",
    "omweather.apk",
    "org.woheller69.omweather_13.apk",
    "pinball.apk",
    "qwotable.apk"
]
"""

"""
apps = [
    "1_CS_app-debug.apk",
    "2_CS_app-debug.apk",
    "3_CS_app-debug.apk",
    "4_CS_app-debug.apk",
    "5_CS_app-debug.apk",
    "6_CS_app-debug.apk",
    "7_CS_app-debug.apk",
]
"""

#apps = glob.glob("testApks/Connectivity/*.apk")
apps = glob.glob("testApks/*/*.apk")

size = len(apps)

for i, app in enumerate(apps):
    print(f"Analyzing {app}...")
    print(f"[{i+1} of {size}]")
    result = subprocess.run(["cmd", "/c", "python", "main.py", f"{app}"])
