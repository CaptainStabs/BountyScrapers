with open("updated-hospitals0.csv", "r") as f:
    for line in f:
        line = line.split(",")[0]
        print(f"select count(*) from prices where cms_certification_num = {line};")
