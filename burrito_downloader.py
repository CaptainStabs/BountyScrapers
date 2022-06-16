import requests, enlighten
import math
import os
from bs4 import BeautifulSoup
import argparse
# import heartrate; heartrate.trace(browser=True, daemon=True)

def downloader(args):
    MANAGER = enlighten.get_manager()
    url = args.url

    html_page = requests.get(url).text
    with open("test.html", "w", encoding="utf-8") as f:
        f.write(html_page)

    soup = BeautifulSoup(html_page, 'html.parser')

    for link in soup.findAll("img"):
        print(link)
        if "ablum" in link:
            print(link)
            file = url.split('/')[-1].replace("\n", "")

            if not os.path.exists(file):
                r = requests.get(url.strip("\n"), stream=True)
                c_len = int(r.headers.get('Content-Length', '0')) or None
                with MANAGER.counter(color = 'green', total = c_len and math.ceil(c_len / 2 ** 20), unit = 'MiB', leave = False) as ctr, \
                    open(file, 'wb', buffering =  2 ** 24) as f:
                    for chunk in r.iter_content(chunk_size=2 ** 20):
                        f.write(chunk)
                        ctr.update()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, required=True)
    args = parser.parse_args()
    downloader(args)
