import pandas as pd
from cachetools import cached
from cachetools.keys import hashkey
# import heartrate; heartrate.trace(browser=True, daemon=True)

# Seperate out the search so that it can cache the ids
@cached(cache={}, key=lambda artist_id, a_df, is_birth: hashkey(artist_id, is_birth))
def artist_search(artist_id, a_df, is_birth):
    r = a_df.loc[a_df['artist_ids'] == int(str(artist_id).strip())]
    if is_birth:
        return r.birth_date.item()
    else:
        return r.death_date.item()


def multiple_ids(artist_id, a_df, is_birth):
    id_list = artist_id.split(",")
    if is_birth:
        b_list = []
        for id_ in id_list:
            birth_year = artist_search(id_, a_df, is_birth)
            b_list.append(str(birth_year))
        birth_years = ("|").join(b_list)
        return birth_years
    else:
        d_list = []
        for id_ in id_list:
            death_year = artist_search(id_, a_df, is_birth)
            d_list.append(str(death_year))
        death_years = ("|").join(d_list)
        return death_years


def artist_dates(artist_id, a_df, is_birth=True):
    if "," in artist_id:
        return multiple_ids(artist_id, a_df, is_birth=is_birth)

    else:
        if is_birth:
            return artist_search(artist_id, a_df, is_birth)
        else:
            return artist_search(artist_id, a_df, is_birth)



df = pd.read_csv("./files/artworks.csv")
# df = df[df["display_date"].isin(["2021", "2022"])]
# ['id', 'title', 'classification', 'medium', 'accession_number', 'dimensions','credit_line', 'artists', 'artist_ids'],
drop_col = ["credit_line_repro", "publication_info", "edition"]
df = df.drop(drop_col, axis=1)
df.columns = ["object_number", "title", "date_description", "category", "materials", "accession_number", "dimensions", "credit_line", "maker_full_name", "artist_ids"]
df["institution_name"] = "Whitney Museum of American Art"
df["institution_city"] = "New York"
df["institution_state"] = "New York"
df["institution_country"] = "United States"
df["institution_latitude"] = 40.73958699161049
df["institution_longitude"] = -74.00886349911856
df["source_1"] = "https://github.com/whitneymuseum/open-access"

a_df = pd.read_csv("./files/artists.csv")
df["maker_full_name"]=df["maker_full_name"].apply(lambda x: x.replace(", ", "|"))
df["maker_birth_year"] = df["artist_ids"].apply(lambda x: artist_dates(x, a_df))
df["maker_death_year"] = df["artist_ids"].apply(lambda x: artist_dates(x, a_df, is_birth=False))
# print(df.loc[df["artist_ids"].str.contains(",")])
df.drop("artist_ids", axis=1, inplace=True)
df.to_csv("output.csv", index=False)
