import json

f = open("results.json", "r")
data = json.load(f)
f.close()

lines = []
for result in data:
    name = result.get("name")
    classification = result.get("FinalClassification")
    label = result.get("Label")

    text = f"{name} & {classification} & {label} \\\ \hline\n"
    text = text.replace("_", "\\textunderscore ")

    lines.append(text)

f = open("latex.txt", "w")
f.writelines(lines)
f.close()
