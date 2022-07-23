import sys
import os
import traceback as tb
from multiprocessing import Pool, Manager
from pathlib import Path
import json
import math
from scraper_single import scraper

p = Path(__file__).resolve().parents[1]
sys.path.insert(1, str(p))
from _common import get_last_id
from _common.send_mail import send_mail

# 1997739
if __name__ == "__main__":
    threads = 32
    end = 3000000
    end_const = math.ceil(end/threads)
    lock = Manager().Lock()
    with open("museums.json", "r", encoding="utf-8") as f:
        mms = json.load(f)

    if not os.path.exists("./files/"):
        os.makedirs("./files/")
    arguments = []

    end_id = end_const #45899
    # start_num is supplemental for first run and is only used if the files don't exist
    for i in range(threads):
        if i == 0:
            start_num = 1997739
        else:
            # Use end_id before it is added to
            start_num = end_id - end_const
        print("Startnum: " + str(start_num))
        arguments.append([f"./files/extracted_data{i}.csv", start_num, end_id, i, lock, mms])
        end_id = end_id + end_const
    # print(arguments)
    # print("\n")

    try:
        pool = Pool(processes=len(arguments))
        pool.starmap(scraper, arguments)
        # for _ in tqdm(pool.istarmap(scraper, arguments), total=len(arguments)):
        #     pass
        pool.close()
        send_mail("Finished", "Finished")
        # pool.starmap(scraper, arguments), total=len(arguments)
    except KeyboardInterrupt:
        print("Quitting")
        pool.terminate()
        sys.exit()
    except Exception:
        tb.print_exc()
        pool.terminate()
        raise
    finally:
        print("   [*] Joining pool...")
        pool.join()
        send_mail("Scraper crashed", "")
        sys.exit()
        print("   [*] Finished joining...")
        sys.exit(1)
