import os
from tqdm import tqdm
import argparse

directory = ("./input_files/")
output_dir = "./fixed/"
def cdm_extractor(file_name, line_num):
    with open(f"./input_files/{file_name}", "r") as f:
        with open(f"C:\\Users\\adria\\github\\BountyScrapers\\7_hospital_prices\\banner\\input_files\\cdm\\{file_name.replace('.csv', '')}_cdm.csv", "a") as out_f:
            lines_till_safe = 4
            for i, line in enumerate(f):
                if i >= line_num+4:
                    if 'Code",Price' in line:
                        out_f.write('Charge Description,CDM CPT Code,Price\n')
                    else:
                        out_f.write(line)

def header_fixer(directory, output_dir, header, lines_to_header, fix_header=False):
    for file in tqdm(os.listdir(directory)):
        # print(os.path.join(directory, file))
        if "cdm" not in file:
            with open(os.path.join(directory, file), "r") as f:
                with open(os.path.join(output_dir, file), "a") as out_f:
                    for i, line in enumerate(f):
                        if "Charge Description Master" in line:
                            cdm_extractor(file, i)
                            break
                        else:
                            out_f.write(line)


header_fixer(directory, output_dir, 1, 4)
