import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_complete


def download_file(url):
    headers = {'Cookie': 'ApplicationGatewayAffinity=28d3f836d72c113f3c64ba238c7a7bbf4d64bf76b299fd91f5fc559d5a278bd6; ApplicationGatewayAffinityCORS=28d3f836d72c113f3c64ba238c7a7bbf4d64bf76b299fd91f5fc559d5a278bd6'}
    hash = url.split('/')[-1].strip('"')
    url = f"https://apim.services.craneware.com/api-pricing-transparency/api/public/{hash}/metadata/cdmFile"
    file = requests.get(url, headers=headers)
    filename = file.text["fileDownloadName"]

    with open(f"./input_files/{filename}.csv", 'w') as f:
        f.write(file.text["contentBytes"].decode('utf-8'))


if __name__ == "__main__":
   threads = []
   with open("banner_urls.csv", "r") as f:
       with ThreadPoolExecutor(max_workers=10) as executor:
        for row in tqdm(f):
            url = row.strip().split(",")[1]
            threads.append(executor.submit(download_file, url))

