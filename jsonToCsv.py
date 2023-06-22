import polars as pl
import json

f = open("results.json", "r")
data = json.load(f)
f.close()

df = []

for item in data:
    for category in item["categories"]:
        if item.get("Classifications") is not None:
            for classification in item.get("Classifications"):
                if classification["Category"] == category:
                    earmoClassification = classification["EarmoClassification"]
                    kadabraClassification = classification["KadabraClassification"]
                    lintClassification = classification["LintClassification"]
                    aDoctorClassification = classification["ADoctorClassification"]
                    paprikaClassification = classification["PaprikaClassification"]
                    relda2Classification = classification["Relda2Classification"]

        dfAux = pl.DataFrame(
            {
                "Name": [item.get("name")],
                "Size": [item.get("size")],
                "Category": [category],
                "Files": [item.get("files")],
                "FilesSize": [item.get("filesSize")],
                "Time": [item.get("time")],

                "Activities": [item.get("Activities")],
                "Permissions": [item.get("Permissions")],
                "Services": [item.get("Services")],
                "Providers": [item.get("Providers")],
                "AndroidManifestAnalyzerTime": [item.get("AndroidManifestAnalyzerTime")],

                "Earmo": [item.get("Earmo")],
                "EarmoTime": [item.get("EarmoTime")],

                "Kadabra": [item.get("Kadabra")],
                "KadabraTime": [item.get("KadabraTime")],

                "Lint": [item.get("Lint")],
                "LintTime": [item.get("LintTime")],

                "ADoctor": [item.get("ADoctor")],
                "ADoctorTime": [item.get("ADoctorTime")],

                "Paprika": [item.get("Paprika")],
                "PaprikaTime": [item.get("PaprikaTime")],

                "Relda2": [item.get("Relda2")],
                "Relda2Time": [item.get("Relda2Time")],

                "EarmoClassification": [earmoClassification],
                "KadabraClassification": [kadabraClassification],
                "LintClassification": [lintClassification],
                "ADoctorClassification": [aDoctorClassification],
                "PaprikaClassification": [paprikaClassification],
                "Relda2Classification": [relda2Classification],

                "FinalClassification": [item.get("FinalClassification")],
                "Label": [item.get("Label")]
            }
        )

        if item.get("Label") == None:
            continue

        if len(df) == 0:
            df = dfAux
        else:
            df.extend(dfAux)

df.write_csv("results.csv")
