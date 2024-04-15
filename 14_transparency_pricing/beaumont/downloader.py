import requests
from tqdm import tqdm

with open("beaumont.csv", "r") as f:
    total = len(f.readlines())
    f.seek(0)
    for line in tqdm(f, total=total):
        line = line.replace("\n", "").replace('"',"")
        url = line
        filename = url.split('/')[-1]

        r = requests.get(url)
        with open("input_files\\" + filename, "wb") as f:
            f.write(r.content)
