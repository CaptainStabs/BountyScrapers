total_cells = 0
total_rows = 0
with open("extracted_data2.csv", "r") as f:
    for i, line in enumerate(f.readlines()):
        if i == 0:
            continue
        total_cells += len(str(",".join(filter(None, [x for x in line.split(",") if x != "\n"]))).split(","))
        total_rows += 1

print("Total Rows:", total_rows)
print("Cell edits:", total_cells)
