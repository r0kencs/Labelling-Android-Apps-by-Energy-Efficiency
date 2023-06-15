import polars as pl
import numpy as np
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

def reject_outliers(data, m = 2.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else np.zeros(len(d))
    return data[s<m]

df = df.with_columns((((pl.col("EarmoClassification") + pl.col("KadabraClassification") + pl.col("LintClassification") + pl.col("ADoctorClassification") + pl.col("PaprikaClassification") + pl.col("Relda2Classification")) / 6).round(2)).alias("FinalClassification"))

values = np.array(df["FinalClassification"].to_list())

#print(f"Min: {values.min()} Max: {values.max()} Mean: {values.mean()} Median: {np.median(values)}")

thresholds = makeThresholds(7, values.mean()-1)

f = open(f"thresholds/labels.json", "w")
data = {"thresholds": thresholds}
f.write(json.dumps(data))
f.close()
