
data = {}
with open("t.txt", "r") as f:
    for line in f:
        if "commit" in line:
