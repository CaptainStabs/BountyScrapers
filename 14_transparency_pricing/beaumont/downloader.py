import requests
from tqdm import tqdm

with open("aurorahealthcare.csv", "r") as f:
    for line in tqdm(f):
        line = line.replace("\n", "").replace('"',"")
        url = line.split(',')[-1]
        filename = url.split('/')[-1]

        r = requests.get(url)
        with open("input_files\\" + filename, "wb") as f:
            f.write(r.content)
