import csv
from tqdm import tqdm
import traceback as tb
import os

in_directory = "./downloads/"
for file in tqdm(os.listdir(in_directory)):
    with open(os.path.join(in_directory, file), "r") as in_f:
        with open("./fixed/" + file, "a") as out_f:
            for line in tqdm(in_f):
                if str(line).strip():
                    out_f.write(line)
