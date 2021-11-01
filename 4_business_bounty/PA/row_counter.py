import os

dir = "./files/"
total_rows = 0

for root, dirs, files in os.walk(dir):
    for file in files:
        with open(root + file, "r", encoding="utf-8") as input_file:
            line_total = 0
            for line in input_file:
                line_total += 1
            line_total = line_total - 1
            print(line_total)
            total_rows = total_rows + line_total

print(total_rows)
