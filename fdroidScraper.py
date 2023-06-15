import requests
from bs4 import BeautifulSoup
import json

def scrapeCategory(baseURL, numberOfPages):
    packages = []

    for page in range(1, numberOfPages+1):
        if page == 1:
            URL = baseURL
        else:
            URL = f"{baseURL}{page}"

        r = requests.get(URL)

        soup = BeautifulSoup(r.content, "html5lib")

        packageHeaders = soup.findAll("a", attrs = {"class": "package-header"})

        for packageHeader in packageHeaders:
            packages.append(packageHeader["href"].split("/")[-2])

    packages = list(dict.fromkeys(packages))

    return packages

data = {
    "Connectivity": scrapeCategory("https://f-droid.org/en/categories/connectivity/", 9),
    "Development": scrapeCategory("https://f-droid.org/en/categories/development/", 6),
    "Games": scrapeCategory("https://f-droid.org/en/categories/games/", 16),
    "Graphics": scrapeCategory("https://f-droid.org/en/categories/graphics/", 3),
    "Internet": scrapeCategory("https://f-droid.org/en/categories/internet/", 24),
    "Money": scrapeCategory("https://f-droid.org/en/categories/money/", 5),
    "Multimedia": scrapeCategory("https://f-droid.org/en/categories/multimedia/", 17),
    "Navigation": scrapeCategory("https://f-droid.org/en/categories/navigation/", 8),
    "Phone and SMS": scrapeCategory("https://f-droid.org/en/categories/phone-sms/", 4),
    "Reading": scrapeCategory("https://f-droid.org/en/categories/reading/", 8),
    "Science and Education": scrapeCategory("https://f-droid.org/en/categories/science-education/", 12),
    "Security": scrapeCategory("https://f-droid.org/en/categories/security/", 8),
    "Sports and Health": scrapeCategory("https://f-droid.org/en/categories/sports-health/", 6),
    "System": scrapeCategory("https://f-droid.org/en/categories/system/", 22),
    "Theming": scrapeCategory("https://f-droid.org/en/categories/theming/", 7),
    "Time": scrapeCategory("https://f-droid.org/en/categories/time/", 8),
    "Writing": scrapeCategory("https://f-droid.org/en/categories/writing/", 9)
}

f = open("fdroidApps.json", "w")
f.write(json.dumps(data))
f.close()
