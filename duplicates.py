import json

f = open("results.json", "r")
data = json.load(f)
f.close()

print(len(data))

results = []
for item in data:
    found = False
    for result in results:
        if item.get("name") == result.get("name"):
            found = True
            break

    if not found:
        results.append(item)

print(len(results))


"""
f = open("results.json", "w")
f.write(json.dumps(results))
f.close()
"""
