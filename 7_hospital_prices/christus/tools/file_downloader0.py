import requests, enlighten
import math
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from tqdm import tqdm
# import heartrate; heartrate.trace(browser=True, daemon=True)

def downloader(filename, url):
    file = f"./input_files/{filename}.json"

    if not os.path.exists(file):
        r = requests.get(url.strip("\n"))
        with open(file, "w", encoding="utf-8") as f:
            f.write(r.text)

if __name__ == "__main__":
    with open("christus_urls.csv", "r") as f:
        with ThreadPoolExecutor(max_workers=2) as executor:
            for line in tqdm(f):
                line = line.split(",")
                # threads.append(executor.submit(downloader, line[0].replace('"', ''), line[1].replace('"', '')))
                downloader(line[0].replace('"', ''), line[1].replace('"', ''))

    # downloader("McKinney","https://www.bswhealth.com/SiteCollectionDocuments/patient-tools/estimate-cost-of-care/75-1037591_BAYLOR%20SCOTT%20&%20WHITE%20%20MEDICAL%20CENTER%20AT%20MCKINNEY_standardcharges.csv", MANAGER)
