import os

directory = ".\\"
total_rows = 0
total_cells = 0
for root, subdirectories, files in os.walk(directory):
        for file in files:
            if file == "extracted_data.csv":
                with open(os.path.join(root, file), "r") as f:
                    for i, line in enumerate(f.readlines()):
                        if i == 0:
                            continue

                        cell_count = len(str(",".join(filter(None, line.split(",")))).split(","))
                        total_cells += cell_count
                        total_rows += 1
print("Total Rows:", total_rows)
print("Cell edits:", total_cells)
