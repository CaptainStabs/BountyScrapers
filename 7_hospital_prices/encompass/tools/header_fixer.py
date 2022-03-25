from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import os

directory = "./input_files/"
output_dir = "./output_files/"
def header_fixer(directory, output_dir, file, lines_to_header, fix_header=False):
        # print(os.path.join(directory, file))
        with open(os.path.join(directory, file), "r", encoding="utf-8") as f:
            with open(os.path.join(output_dir, file), "a", encoding="utf-8") as out_f:
                for i, line in enumerate(f):
                    if i < int(lines_to_header):
                        continue


                    out_f.write(line.strip('"'))

if __name__ == "__main__":
    threads = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        for file in tqdm(os.listdir(directory)):
            threads.append(executor.submit(header_fixer, directory, output_dir, file, 5, 4))

        for task in tqdm(as_completed(threads)):
            a = "A"
