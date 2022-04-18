import requests
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
from base64 import b64decode

def download_file(url):
    hash = url.split('/')[-1].strip('"')
    url = f"https://apim.services.craneware.com/api-pricing-transparency/api/public/{hash}/metadata/cdmFile"
    file = json.loads(requests.get(url).text)
    try:
        filename = file["fileDownloadName"]
        print(filename)

        with open(f"./input_files/{filename}", 'wb') as f:
            f.write(b64decode(file["contentBytes"]))
        return "Success"
    except KeyError:
        print(file)


if __name__ == "__main__":
    threads = []
    url_list = []
    with open("banner_urls.csv", "r") as f:
        for row in tqdm(f):
            url_list.append(row.strip().split(",")[1])
    
    with ProcessPoolExecutor(max_workers=10) as executor:
        for url in tqdm(url_list):
            threads.append(executor.submit(download_file, url))

        for task in tqdm(as_completed(threads)):
            print(task.result())

