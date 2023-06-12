import polars as pl
import json

f = open("results.json", "r")
data = json.load(f)
f.close()

df = []

for item in data:
    for category in item["categories"]:
        dfAux = pl.DataFrame(
            {
                "Name": [item["name"]],
                "Size": [item["size"]],
                "Category": [category],
                "Files": [item["files"]],
                "Time": [item["time"]],

                "Activities": [item["Activities"]],
                "Permissions": [item["Permissions"]],
                "Services": [item["Services"]],
                "Providers": [item["Providers"]],
                "AndroidManifestAnalyzerTime": [item["AndroidManifestAnalyzerTime"]],

                "Earmo": [item["Earmo"]],
                "EarmoTime": [item["EarmoTime"]],

                "Kadabra": [item["Kadabra"]],
                "KadabraTime": [item["KadabraTime"]],

                "Lint": [item["Lint"]],
                "LintTime": [item["LintTime"]],

                "ADoctor": [item["ADoctor"]],
                "ADoctorTime": [item["ADoctorTime"]],

                "Paprika": [item["Paprika"]],
                "PaprikaTime": [item["PaprikaTime"]],

                "Relda2": [item["Relda2"]],
                "Relda2Time": [item["Relda2Time"]]
            }
        )

        if len(df) == 0:
            df = dfAux
        else:
            df.extend(dfAux)

df.write_csv("results.csv")
