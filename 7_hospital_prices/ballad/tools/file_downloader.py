from tqdm import tqdm
import requests
import csv

with open("files.csv", newline='') as f:
    line_count = len([line for line in f.readlines()]) -1
    f.seek(0)
    reader = csv.reader(f)
    for line in tqdm(reader, total=line_count):
        name, link = line
        print(link)
        # with open("./downloads/" + name.split(" [")[0] + ".txt", "w") as f_out:
        #     f_out.write(requests.get(link.strip("\n")).text)
