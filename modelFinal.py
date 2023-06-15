import polars as pl
import json

df = pl.read_csv("results.csv")

def makeThresholds(n, mean):
    finalList = []

    for i in range(n):
        percentage = i / n
        value = mean * percentage / 0.50
        finalList.append(value)

    finalList2 = [round(t+1, 2) for t in finalList]

    return finalList2

def computeLabel(value, thresholds):
    for i, threshold in enumerate(thresholds):
        if value < threshold:
            return len(thresholds)-i+1

    return 1

def objectListToList(list, key):
    finalList = []
    for item in list:
        val = item[key]
        finalList.append(val)
    return finalList

df = df.with_columns((((pl.col("EarmoClassification") + pl.col("KadabraClassification") + pl.col("LintClassification") + pl.col("ADoctorClassification") + pl.col("PaprikaClassification") + pl.col("Relda2Classification")) / 6).round(2)).alias("FinalClassification"))

apps = pl.count(df["Name"])

max = df.max()
min = df.min()

sum = pl.sum(df.get_column("FinalClassification"))
min = min.select(pl.col("FinalClassification")).item()
max = max.select(pl.col("FinalClassification")).item()
mean = sum / apps

#print(f"Mean: {mean}")
#print(f"Min: {min}")
#print(f"Max: {max}")

thresholds = makeThresholds(7, mean-1)

f = open(f"thresholds/labels.json", "w")
data = {"thresholds": thresholds}
f.write(json.dumps(data))
f.close()
