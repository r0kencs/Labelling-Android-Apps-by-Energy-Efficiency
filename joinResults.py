import json

"""
f = open("results.json", "r")
results = json.load(f)
f.close()

f = open("results3.json", "r")
results3 = json.load(f)
f.close()

for item in results3:
    found = False
    for idx, result in enumerate(results):
        if item.get("name") == result.get("name"):
            s = set(result["categories"])
            temp = [x for x in item.get("categories") if x not in s]
            results[idx]["categories"] = result["categories"] + temp
            found = True
            break
    if not found:
        results.append(item)

f = open("resultsFinal.json", "w")
f.write(json.dumps(results))
f.close()
