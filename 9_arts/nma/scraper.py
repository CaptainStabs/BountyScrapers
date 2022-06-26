import requests
import csv
import json
import os
import time
import requests
import sys
from tqdm import tqdm
from pathlib import Path

p = Path(__file__).resolve().parents[1]
sys.path.insert(1, str(p))
from _common import get_last_id

filename = "extracted_data.csv"

columns = ['institution_name', 'institution_city', 'institution_state', 'institution_country', 'institution_latitude', 'institution_longitude', 'object_number', 'title', 'accession_number', 'source_1', 'category', 'material', 'image_url', 'dimensions', 'maker_full_name', 'maker_role', 'description', 'from_location', 'date_description', 'year_start', 'year_end', 'drop_me']

with open(filename, "a", encoding='utf-8', newline='') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=columns)

    if os.path.exists(filename) and os.stat(filename).st_size > 283:
        start_id = get_last_id(filename)
    else:
        start_id = 0

    if os.stat(filename).st_size == 0:
        writer.writeheader()

    s = requests.Session()
    for i in tqdm(range(0, 84402)):
        st = time.perf_counter()
        url = "https://data.nma.gov.au/object/84401"
        r = s.get(url)
        jd = r.json()

        # max 84401
        if "data" in jd.keys():
            jd = jd["data"][0]

            data = {
                "institution_name": "National Museum of Australia",
                "institution_city": "Acton",
                "institution_state": "Australian Capital Territory",
                "institution_country": "Australia",
                "institution_latitude": -35.29289948785895,
                "institution_longitude": 149.12054371988773,
                "object_number": jd["id"],
                "title": jd["title"],
                "accession_number": jd["identifier"],
                "source_1": url,
                "drop_me": i
            }

            if jd["additionalType"]:
                data["category"] = "|".join([x for x in jd["additionalType"]])

            if jd["medium"]:
                data["material"] = "|".join([x["title"] for x in jd["medium"]])

            meta = jd["_meta"]
            if "hasFormat" in meta.keys():
                data["image_url"] = meta["hasFormat"]

            ex = jd["extent"]
            try:
                dim = " x ".join([str(ex["height"]), str(ex["length"]), str(ex["width"])])
                data["dimensions"] = " ".join([dim, ex["unitText"]])
            except KeyError:
                try:
                    dim = " x ".join([str(ex["height"]), str(ex["width"]), str(ex["depth"])])
                    data["dimensions"] = " ".join([dim, ex["unitText"]])
                except KeyError:
                    print(json.dumps(ex, indent=4))

            contrib = jd["contributor"]
            if "creator" in jd.keys():
                creator = jd["creator"]
                mfn = "|".join([x["title"] for x in creator])
                mr = "|".join([x["roleName"] for x in creator])

                if contrib:
                    mfn1 =  "|".join([x["title"] for x in contrib])
                    mr1 = "|".join([x["roleName"] for x in contrib])

                    mfn = "|".join([mfn, mfn1])
                    mr = "|".join([mr, mr1])

                data["maker_full_name"] = mfn
                data["maker_role"] = mr


            elif contrib:
                data["maker_full_name"] = "|".join([x["title"] for x in contrib])
                data["maker_role"] = "|".join([x["roleName"] for x in contrib])

            if "description" in jd.keys():
                data["description"] = jd["description"][:10000]
            elif "physicalDescription" in jd.keys():
                data["description"] = jd["physicalDescription"][:10000]
            elif "significanceStatement" in jd.keys():
                data["description"] = jd["significanceStatement"][:10000]

            if jd["spatial"]:
                data["from_location"] = '|'.join([": ".join([x["roleName"], x["title"]]) for x in jd["spatial"]])[:4000]

            if "temporal" in jd.keys():
                temp = jd["temporal"][0]
                if "roleName" in temp.keys():
                    data["date_description"] = ": ".join([temp["roleName"], temp["title"]])
                else:
                    data["date_description"] = ": ".join([temp["interactionType"], temp["title"]])
                    print("using interaction type")

                data["year_start"] = temp["startDate"]
                data["year_end"] = temp["endDate"]

            writer.writerow(data)
            et = time.perf_counter()
            st = 1 - (et - st)
            # print((et - st))
            st = abs(st)
            time.sleep(st)
