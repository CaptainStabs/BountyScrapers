with open("urls.csv", "r") as f, open("defemaled_urls.csv", "a") as fo:
    for line in f:
        if "female" not in line.lower():
            fo.write(line)
