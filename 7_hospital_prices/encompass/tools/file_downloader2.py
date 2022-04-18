from tqdm import tqdm
import requests

with open("downloads.csv", "r", encoding="utf-8") as f:
    for i, line in tqdm(enumerate(f)):
        if i:
            line = line.split(",")
            link = line[1].replace('"', '')
            print(link)
            with open("./input_files/" + line[0].replace('"', '') + ".csv", "w", encoding="utf-8") as f_out:
                f_out.write(requests.get(link.strip("\n")).text)
