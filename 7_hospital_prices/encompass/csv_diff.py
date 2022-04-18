from tqdm import tqdm

input_file2 = "C:\\Users\\adria\\hospital-price-transparency-v3\\stabs.csv"
input_file1 = "C:\\Users\\adria\\hospital-price-transparency-v3\\mysql.csv"
output_path = "./out2.csv"

with open(input_file1, 'r') as t1:
    fileone = set(t1)

with open(input_file2, 'r') as t2, open(output_path, 'w') as outFile:
    for line in tqdm(t2):
        if line.upper() not in fileone:
            outFile.write(line)
