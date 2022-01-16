import os
from tqdm import tqdm

directory = "C:\\Users\\adria\\github\\BountyScrapers\\6_us_housing_prices\\OR\\marion\\files\\"
line_total = 0
for file in tqdm(os.listdir(directory)):
    with open(directory + file, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line_total += 1

    line_total -= 1

print(line_total)
