import polars as pl
import json

f = open("results.json", "r")
data = json.load(f)
f.close()

df = []

for item in data:
    dfAux = pl.DataFrame(
        {
            "Name": [item.get("name")],
            "Label": [item.get("Label")]
        }
    )

    if item.get("Label") == None:
        continue

    if len(df) == 0:
        df = dfAux
    else:
        df.extend(dfAux)

df.write_csv("resultsLabel.csv")
