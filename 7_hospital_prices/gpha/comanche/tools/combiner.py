import os
from tqdm import tqdm

input_dir = "./COMANCHE_COUNTY_HOSPITAL/"

with open("comanche_combined.csv", "a") as f:
    for file in tqdm(os.listdir(input_dir)):
        with open(os.path.join(input_dir, file), "r") as f2:
            for line in f2:
                f.write(line)
