import requests
import json
import tqdm
import datetime

import sys
from pathlib import Path

p = Path(__file__).resolve().parents[2]
sys.path.insert(1, str(p))
from _common import date_parse


s = requests.Session()
id = 2004001004
url = f"https://portal.assessor.lacounty.gov/api/parceldetail?ain={id}"

r = requests.get(url).json()
r = r["Parcel"]

assessed_date = str(date_parse("-".join([r["CurrentRoll_BaseYear"], "01", "01"])))
data = {
    "state": "CA",
    "property_zip5": r["SitusZipCode"][:5],
    "property_street_address": " ".join(r["SitusStreet"].upper().split()),
    "property_city": r["SitusCity"].strip(" CA").strip(),
    "property_county": "LOS ANGELES",
    "property_id": r["AIN"],
    "property_type": r["UseType"],
    "property_lat": r["Latitude"],
    "property_lon": r["Longitude"],
    "building_num_units": r["NumOfUnits"],
    "building_year_built": r["YearBuilt"],
    "building_area_sqft": r["SqftMain"],
    "land_area_sqft": r["SqftLot"],
    "building_num_beds": r["NumOfBeds"],
    "building_num_baths": r["NumOfBaths"],
    "land_area_acres": r["LandAcres"],
    "land_assessed_value": r["CurrentRoll_LandValue"],
    "land_assessed_date": assessed_date,
    "building_assessed_value": r["CurrentRoll_ImpValue"],
    "building_assessed_date": assessed_date,
}

sale_request = s.get(f"https://portal.assessor.lacounty.gov/api/parcel_ownershiphistory?ain={id}").json()

sr = sale_request["Parcel_OwnershipHistory"]

for sale in sr:
    data["sale_datetime"] = str(date_parse(sale["RecordingDate"]))
    data["sale_price"] = sale["DTTSalePrice"]
    data["total_assessed_value"] = sale["AssessedValue"]
    data["transfer_deed_type"] = sale["DocumentReasonCodeDesc"]

print(json.dumps(data, indent=2))
