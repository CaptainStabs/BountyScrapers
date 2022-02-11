import csv
from tqdm import tqdm
import json

from pathlib import Path
import sys

p = Path(__file__).resolve().parents[2]
sys.path.insert(1, str(p))

from _sale_type.sale_type import sale_type

with open("Tax_Parcels.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)
    # sale_type = []
    sale_types = {}
    for row in tqdm(reader, total=line_count):
        sale_instrument = row["SalesInstrument"].upper().strip()
        sale_desc = row["SalesInstrumentDesc"].upper().strip()
        if sale_instrument not in sale_type:
            if sale_desc:
                # sale_type.append(row["SalesInstrument"])
                sale_types[sale_instrument] = sale_desc

print(json.dumps(sale_types, indent=2))
