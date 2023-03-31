import subprocess

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

for app in apps:
    print(f"Analyzing {app}...")
    result = subprocess.run(["cmd", "/c", "python", "main.py", f"apks/{app}"])
