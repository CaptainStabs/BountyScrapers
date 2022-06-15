import requests
from tqdm import tqdm

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
    'DNT': '1',
    'Content-Type': 'text/xml; charset=UTF-8',
    'Accept': '*/*',
}

with open("urls.csv", "r") as f:
    for line in tqdm(f.readlines()):
        name, url  = line.replace('"', "").strip("\n").split(",")
        with open(f"./pdfs/{name}", "wb") as f:
            f.write(requests.get(url, headers=headers).content)
