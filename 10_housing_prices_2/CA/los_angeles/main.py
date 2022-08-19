import sys
import traceback as tb
from multiprocessing import Pool
from pathlib import Path

from scraper import scraper
# from tester import scraper

p = Path(__file__).resolve().parents[2]
sys.path.insert(1, str(p))
from _common import get_last_id
from _common.send_mail import send_mail

if __name__ == "__main__":
    arguments = []

    end_id = 584339605 #8,765,094,086
    # start_num is supplemental for first run and is only used if the files don't exist
    for i in range(15):
        if i == 0:
            start_num = 2004001003
        else:
            # Use end_id before it is added to
            start_num = end_id - 584339605
        print("Startnum: " + str(start_num))
        arguments.append([f"F:/_Bounty/LA/extracted_data{i}.csv", start_num, end_id])
        end_id = end_id + 584339605
    print(arguments)

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
