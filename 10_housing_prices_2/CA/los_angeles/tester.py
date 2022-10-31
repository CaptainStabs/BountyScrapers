import requests
from tqdm import tqdm

def scraper(path, start, end):
    for i in tqdm(range(start, end)):
        try:
            r = requests.get(f"https://portal.assessor.lacounty.gov/api/parceldetail?ain={i}")

            if r.status_code == 429:
                print("TOO Many Requests")
                return

            r = r.json()["Parcel"]

        except KeyboardInterrupt:
            return
