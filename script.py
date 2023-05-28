import subprocess

import glob
from itertools import chain
from itertools import zip_longest

from datetime import datetime

def twolists(*lists):
    return [x for x in chain.from_iterable(zip_longest(*lists)) if x is not None]

apps_connectivity = glob.glob("testApks/Connectivity/*.apk")
apps_development = glob.glob("testApks/Development/*.apk")
apps_games = glob.glob("testApks/Games/*.apk")
apps_graphics = glob.glob("testApks/Graphics/*.apk")
apps_internet = glob.glob("testApks/Internet/*.apk")
apps_money = glob.glob("testApks/Money/*.apk")
apps_multimedia = glob.glob("testApks/Multimedia/*.apk")
apps_navigation = glob.glob("testApks/Navigation/*.apk")
apps_phoneAndSms = glob.glob("testApks/Phone and SMS/*.apk")
apps_reading = glob.glob("testApks/Reading/*.apk")
apps_scienceAndEducation = glob.glob("testApks/Science and Education/*.apk")
apps_security = glob.glob("testApks/Security/*.apk")
apps_sportsAndHealth = glob.glob("testApks/Sports and Health/*.apk")
apps_system = glob.glob("testApks/System/*.apk")
apps_theming = glob.glob("testApks/Theming/*.apk")
apps_time = glob.glob("testApks/Time/*.apk")
apps_writing = glob.glob("testApks/Writing/*.apk")

apps = twolists(apps_connectivity, apps_development, apps_games, apps_graphics, apps_internet, apps_money,
apps_multimedia, apps_navigation, apps_phoneAndSms, apps_reading, apps_scienceAndEducation, apps_security,
apps_sportsAndHealth, apps_system, apps_theming, apps_time, apps_writing)

size = len(apps)

for i, app in enumerate(apps):
    appName = app.split("\\")[-1]
    category = app.split("\\")[0].split("/")[-1]

    now = datetime.now()
    currentTime = now.strftime("%H:%M:%S")

    print(f"Analyzing {appName}...")
    print(f"Category: {category}\tStart Time: {currentTime}")
    print(f"[{i+1} of {size}]")
    result = subprocess.run(["cmd", "/c", "python", "main.py", f"{app}", f"{category}"])
