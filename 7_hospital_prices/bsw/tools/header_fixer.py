import os
from tqdm import tqdm
import argparse

directory = ("./input_files/")
output_dir = "./fixed/"
def header_fixer(directory, output_dir, header, lines_to_header, fix_header=False):
    for file in tqdm(os.listdir(directory)):
        # print(os.path.join(directory, file))
        with open(os.path.join(directory, file), "r") as f:
            with open(os.path.join(output_dir, file), "a") as out_f:
                for i, line in enumerate(f):
                    if i < int(lines_to_header):
                        continue
                    elif i == int(lines_to_header):
                        if fix_header:
                            out_f.write(header)

                    elif "N/A - Data not applicable to specific procedure." in line:
                        break

                    elif ",,,,,,,,,,,,,," in line:
                        continue

                    else:
                        out_f.write(line)

header_fixer(directory, output_dir, 1, 3)

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--directory', type=str)
#     parser.add_argument('--output_dir', type=str)
#     parser.add_argument('--header', type=str)
#     parser.add_argument('--lines_to_header', type=str)
#     # parser.add_argument('fix_header',type=bool, default=True)
#     header_fixer(parser.parse_args())
