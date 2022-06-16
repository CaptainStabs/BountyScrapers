import json
import os
import re
from html import unescape


import pandas as pd
from tqdm import tqdm

# import heartrate; heartrate.trace(browser=True, daemon=True)

def video_link_checker(x):
    if len(x) != 0:
        # print(x)
        return x[0]["uri"]
    else:
        return None

def date_checker(date, desc, start=True):
    if len(date):
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
    else:
        return [pd.NA, desc]

def link_checker(link, img_url):
    # [{'url': 'https://www.justwatch.com/au/movie/the-birth-of-a-nation-1915', 'title': 'Stream, rent or buy at <span>JustWatch</span>', 'source': 'justwatch'}]
    if len(link) and img_url: # prefer original url over the alt
        return img_url
    elif len(link) and not img_url:
        return link[0]["url"]
    else:
        return pd.NA

def html_ents_to_unicode(text):
    return unicode(BeautifulStoneSoup(text, convertEntities=BeautifulStoneSoup.ALL_ENTITIES))

html_remover = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
dir = "F:/museum-collections/_acmi/"
for i, file in tqdm(enumerate(os.listdir(dir)), total = len(os.listdir(dir))):
    # pandas' read_json didn't work with this format
    with open("F:/museum-collections/_acmi/" + file, "r") as f:
        j = json.load(f)
        j = j['results']

    df = pd.DataFrame.from_dict(j)

    # headline_credit -> creation year?
    try:
        df = df.drop(["acmi_id", "title_annotation", "slug", "credit_line", "is_on_display",
                      "last_on_display_place", "last_on_display_date", "is_context_indigenous", 'unpublished', 'external', 'description',
                      'constellations_primary', 'constellations_other', 'recommendations',
                      'title_for_label', 'creator_credit_for_label',
                      'headline_credit_for_label', 'description_for_label',
                      'credit_line_for_label', 'details', 'stats', 'creators_primary', 'creators_other', 'record_type', 'headline_credit', 'media_note', 'holdings',
                      'part_of', 'parts', 'part_siblings', 'group', 'group_works',
                      'group_siblings', 'source', 'source_identifier', 'eaas_environment_id', 'labels', 'external_references'], axis=1)
        # print(df['video_links'])
    except KeyError:
        df = df.drop(["acmi_id", "title_annotation", "slug", "credit_line", "is_on_display",
                      "last_on_display_place", "last_on_display_date", "is_context_indigenous", 'unpublished','description',
                      'constellations_primary', 'constellations_other', 'recommendations',
                      'title_for_label', 'creator_credit_for_label',
                      'headline_credit_for_label','description_for_label',
                      'credit_line_for_label', 'details', 'stats', 'creators_primary', 'creators_other', 'record_type', 'headline_credit', 'media_note', 'holdings',
                      'part_of', 'parts', 'part_siblings', 'group', 'group_works',
                      'group_siblings', 'source', 'source_identifier', 'eaas_environment_id', 'labels', 'external_references'], axis=1)

    df.columns = ['object_number', 'title', 'maker_full_name', 'category', 'materials',
           'date_description', 'description', 'links', 'image_url', 'from_location',
           'production_dates']

    df["maker_full_name"]=df["maker_full_name"].apply(lambda x: str(x).replace(", ", "|")) # replace commas with pipes
    df["image_url"]=df["image_url"].apply(lambda x: video_link_checker(x))
    df["from_location"]=df["from_location"].apply(lambda x: "|".join([i["name"] for i in x])) # concat multiple locations
    df["description"]=df["description"].apply(lambda x: unescape(re.sub(html_remover, '', x)).replace("\n", "")[:10000])
    df["image_url"] = df.apply(lambda x: link_checker(x['links'], x["image_url"]), axis=1)

    df[["year_start", "date_description"]] = df.apply(lambda x: date_checker(x["production_dates"], x["date_description"]), axis=1, result_type="expand")
    df[["year_end", "date_description"]] = df.apply(lambda x: date_checker(x["production_dates"], x["date_description"], start=False), axis=1, result_type="expand")


    page_num = file.split("_")[-1][:-5]
    df["source_1"] = f"https://api.acmi.net.au/works/?page={page_num}"



    df.drop("production_dates", axis=1, inplace=True)

    df["institution_name"] = "Australian Centre for the Moving Image"
    df["institution_city"] = "Melbourne"
    df["institution_state"] = "Victoria"
    df["institution_country"] = "Australia"
    df["institution_latitude"] = -37.81759618959322
    df["institution_longitude"] = 144.96868723906857

    df.drop("links", axis=1, inplace=True)

    if not i:
        df.to_csv("extracted_data.csv", mode="a", index=False)
    else:
        df.to_csv("extracted_data.csv", mode="a", header=False, index=False)
