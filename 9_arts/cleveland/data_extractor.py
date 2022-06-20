import pandas as pd
import polars as pl
import re

def year_extractor(c):
    y = c[c.find("(") + 1 : c.find(")")].replace("mid-", "mid ")
    if "," in y:
        y = y.split(", ")[-1] # gets content from inside (), gets content right of comma,
    try:
        if any(x in y for x in ["-", "–"]):
            try:
                birth_year, death_year = (
                    y.split("-")
                    )
            except ValueError:
                birth_year, death_year = (
                    y.split("–")
                )
        else:
            birth_year, death_year = y.strip(), ""
    except ValueError:
        print(y)
        return "", ""

    return birth_year, death_year

# print(year_extractor("(, 1958)"))

def creator_parser(creator):
    # creator format: name (nationality, birth_year-death_year), role
    name_list = []
    role_list = []
    birth_list = []
    death_list = []
    if isinstance(creator, str):
        creators = creator.split(";")
        for c in creators:
            if c:
                if "(" in c:
                    name_list.append(c.split(" (")[0].strip())
                    role_list.append(re.sub(r"\([^)]*\)", "", c).split(" , ")[-1].strip())
                    birth_year, death_year = year_extractor(c)

                    birth_list.append(birth_year)
                    death_list.append(death_year)
                else:
                    return c.split(",")[0], pd.NA, pd.NA, pd.NA

        names = "|".join(name_list)
        roles = "|".join(role_list)
        births = "|".join(birth_list)
        deaths = "|".join(death_list)
        return names, roles, births, deaths
    else:
        return pd.NA, pd.NA, pd.NA, pd.NA





# print(creator_parser("Albert-Charles Lebourg (French, 1849-1928), artist; name (AA, 2015-2020), maker"))

df = pd.read_csv("_data.csv")
# ['id', 'accession_number',
#        'current_location', 'title', 'creation_date',
#        'creation_date_earliest', 'creation_date_latest', 'creators', 'culture',
#        'technique', 'support_materials', 'department', 'type',
#        'measurements', 'creditline', 'inscriptions',  'provenance',
#        'find_spot', 'digital_description', 'url', 'image_web', ],
df = df.drop(
    [
        "share_license_status",
        "tombstone",
        "title_in_original_language",
        "series",
        "series_in_original_language",
        "collection",
        "state_of_the_work",
        "edition_of_the_work",
        "copyright",
        "exhibitions",
        "related_works",
        "former_accession_numbers",
        "fun_fact",
        "wall_description",
        "external_resources",
        "citations",
        "catalogue_raisonne",
        "image_print",
        "image_full",
        "updated_at",
        "Unnamed: 41",
        "Unnamed: 42",
    ],
    axis=1,
)
df.columns = [
    "object_number",
    "accession_number",
    "current_location",
    "title",
    "date_description",
    "year_start",
    "year_end",
    "creators",
    "culture",
    "technique",
    "materials",
    'department',
    'category',
    'dimensions',
    'credit_line',
    'inscriptions',
    'provenance',
    'from_location',
    'description',
    'source_2',
    'image_url'
]

df[["maker_full_name", "maker_role", "maker_birth_year", "maker_death_year"]] = df.apply(lambda x: creator_parser(x["creators"]), axis=1, result_type='expand')

df = df.drop("creators", axis=1)

df["technique"] = df.apply(lambda x: df["technique"][:200])
df["title"] = df.apply(lambda x: df["title"][:1000])

df["institution_name"] = "The Cleveland Museum of Art"
df["institution_city"] = "Cleveland"
df["institution_state"] = "Ohio"
df["institution_country"] = "United States"
df["institution_latitude"] = 41.509209799356306
df["institution_longitude"] = -81.61205957318529
df["source_1"] = "https://github.com/ClevelandMuseumArt/openaccess/blob/master/data.csv"

df.to_csv("extracted_data.csv", index=False)
