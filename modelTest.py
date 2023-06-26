import polars as pl
import numpy as np
import json

df = pl.read_csv("results.csv")

categoryDfs = df.partition_by("Category")

def computeLabel(value, thresholds):
    for i, threshold in enumerate(thresholds):
        if value <= threshold:
            return len(thresholds)-i+1

    return 1

def makeThresholds(values):
    thresholds = np.percentile(values, np.arange(0, 100, 25))

    return thresholds.tolist()

def defineThresholds(bins):
    bins = np.round(bins*100, 2).tolist()

    sum = 0
    thresholds = []
    for v, p in enumerate(bins):
        sum = sum + p
        if sum >= 20 and len(thresholds) == 0:
            thresholds.append(v)
        elif sum >= 40 and len(thresholds) == 1:
            thresholds.append(v)
        elif sum >= 60 and len(thresholds) == 2:
            thresholds.append(v)
        elif sum >= 80 and len(thresholds) == 3:
            thresholds.append(v)

    return thresholds

def modelTool(categoryDf, categoryName, tool):

    #print(f"---------------- {tool} ----------------")

    values = np.array(categoryDf[tool].to_list())
    sizeOfCode = np.array(categoryDf["Activities"].to_list())

    sortedIdxs = values.argsort()
    sortedValues = values[sortedIdxs]
    sortedSizeOfCode = sizeOfCode[sortedIdxs]

    max = sortedValues.max()
    sumSizeOfCode = np.sum(sortedSizeOfCode)

    v = sortedSizeOfCode / sumSizeOfCode

    bins = np.bincount(sortedValues, weights=v)

    thresholds = makeThresholds(values)
    #print(thresholds)
    classifications = [computeLabel(value, thresholds) for value in values]
    #for n in range(5):
        #print(f"{n+1}: {classifications.count(n+1)}")

    """
    thresholds = defineThresholds(bins)
    print(thresholds)
    classifications = [computeLabel(value, thresholds) for value in values]
    for n in range(5):
        print(f"{n+1}: {classifications.count(n+1)}")
    """

    f = open(f"thresholds2/{categoryName}_{tool}.json", "w")
    data = {"thresholds": thresholds}
    f.write(json.dumps(data))
    f.close()

for categoryDf in categoryDfs:
    categoryName = pl.first(categoryDf["Category"])
    apps = pl.count(categoryDf["Name"])

    modelTool(categoryDf, categoryName, "Earmo")
    modelTool(categoryDf, categoryName, "Kadabra")
    modelTool(categoryDf, categoryName, "Permissions")
    modelTool(categoryDf, categoryName, "Lint")
    modelTool(categoryDf, categoryName, "ADoctor")
    modelTool(categoryDf, categoryName, "Paprika")
    modelTool(categoryDf, categoryName, "Relda2")
