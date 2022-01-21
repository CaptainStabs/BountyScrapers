
with open("PARCEL.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])

    print(line_count)

    input_csv.seek(0)

    line_count = 0
    for line in input_csv.readlines():
        line_count += 1

    print(line_count)
