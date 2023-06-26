import polars as pl
import numpy as np
import json

df = pl.read_csv("results.csv")

def computeLabel(value, thresholds):
    for i, threshold in enumerate(thresholds):
        if value <= threshold:
            return i+1

    return 1

def makeThresholds(values):
    thresholds = np.percentile(values, np.arange(14.28, 100, 14.28))

    return thresholds.tolist()

values = np.array(df["FinalClassification"].to_list())

thresholds = makeThresholds(values)

print(values.min())

print(thresholds)

labels = [computeLabel(value, thresholds) for value in values]
for n in range(7):
    print(f"{n+1}: {labels.count(n+1)}")
