import csv
import json
import os
import sys
import time
import traceback as tb
from pathlib import Path

import requests
from tqdm import tqdm

p = Path(__file__).resolve().parents[1]
sys.path.insert(1, str(p))
from _common import get_last_id
from _common.send_mail import send_mail

filename = "extracted_data.csv"

columns = ['institution_name', 'institution_city', 'institution_state', 'institution_country', 'institution_latitude', 'institution_longitude', "object_number", "accession_number", "culture", "date_description", "materials", "from_location", "credit_line", "description", "department", "dimensions", "image_url", "source_1", "source_2"]

with open(filename, "a", encoding='utf-8', newline='') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=columns)

    if os.path.exists(filename) and os.stat(filename).st_size > 299:
        next = get_last_id(filename, 299, "source_2")
        # start_id = 3320
    else:
        next = "https://collections.maa.cam.ac.uk/objects-api/objects"

    if os.stat(filename).st_size == 0:
        writer.writeheader()

    s = requests.Session()
    with tqdm(total=17027) as pbar:
        while next:
            r = s.get(next)
            jdr = r.json()

            # max 84401
            try:
                if jdr:
                    for jd in jdr["results"]:
                        data = {
                            "institution_name": "Museum of Archaeology and Anthropology",
                            "institution_city": "Cambridge",
                            "institution_state": "Cambridgeshire",
                            "institution_country": "United Kingdom",
                            "institution_latitude": 52.202851448958754,
                            "institution_longitude": 0.1212875687220559,
                            "object_number": jd["id"],
                            "accession_number": jd["main_ref_no"]["number"],
                            "culture": "|".join(jd["culture_group"]),
                            "date_description": "|".join([x["name"] for x in jd["period"]]),
                            "materials": "|".join([x["name"] for x in jd["material"]]),
                            "from_location": jd["de_norm_place"],
                            "credit_line": jd["source"],
                            "description": jd["description"].replace("<br />", ""),
                            "department": jd["department"]["name"],
                            "dimensions": jd["dimensions"],
                            "image_url": jd["images"][0] if len(jd["images"]) else None,
                            "source_1": jd["facebook_share"].split("?u=")[-1],
                            "source_2": next
                        }
                        writer.writerow(data)

            except Exception as e:
                tb.print_exc()
                # print(json.dumps(jdr, indent=4))

            next = jdr["next"]
            pbar.update(1)
send_mail("MAA finished")
