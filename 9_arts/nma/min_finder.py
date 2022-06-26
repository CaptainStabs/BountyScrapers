import requests
from tqdm import tqdm
import time

s = requests.Session()
for i in tqdm(range(84683, 0, -1)):
    st = time.perf_counter()
    url = f"https://data.nma.gov.au/object/{i}"
    r = s.get(url)
    jd = r.json()
    et = time.perf_counter()
    if jd["data"]:
        print(url)
        break

    sleep_time = 1 - (et - st)
    sleep_time = abs(sleep_time)
    time.sleep(sleep_time)
