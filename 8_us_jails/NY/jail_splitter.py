import os

lines = []
with open("tabula-jail_population.csv", "r") as f:
    for i, line in enumerate(f):
        if "jail" in line.lower(): filename = line.split(",")[0]
        if not i:
            header = line

        lines.append(line)
        if line.strip() == ",,,,,,,,,,,,,,,":

            print(filename)
            with open(f"./files/{filename}.csv", "a") as f:
                for l in lines:
                    if l != ",,,,,,,,,,,,,,,\n":
                        f.write(l)
            lines = []
