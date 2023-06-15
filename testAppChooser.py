import json
import random

def chooseApps(category, categoryFile):
    f = open(categoryFile, "r")
    currentApps = json.load(f)
    f.close()

    currentApps = [app.get("name") for app in currentApps]

    f = open(f"fdroidApps.json", "r")
    data = json.load(f)
    f.close()

    allApps = data[category]

    notInCurrentApps = [app for app in allApps if app not in currentApps]

    chosenApps = []
    for _ in range(40):
        app = random.choice(notInCurrentApps)
        chosenApps.append(app)
        notInCurrentApps.remove(app)

    currentApps = currentApps + chosenApps

    data = [{"name": app} for app in currentApps]

    f = open(categoryFile, "w")
    f.write(json.dumps(data))
    f.close()

chooseApps("Connectivity", "testApks/connectivity.json")
chooseApps("Development", "testApks/development.json")
chooseApps("Games", "testApks/games.json")
chooseApps("Graphics", "testApks/graphics.json")
chooseApps("Internet", "testApks/internet.json")
chooseApps("Money", "testApks/money.json")
chooseApps("Multimedia", "testApks/multimedia.json")
chooseApps("Navigation", "testApks/navigation.json")
chooseApps("Phone and SMS", "testApks/phoneandsms.json")
chooseApps("Reading", "testApks/reading.json")
chooseApps("Science and Education", "testApks/scienceandeducation.json")
chooseApps("Security", "testApks/security.json")
chooseApps("Sports and Health", "testApks/sportsandhealth.json")
chooseApps("System", "testApks/system.json")
chooseApps("Theming", "testApks/theming.json")
chooseApps("Time", "testApks/time.json")
chooseApps("Writing", "testApks/writing.json")
