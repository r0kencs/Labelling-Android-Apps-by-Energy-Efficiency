f = open("output/andless/relda2/andless", "r")
#f = open("output/stopthefire/relda2/stopthefire", "r")
lines = f.readlines()
f.close()

totalLeaks = 0
for line in lines:
    if len(line) > 1:
        aux = line.rstrip().split(" has ")
        if len(aux) == 2:
            leaksText = aux[1]
            leaks = int(leaksText.replace(" resource leak(s)", ""))
            totalLeaks = totalLeaks + leaks

print(totalLeaks)
