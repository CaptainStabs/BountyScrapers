from lxml.html import fromstring
import requests
from bs4 import BeautifulSoup
import json
import csv

import sys
from pathlib import Path

p = Path(__file__).resolve().parents[2]
sys.path.insert(1, str(p))
from _common import date_parse


sale_types = json.load(open("doctypes.json", "r"))


columns = ["property_id","property_street_address","property_township","land_area_acres","land_area_sqft","property_type","building_num_stories","building_num_units","building_year_built","building_area_sqft","building_num_beds","building_num_baths","property_lat","property_lon", "sale_id", "sale_datetime", ""]
with open("extracted_data.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    with open("extracted_sales_data.csv", "a", encoding="utf-8", newline="") as output_csv:
        writer = csv.DictWriter(output_csv)
r = requests.get("http://gis.summitcountyco.gov/Map/DetailData.aspx?Schno=6518029").text

soup = BeautifulSoup(r, "html.parser")

rows = soup.find("table").find_all("tr")

cols = ["id", "date", "type", "price"]
for row in rows:
    sale_row = row.find_all("td", class_="style2b") # style2b is only assigned to the sale-related cells
    if sale_row: # Filter out blank rows
        sale_row = [x.get_text() for x in sale_row] # Get the text from each item in the sale_row list

        if len(sale_row) != 4:
            print("Sale row is not 4\n url") # add url once we get there

        sale_data = dict(zip(cols, sale_row))
        sale_data["type"] = sale_types[sale_data["type"]]

        print(sale_data)
