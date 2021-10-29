import csv
from tqdm import tqdm

with open("alabama_merged_data.csv", "a", newline="", encoding="utf-8") as output_file:
    for i in range(1, 6):
        with open(f"alabama{i}.csv", "r", encoding="utf-8") as csv_file:

            for i, line in enumerate(csv_file):
                if i == 0:
                    continue

                output_file.write(str(line))
