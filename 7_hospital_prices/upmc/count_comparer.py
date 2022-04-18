with open("updated-hospitals0.csv", "r") as f:
    for line in f:
        if line == "cms_certification_num,Mine,55": continue
        line = line.split(",")
        id = line[0]
        mine = line[1]
        his = line[2]

        if his >= mine:
            print(id)
