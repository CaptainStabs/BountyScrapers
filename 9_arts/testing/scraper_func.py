import signal
from tqdm import tqdm
import time


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
            time.sleep(0.05)

            with lock:
                bar.update(1)

    except KeyboardInterrupt:
        return

    except:
        raise


# scraper("extracted_data.csv", 0, 2220758)
# send_mail("Finished", "Finished")
