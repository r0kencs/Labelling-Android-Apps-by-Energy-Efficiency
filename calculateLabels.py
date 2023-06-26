import json

def decideClassification(value, thresholds):
    for i, threshold in enumerate(thresholds):
        if value <= threshold:
            return len(thresholds)-i+1

    return 1

def computeClassificationsAux(category, tool, result):
    f = open(f"thresholds2/{category}_{tool}.json")
    data = json.load(f)
    f.close()
    thresholds = data["thresholds"]
    classification = decideClassification(result, thresholds)

    return classification

def computeClassifications(item):
    classifications = []

    for category in item.get("categories"):
        earmoClassification = computeClassificationsAux(category, "Earmo", item.get("Earmo"))
        kadabraClassification = computeClassificationsAux(category, "Kadabra", item.get("Kadabra"))
        permissionsClassification = computeClassificationsAux(category, "Permissions", item.get("Permissions"))
        lintClassification = computeClassificationsAux(category, "Lint", item.get("Lint"))
        aDoctorClassification = computeClassificationsAux(category, "ADoctor", item.get("ADoctor"))
        paprikaClassification = computeClassificationsAux(category, "Paprika", item.get("Paprika"))
        Relda2Classification = computeClassificationsAux(category, "Relda2", item.get("Relda2"))

        categoryClassifications = {
            "Category": category,
            "EarmoClassification": earmoClassification,
            "KadabraClassification": kadabraClassification,
            "PermissionsClassification": permissionsClassification,
            "LintClassification": lintClassification,
            "ADoctorClassification": aDoctorClassification,
            "PaprikaClassification": paprikaClassification,
            "Relda2Classification": Relda2Classification
        }

        classifications.append(categoryClassifications)

    return classifications

def computeFinalClassification(item):
    classificationsSum = 0
    categorySum = 0
    for categoryClassifications in item.get("Classifications"):
        categorySum = categorySum + 1
        classificationsSum = classificationsSum + categoryClassifications["EarmoClassification"] + categoryClassifications["KadabraClassification"] + categoryClassifications["PermissionsClassification"] + categoryClassifications["LintClassification"] + categoryClassifications["ADoctorClassification"] + categoryClassifications["PaprikaClassification"] + categoryClassifications["Relda2Classification"]

    finalClassification = round(classificationsSum / (categorySum * 7), 2)

    return finalClassification

def computeLabel(item):
    f = open(f"thresholds2/labels.json")
    data = json.load(f)
    f.close()
    thresholds = data["thresholds"]

    classification = decideClassification(item.get("FinalClassification"), thresholds)

    labels = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G" }

    return labels.get(classification)

resultsFile = open("results.json", "r")
results = json.load(resultsFile)
resultsFile.close()

diff = 0

for result in results:
    result["Classifications"] = computeClassifications(result)
    result["FinalClassification"] = computeFinalClassification(result)
    result["Label"] = computeLabel(result)


resultsFile = open("results.json", "w")
resultsFile.write(json.dumps(results))
resultsFile.close()
