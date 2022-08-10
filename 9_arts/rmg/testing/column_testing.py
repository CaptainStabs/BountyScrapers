import polars as pl
import pandas as pd
from tqdm import tqdm
import json

headers = {}
column = ['ID:', 'Collection:', 'Type:', 'Display location:', 'Creator:', 'Events:', 'Date made:', 'Credit:', 'Measurements:', 'Parts:', 'Places:', 'People:', 'Vessels:', 'Exhibition:']

for i in tqdm(range(110000, 110500, 5)):
    try:
        print(f"https://www.rmg.co.uk/collections/objects/rmgc-object-{i}")
        df = pd.read_html(f"https://www.rmg.co.uk/collections/objects/rmgc-object-{i}")[0]
    except KeyboardInterrupt:
        break
    except:
        raise
        try:
            df = pd.read_html(f"https://www.rmg.co.uk/collections/objects/rmgc-object-{i+1}")[0]
        except:
            continue
    df = df.transpose()
    df.columns = df.iloc[0]
    cols = df.columns.tolist()

    for x in cols:
        if x not in headers.keys():
            headers[x] = [df.iloc[-1][x], i]

print(headers)
print(headers.keys())
print(json.dumps(headers, indent=4))
