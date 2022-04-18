from tqdm import tqdm

total_cells = 0
total_rows = 0
with open("F:\\hospital-price-transparency-v4\\hospital_extracted_data.csv", "r") as f:
    for i, line in tqdm(enumerate(f)):
        if i == 0:
            continue
        total_cells += len(str(",".join(filter(None, [x for x in line.split(",") if x != "\n" and x != ""]))).split(","))
        total_rows += 1

print("Total Rows:", total_rows)
print("Cell edits:", total_cells)
