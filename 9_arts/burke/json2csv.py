import json
import pandas as pd

filename = "Archeology"
with open(filename + ".json", "r", encoding="utf-8") as f:
    jd = json.load(f)
    jd = jd["items"]
df = pd.DataFrame(jd)

#  'People', 'Provenance', 'Site', 'SiteNumber', 'Country',
#        'State', 'County', 'Origin', 'Found', 'Level', 'Stratum', 'Status',
#        'Latitude', 'Longitude', 'BagNumber', 'SearchTerms', 'Media',
#        'DatesCreated', 'SitesAdded', 'Title', 'Contains']

cols = {
    "Collection": "category", # Remove "Burk Musuem" from col later
    "Account": "accession_number",
    "ReceivedDate": "acquired_year", # will need to format
    "ReceivedFrom": "acquired_from",
    "Credit": "credit_line",
    "ObjectID": "object_number",
    "ObjectName": "title",
    "Description": "description",
    "Material": "materials",
    "Technique": "technique",
    "CircumferenceCentimeters": "circ",
    "WeightGrams": "wgt",
    "DiameterCentimeters": "diam",
    "HeightCentimeters": "hgt",
    "LengthCentimeters": "lgt",
    "WidthCentimeters": "wdt",
    "DepthCentimeters": "dpth",
    "InscriptionText": "inscription",
    "People": "maker_full_name",
    "Provenance": "provenance",
    "Country": "country",
    "State": "state",
    "County": "county",
    "Media": "media"
}

keep_list = cols.keys()
col_list = list(df.columns)
remove_list = [x for x in col_list if x not in keep_list]
df = df.drop(remove_list, axis=1)

df = df.rename(columns=cols)

df.to_csv(filename + ".csv", index=False)
