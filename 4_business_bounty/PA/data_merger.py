import csv
from tqdm import tqdm

with open("pa_merged_data.csv", "a", newline="", encoding="utf-8") as output_file:
    for i in range(60):
        with open(f"./files/pa_{i}.csv", "r", encoding="utf-8") as csv_file:

            for i, line in enumerate(csv_file):
                if i == 0:
                    continue

                output_file.write(str(line))
