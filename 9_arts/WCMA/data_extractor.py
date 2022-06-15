import pandas as pd
import polars as pl
import json
import numpy as np

with open("Objects-utf8.json", "r", encoding="utf-8-sig") as f:
    d = json.load(f)

df = pd.DataFrame(d)

def life_span(x):
    try:
        years = x.split("-")
        birth_year = years[0]
        try:
            death_year = years[1]
        except IndexError:
            death_year = pd.NA
        return [birth_year, death_year]
    except AttributeError:
        return [pd.NA, pd.NA]
    except IndexError:
        print(x)

df.drop(["ulan", "department", "paper_support", "catalogue_raisonne", "portfolio", "signed", "marks", "classification", 'element_type', 'width_cm',
       'height_cm', 'depth_cm', 'width_in', 'height_in', 'depth_in', 'area_in',
       'size_s_m_l', 'is_3d', 'orientation_p_l_s', 'copyright_holder',
       'publicCaption', 'artistNationality',  'paper_support', 'catalogue_raisonne', 'portfolio', 'signed', 'marks', 'description',
       'terms', 'data_date', 'Description',  'source_name', "filename"], inplace=True, axis=1)

df.columns = ['object_number', 'accession_number', 'title', 'maker_full_name',
       'culture', 'period', 'date_description',
       'year_start', 'year_end', 'accession_year',
       'category', 'materials', 'credit_line',
       'inscriptions', 'dimensions','artistLifeSpan']

# Set `not found` to null
df["artistLifeSpan"] = df["artistLifeSpan"].replace("not found", pd.NA)
df["date_description"] = df["date_description"].replace("no date", pd.NA)
df["inscriptions"] = df["inscriptions"].replace("no inscription", pd.NA)

df["image_url"] = "https://get-thumb.herokuapp.com/getThumb.php?objectid=" + df['object_number'].astype(str)
df["source_1"] = "https://github.com/wcmaart/collection"

df[["maker_birth_year", "maker_death_year"]] = df.apply(lambda x: life_span(x["artistLifeSpan"]), axis=1, result_type="expand")
df["maker_full_name"]=df["maker_full_name"].apply(lambda x: str(x).replace(", ", "|"))
df.drop("artistLifeSpan", axis=1, inplace=True)

df["institution_name"] = "Williams College Museum of Art ("
df["institution_city"] = "Williamstown"
df["institution_state"] = "Massachusetts"
df["institution_country"] = "United States"
df["institution_latitude"] = 42.7112131380762
df["institution_longitude"] = -73.20269661733933

df.to_csv("output.csv", index=False)
