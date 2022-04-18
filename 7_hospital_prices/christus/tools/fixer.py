import os
from tqdm import tqdm
import hashlib
bad_lines = ['ef53f621c23bd26a02cd92754e9dfcd1', 'd41d8cd98f00b204e9800998ecf8427e', 'd10723dae9f0fce5dc71af6ad7ccf2f9', '3b095dcfd7860f9cec8c6b5bf2705805', '14b732107c41d943add0629db6f22090', '58ba75136a636fe379632f45e50ee584']
directory = ("./input_files/")
output_dir = "./output_files/"
def header_fixer(directory, output_dir):
    for file in tqdm(os.listdir(directory)):
        # print(os.path.join(directory, file))
        with open(os.path.join(directory, file), "r", encoding="iso-8859-1") as f:
            with open(os.path.join(output_dir, file), "ab") as out_f:
                for line in f:
                    line_hash = hashlib.md5(line.strip().encode('iso-8859-1', "ignore"))
                    if line == "":
                        continue
                    elif not any(line_hash.hexdigest() in bad_lines for bad_lines in bad_lines):
                        out_f.write(line.encode('iso-8859-1', "ignore"))


header_fixer(directory, output_dir)
