import pandas as pd
import dateparser
from tqdm import tqdm
import functools

tqdm.pandas()

def dimensions(x):
    sizes = [x["hgt"], x["lgt"], x["wdt"], x["dpth"], x["circ"], x["diam"]]

    sizes = [str(x) for x in sizes if not pd.isna(x)]
    if len(sizes):
        size = " x ".join(sizes)
        size = " ".join([size, "cm"])
    else: size = ""

    wgt = x["wgt"]
    if wgt and not pd.isna(wgt):
        weight = " ".join([str(wgt), "g"])
    else: weight = pd.NA

    dims = [size, weight]
    dims = [x for x in dims if not pd.isna(x) and x]
    if len(dims):
        return " ".join(dims)
    else: return pd.NA

@functools.lru_cache(maxsize=None)
def get_year(x):
    if pd.isna(x):
        return

    if type(x) == float:print("\n FLOAT", x)
    x = x.replace("s", "").replace("?", "")

    if len(x) == 4 and x.isdigit():
        return int(x)

    date = dateparser.parse(x) if x and any(chr.isdigit() for chr in x) else None
    if date:
        return int(date.year)
    else: return

def get_loc(x):
    locs = [x["county"], x["state"], x["country"]]
    locs = [x for x in locs if not pd.isna(x)]
    if len(locs):
        return ", ".join(locs)
    else: return pd.NA

file = "Archeology.csv"
df = pd.read_csv(file)

df["dimensions"] = df.apply(lambda x: dimensions(x), axis=1)
df["acquired_year"] = df["acquired_year"].progress_apply(lambda x: get_year(x) if x else None)
df["category"] = df["category"].str.replace("Burke Museum", "")
df["image_url"] = df["media"].apply(lambda x: eval(x)[0]["BaseURL"] + eval(x)[0]["FileURL"] if not pd.isna(x) else pd.NA)
df["from_location"] = df.apply(lambda x: get_loc(x), axis=1)
print(df)
df = df.drop(["circ", "wgt", "diam", "hgt", "lgt", "wdt", "dpth", "media", "country", "state", "county"], axis=1)

df["institution_name"] = "Burke Museum of Natural History and Culture"
df["institution_city"] = "Seattle"
df["institution_state"] = "Washington"
df["institution_country"] = "United States"
df["institution_latitude"] = 47.66044008449786
df["institution_longitude"] = -122.31153649941562
df["source_1"] = "https://www.burkemuseum.org/collections/search/"

df.to_csv(file[:-4] + "_extracted.csv", index=False)
