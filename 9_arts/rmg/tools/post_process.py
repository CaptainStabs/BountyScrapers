import pandas as pd

def maker_name(x):
    creator, people = x["creator"], x["people"]
    c, p = None, None
    if not pd.isnull(creator):
        c = "|".join(creator.split("; "))
    if not pd.isnull(people):
        p = "|".join(people.split("; "))
    l = [x for x in [c, p] if x]
    if len(l):
        return "|".join(l)
    else:
        return


df = pd.read_csv("combined.csv")

df = df.rename(columns={
    "id": "object_number",
    "collection": "category",
    "type": "sub_cat",
    "display_location": "current_location",
    "date_made": "date_description",
    "credit": "credit_line",
    "measurements": "dimensions",
    "places": "from_location",
})

df["maker_full_name"] = df.apply(lambda x: maker_name(x), axis=1)

df["category"] = df["category"].fillna('')
df["sub_cat"] = df["sub_cat"].fillna('')
df["category"] = df[["category", "sub_cat"]].apply(", ".join, axis=1)
df["category"] = df["category"].str.strip(", ")

df["description"] = df["description"][:10000]
df["date_description"] = df["date_description"].apply(lambda x: " ".join(x.split()) if len(str(x)) > 500 else x)
df["date_description"] = df["date_description"].apply(lambda x: x.replace(" - ", ",") if len(str(x)) > 500 else x)
df["date_description"] = df["date_description"].apply(lambda x: x[:500] if len(str(x)) > 500 else x)

df["institution_name"] = "National Maritime Museum"
df["institution_city"] = "London"
df["institution_state"] = "England"
df["institution_country"] = "United Kingdom"
df["institution_latitude"] = 41.0919742529525
df["institution_longitude"] = -73.83528113087031


df = df.drop(["events", "parts", "vessels", "exhibition", "drop_me", "creator", "people", "sub_cat"], axis=1)

df.to_csv("finished.csv", index=False)
