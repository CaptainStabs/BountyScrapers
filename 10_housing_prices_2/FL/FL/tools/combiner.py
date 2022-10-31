import os
from tqdm import tqdm

directory = "./DBF/csv/"
l = 0
with open("Parcels.csv", "a", newline="\n") as f:
    for root, dirs, files in os.walk(directory):
            # print(files)
            for file in tqdm(files):
                with open(os.path.join(root, file), "r") as file_input:
                    for i, line in enumerate(file_input):
                        if l: # Only run on first file to get headers
                            if i == 0:
                                continue

                        f.write(line)
                l += 1
