import pandas as pd
import re

def year_extractor(date):
    date = str(date)
    if date:
        return date.split("-")[0]
    else: return pd.NA

def dimensions(dim):
    print(dim)
    dimension = " x ".join([str(dim["circ"]), str(dim["depth"]), str(dim["diameter"]), str(dim["height"]), str(dim["length"]), str(dim["width"])])
    dimension = " ".join([dimension, "cm"])
    if not isinstance(dim["weight"], type(None)):
        dimension = " ".join([dimension, str(dim["weight"]), "kg"])
    if not isinstance(dim["duration"], type(None)):
        dimension = " ".join([dimension, str(dim["duration"]), "sec."])
    return dimension

df = pd.read_csv("Artworks.csv")

# ['Title', 'Artist',
#        'BeginDate', 'EndDate', 'Gender', 'Date', 'Medium', 'Dimensions',
#        'CreditLine', 'AccessionNumber', 'Classification', 'Department',
#        'DateAcquired', 'ObjectID', 'URL', 'ThumbnailURL',
#

df = df.drop(['ConstituentID', 'ArtistBio', 'Nationality', 'Circumference (cm)', 'Depth (cm)', 'Diameter (cm)', 'Height (cm)','Length (cm)', 'Weight (kg)', 'Width (cm)', 'Seat Height (cm)','Duration (sec.)', 'Cataloged'], axis=1)

df.columns = ["title",
              "maker_full_name",
              "maker_birth_year",
              "maker_death_year",
              "maker_gender",
              "date_description",
              "materials",
              "dimensions",
              "credit_line",
              "accession_number",
              "category",
              "department",
              "acquired_year",
              "object_number",
              "source_2",
              "image_url",
              ]

df["source_1"] = "https://github.com/MuseumofModernArt/collection/blob/master/Artworks.csv"
df["maker_birth_year"] = df["maker_birth_year"].str.replace(r'[()]+', '', regex = True)
df["maker_death_year"] = df["maker_death_year"].str.replace(r'[()]+', '', regex = True)
df["maker_gender"] = df["maker_gender"].str.replace(r'[()]+', '', regex = True)
df["acquired_year"] = df["acquired_year"].apply(lambda x: year_extractor(x))

df["institution_name"] = "The Museum of Modern Art"
df["institution_city"] = "New York"
df["institution_state"] = "New York"
df["institution_country"] = "United States"
df["institution_latitude"] = 40.761578954235446
df["institution_longitude"] = -73.97766451738849
# df["source_1"] = "https://github.com/MuseumofModernArt/collection/blob/master/Artworks.csv"

df_obj = df.select_dtypes(['object'])
df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())


df["maker_full_name"] = df["maker_full_name"].str.replace(", ", "|")
df["maker_birth_year"] = df["maker_birth_year"].str.replace(" ", "|")
df["maker_death_year"] = df["maker_death_year"].str.replace(" ", "|")
df["maker_gender"] = df["maker_gender"].str.replace(" ", "|")


df.to_csv("extracted_data.csv", index=False)
