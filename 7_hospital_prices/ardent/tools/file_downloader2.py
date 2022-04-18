from tqdm import tqdm
import requests

with open("hospital_home_source.csv", "r") as f:
    for line in tqdm(f):
        link = line.split(",")[2]
        # print(link)
        with open("./downloads/" + link.split("/")[-1].replace("\n", "").strip(), "w") as f_out:
            f_out.write(requests.get(link.strip("\n")).text)
