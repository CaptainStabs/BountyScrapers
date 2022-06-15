import requests, enlighten
import math
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from tqdm import tqdm
import argparse
import sys
# import heartrate; heartrate.trace(browser=True, daemon=True)

def downloader(filename, url, manager, output_path):
    headers = {
        'User-Agent': 'Mozilla/6.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
        'DNT': '1',
        'Content-Type': 'text/xml; charset=UTF-8',
        'Accept': '*/*',
    }
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    file = f"./{output_path}/{filename}.pdf"

    if not os.path.exists(file):
        r = requests.get(url.strip("\n"), stream=True, headers=headers)
        c_len = int(r.headers.get('Content-Length', '0')) or None
        with manager.counter(color = 'green', total = c_len and math.ceil(c_len / 2 ** 20), unit = 'MiB', leave = False) as ctr, \
            open(file, 'wb', buffering =  2 ** 24) as f:
            for chunk in r.iter_content(chunk_size=2 ** 20):
                f.write(chunk)
                ctr.update()
def cli():
    parser = argparse.ArgumentParser(description='Download files from csv list')
    parser.add_argument('--f', type=str, metavar='FILE', help='Path to input CSV')
    parser.add_argument('--op', type=str, default="pdfs", metavar="OUTPUT/PATH", help='Where to save files')
    args = parser.parse_args()
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    threads = []
    MANAGER = enlighten.get_manager()
    with open(args.f, "r") as f:
        with ThreadPoolExecutor(max_workers=5) as executor:
            for line in f:
                line = line.split(",")
                # threads.append(executor.submit(downloader, line[0].replace('"', ''), line[1].replace('"', ''), MANAGER))
                downloader(line[0].replace('"', ''), line[1].replace('"', ''), manager=MANAGER, output_path=args.op)



if __name__ == "__main__":
    cli()
    # parser = argparse.ArgumentParser(description='Download files from csv list')
    # parser.add_argument('--f', type=str, metavar='FILE', help='Path to input CSV')
    # parser.add_argument('--op', type=str, default="pdfs", metavar="OUTPUT/PATH", help='Where to save files')
    # args = parser.parse_args()
    # if len(sys.argv)==1:
    #     parser.print_help(sys.stderr)
    #     sys.exit(1)
    # threads = []
    # MANAGER = enlighten.get_manager()
    # with open(args.f, "r") as f:
    #     with ThreadPoolExecutor(max_workers=5) as executor:
    #         for line in f:
    #             line = line.split(",")
    #             # threads.append(executor.submit(downloader, line[0].replace('"', ''), line[1].replace('"', ''), MANAGER))
    #             downloader(line[0].replace('"', ''), line[1].replace('"', ''), MANAGER, arsg.op)
