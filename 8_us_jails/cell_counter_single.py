from tqdm import tqdm
import os

directory = ".\\"
total_rows = 0
total_cells = 0
cell_count = 0
for root, subdirectories, files in os.walk(directory):
    print(files)
    for file in files:
        if file == "extracted_data.csv":
            print(os.path.join(root, file))
            with open(os.path.join(root, file), "r") as f:
                for i, line in enumerate(f.readlines()):
                    if i == 0:
                        continue

                    total_cells += len(str(",".join(filter(None, [x for x in line.split(",") if x != "\n" and x != ""]))).split(","))
                    total_cells += cell_count
                    total_rows += 1
print("Total Rows:", total_rows)
print("Cell edits:", total_cells)
