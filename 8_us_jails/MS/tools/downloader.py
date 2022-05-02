import requests, enlighten
import math
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from tqdm import tqdm
# import heartrate; heartrate.trace(browser=True, daemon=True)

def downloader(filename, url, manager):
    headers = {
        'User-Agent': 'Mozilla/6.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
        'DNT': '1',
        'Content-Type': 'text/xml; charset=UTF-8',
        'Accept': '*/*',
    }

    file = f"./pdfs/{filename}.pdf"

    if not os.path.exists(file):
        r = requests.get(url.strip("\n"), stream=True, headers=headers)
        c_len = int(r.headers.get('Content-Length', '0')) or None
        with MANAGER.counter(color = 'green', total = c_len and math.ceil(c_len / 2 ** 20), unit = 'MiB', leave = False) as ctr, \
            open(file, 'wb', buffering =  2 ** 24) as f:
            for chunk in r.iter_content(chunk_size=2 ** 20):
                f.write(chunk)
                ctr.update()


if __name__ == "__main__":
    threads = []
    MANAGER = enlighten.get_manager()
    with open("urls.csv", "r") as f:
        with ThreadPoolExecutor(max_workers=5) as executor:
            for line in f:
                line = line.split(",")
                # threads.append(executor.submit(downloader, line[0].replace('"', ''), line[1].replace('"', ''), MANAGER))
                downloader(line[0].replace('"', ''), line[1].replace('"', ''), MANAGER)

    # downloader("McKinney","https://www.bswhealth.com/SiteCollectionDocuments/patient-tools/estimate-cost-of-care/75-1037591_BAYLOR%20SCOTT%20&%20WHITE%20%20MEDICAL%20CENTER%20AT%20MCKINNEY_standardcharges.csv", MANAGER)
