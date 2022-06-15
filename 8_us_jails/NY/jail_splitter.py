import os

input("PRESS ENTER TO CONTINUE")
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
                f.write(",".join(["jail", "type", "2021-04-01", "2021-05-01", "2021-06-01", "2021-07-01", "2021-08-01", "2021-09-01", "2021-10-01", "2021-11-01", "2021-12-01", "2022-01-01", "2022-02-01", "2022-03-01", "2022-04-01", "delete"]) + "\n")
                for l in lines:
                    if l != ",,,,,,,,,,,,,,,\n":
                        f.write(l)
            lines = []
