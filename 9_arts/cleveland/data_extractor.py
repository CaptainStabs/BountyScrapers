import pandas as pd
import polars as pl
import re

def year_extractor(c):


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
                print(c)
                if "(" in c:
                    name_list.append(c.split(" (")[0].strip())
                    role_list.append(re.sub(r"\([^)]*\)", "", c).split(" , ")[-1].strip())
                    try:
                        birth_year, death_year = (
                            c[c.find("(") + 1 : c.find(")")].split(", ")[1].split("-") # gets content from inside (), gets content right of comma, then splits date range
                        )
                    except ValueError:
                        birth_year, death_year = (
                            c[c.find("(") + 1 : c.find(")")].split(", ")[1].split("–") # gets content from inside (), gets content right of comma, then splits date range
                        )

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
    'source_1',
    'image_url'
]

df[["maker_full_name", "maker_role", "maker_birth_year", "maker_death_year"]] = df.apply(lambda x: creator_parser(x["creators"]), axis=1, result_type='expand')
