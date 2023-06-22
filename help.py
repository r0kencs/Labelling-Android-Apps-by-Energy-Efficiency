import json

f = open("results.json", "r")
results = json.load(f)
f.close()

f = open("blacklist.json", "r")
blacklist = json.load(f)
f.close()

for item in results:
    for b in blacklist:
        if item.get("name") == b.get("name"):
            print(b.get("name"))
            break
