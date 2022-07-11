import signal
from tqdm import tqdm
import time


def scraper(filename, start_num=False, end_num=False):
    try:
        # print("\nARGS:", filename, start_num, end_num)
        for i in tqdm(range(start_num, end_num)):
            time.sleep(5)

    except KeyboardInterrupt:
        return

    except:
        raise


# scraper("extracted_data.csv", 0, 2220758)
# send_mail("Finished", "Finished")
