with open("nums.txt", "r") as f:
    lines = []
    for line in f:
        line = line.strip("\n")
        # print(f"delete from prices where cms_certification_num = '{line}';")
        lines.append(line)

    print(lines)
