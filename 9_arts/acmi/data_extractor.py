import pandas as pd
import json

def video_link_checker(x):
    if len(x) != 0:
        print(x)
        return x
    else:
        return pd.NA

def date_checker(date, desc, start=True):
    date = date[0]
    if start:
        x = "date"
    else:
        x = "to_year"
    if len(str(date[x])) > 4: # If bigger than a year
        if not desc:  # If the date_description is missing, set it to that
            return [pd.NA, date[x]] # Null the date, set date to description
        else:
            return [pd.NA, desc]
    else:
        return [date[x], desc]


# pandas' read_json didn't work with this format
with open("download.json", "r") as f:
    j = json.load(f)
    j = j['results']

df = pd.DataFrame.from_dict(j)

# headline_credit -> creation year?

df = df.drop(["acmi_id", "title_annotation", "slug", "credit_line", "is_on_display",
              "last_on_display_place", "last_on_display_date", "is_context_indigenous", 'unpublished', 'external', 'brief_description',
       'constellations_primary', 'constellations_other', 'recommendations',
       'title_for_label', 'creator_credit_for_label',
       'headline_credit_for_label', 'description', 'description_for_label',
       'credit_line_for_label', 'details', 'stats', "links", 'creators_primary', 'creators_other', 'record_type', 'headline_credit', 'media_note', 'holdings',
       'part_of', 'parts', 'part_siblings', 'group', 'group_works',
       'group_siblings', 'source', 'source_identifier', 'eaas_environment_id', 'labels', 'external_references'], axis=1)
# print(df['video_links'])

df.columns = ['object_number', 'title', 'maker_full_name', 'category', 'materials',
       'date_description', 'image_url', 'from_location',
       'production_dates']


df["maker_full_name"]=df["maker_full_name"].apply(lambda x: str(x).replace(", ", "|")) # replace commas with pipes
df["image_url"]=df["image_url"].apply(lambda x: video_link_checker(x))
df["from_location"]=df["from_location"].apply(lambda x: "|".join([i["name"] for i in x])) # concat multiple locations

df[["year_start", "date_description"]] = df.apply(lambda x: date_checker(x["production_dates"], x["date_description"]), axis=1, result_type="expand")
df[["year_end", "date_description"]] = df.apply(lambda x: date_checker(x["production_dates"], x["date_description"], start=False), axis=1, result_type="expand")

df.drop("production_dates", axis=1, inplace=True)
