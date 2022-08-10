import signal
from tqdm import tqdm
import time
import random
import sys


def scraper(filename, start_num, end_num, position, lock):
    with lock:
        bar = tqdm(
            desc=f'{start_num}-{end_num}',
            total=end_num,
            position=position,
            leave=False
        )
    try:
        # print("\nARGS:", filename, start_num, end_num)
        # for i in tqdm(range(start_num, end_num)):
        for i in range(start_num, end_num):
            if i % 2 == 0:
                with lock:
                    sys.stdout.write("\r")
                    sys.stdout.write("AAAA")
                    sys.stdout.flush()
                # print("AAA")
            time.sleep(0.05)
            time.sleep(random.uniform(0.01,0.1))

            with lock:
                bar.update(1)

    except KeyboardInterrupt:
        return

    except:
        raise


# scraper("extracted_data.csv", 0, 2220758)
# send_mail("Finished", "Finished")
