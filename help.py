import json

f = open("results.json", "r")
data = json.load(f)
f.close()


for idx, item in enumerate(data):
    data[idx]["name"] = item["name"].rsplit("_", 1)[0]

f = open("results.json", "w")
f.write(json.dumps(data))
f.close()
