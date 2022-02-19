with open("Parcels.csv", "r") as f:
    total = 0
    for i, line in enumerate(f.readlines()):
        if i == 0:
            continue
        total += 1

print(total)
