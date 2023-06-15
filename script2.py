import subprocess

import glob
from itertools import chain
from itertools import zip_longest
import json
import requests
import urllib.request
import os
import time

from datetime import datetime

def addCategory(dict, category):
    for idx, item in enumerate(dict):
        dict[idx]["category"] = category

    return dict

def getData(appName):
    response = requests.get(f"https://f-droid.org/api/v1/packages/{appName}")
    responseJson = response.json()
    versionCode = responseJson["suggestedVersionCode"]

    try:
        urllib.request.urlretrieve(f"https://f-droid.org/repo/{appName}_{versionCode}.apk", f"testApks/{appName}.apk")
    except:
        return False

    return True

def twolists(*lists):
    return [x for x in chain.from_iterable(zip_longest(*lists)) if x is not None]

f = open("testApks/connectivity.json")
data = json.load(f)
f.close()
apps_connectivity = addCategory(data, "Connectivity")

f = open("testApks/development.json")
data = json.load(f)
f.close()
apps_development = addCategory(data, "Development")

f = open("testApks/games.json")
data = json.load(f)
f.close()
apps_games = addCategory(data, "Games")

f = open("testApks/graphics.json")
data = json.load(f)
f.close()
apps_graphics = addCategory(data, "Graphics")

f = open("testApks/internet.json")
data = json.load(f)
f.close()
apps_internet = addCategory(data, "Internet")

f = open("testApks/money.json")
data = json.load(f)
f.close()
apps_money = addCategory(data, "Money")

f = open("testApks/multimedia.json")
data = json.load(f)
f.close()
apps_multimedia = addCategory(data, "Multimedia")

f = open("testApks/navigation.json")
data = json.load(f)
f.close()
apps_navigation = addCategory(data, "Navigation")

f = open("testApks/phoneandsms.json")
data = json.load(f)
f.close()
apps_phoneAndSms = addCategory(data, "Phone and SMS")

f = open("testApks/reading.json")
data = json.load(f)
f.close()
apps_reading = addCategory(data, "Reading")

f = open("testApks/scienceandeducation.json")
data = json.load(f)
f.close()
apps_scienceAndEducation = addCategory(data, "Science and Education")

f = open("testApks/security.json")
data = json.load(f)
f.close()
apps_security = addCategory(data, "Security")

f = open("testApks/sportsandhealth.json")
data = json.load(f)
f.close()
apps_sportsAndHealth = addCategory(data, "Sports and Health")

f = open("testApks/system.json")
data = json.load(f)
f.close()
apps_system = addCategory(data, "System")

f = open("testApks/theming.json")
data = json.load(f)
f.close()
apps_theming = addCategory(data, "Theming")

f = open("testApks/time.json")
data = json.load(f)
f.close()
apps_time = addCategory(data, "Time")

f = open("testApks/writing.json")
data = json.load(f)
f.close()
apps_writing = addCategory(data, "Writing")

apps = twolists(apps_connectivity, apps_development, apps_games, apps_graphics, apps_internet, apps_money,
apps_multimedia, apps_navigation, apps_phoneAndSms, apps_reading, apps_scienceAndEducation, apps_security,
apps_sportsAndHealth, apps_system, apps_theming, apps_time, apps_writing)

size = len(apps)

for i, app in enumerate(apps):

    print(app)

    appName = app["name"]
    category = app["category"]

    now = datetime.now()
    currentTime = now.strftime("%H:%M:%S")

    print(f"Analyzing {appName}...")
    print(f"Category: {category}\tStart Time: {currentTime}")
    print(f"[{i+1} of {size}]")

    print(f"Downloading Apk...")
    if not getData(appName):
        continue

    result = subprocess.run(["cmd", "/c", "python", "main.py", f"testApks/{appName}.apk", "-c", f"{category}"])

    print(f"Deleting Apk...")
    os.remove(f"testApks/{appName}.apk")
