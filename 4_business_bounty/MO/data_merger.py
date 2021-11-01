import csv
from tqdm import tqdm

with open("mt_merged_data.csv", "a", newline="", encoding="utf-8") as output_file:
    for i in range(3):
        with open(f"./files/mt_{i}.csv", "r", encoding="utf-8") as csv_file:

            for i, line in enumerate(csv_file):
                if i == 0:
                    continue

                output_file.write(str(line))
