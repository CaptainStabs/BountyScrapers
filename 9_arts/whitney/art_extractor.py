import pandas as pd
import functools
import heartrate; heartrate.trace(browser=True, daemon=True)

def artist_search(artist_id, a_df, is_birth):
    if is_birth:
        return a_df.loc[a_df['artist_ids'] == int(str(id).strip())].birth_date.item()
    else:


def multiple_ids(artist_id, a_df, is_birth):
    id_list = artist_id.split(",")
    if is_birth:
        b_list = []
        for id in id_list:
            birth_year = artist_search(id, a_df, is_birth)
            b_list.append(str(birth_year))
        birth_years = ("|").join(b_list)
        return birth_years
    else:
        d_list = []
        for id in id_list:
            death_year = a_df.loc[a_df['artist_ids'] == int(str(id).strip())].death_date.item()
            d_list.append(str(death_year))
        death_years = ("|").join(b_list)
        return death_years


@functools.lru_cache(maxsize=None)
def artist_dates(artist_id, a_df, is_birth=True):
    if "," in artist_id:
        multiple_ids(artist_id, a_df, is_birth=is_birth)

    else:
        if is_birth:
            birth_year = a_df.loc[a_df['artist_ids'] == int(str(artist_id).strip())].birth_date.item()
            return birth_year
        else:
            death_year = a_df.loc[a_df['artist_ids'] == int(str(artist_id).strip())].death_date.item()
            return death_year



df = pd.read_csv("artworks.csv")
# df = df[df["display_date"].isin(["2021", "2022"])]
# ['id', 'title', 'classification', 'medium', 'accession_number', 'dimensions','credit_line', 'artists', 'artist_ids'],
drop_col = ["credit_line_repro", "publication_info", "edition"]
df = df.drop(drop_col, axis=1)
df.columns = ["object_number", "title", "date_description", "category", "materials", "accession_number", "dimensions", "credit_line", "maker_full_name", "artist_ids"]
# df["institution_name"] = "Whitney Museum of American Art"
# df["institution_city"] = "New York"
# df["institution_state"] = "New York"
# df["institution_country"] = "United States"
# df["institution_latitude"] = 40.73958699161049
# df["institution_longitude"] = -74.00886349911856
# df["source_1"] = "https://github.com/whitneymuseum/open-access"

a_df = pd.read_csv("artists.csv")
df["maker_full_name"]=df["maker_full_name"].apply(lambda x: x.replace(", ", "|"))
df["maker_birth_year"] = df["artist_ids"].apply(lambda x: artist_dates(x, a_df))
df["maker_death_year"] = df["artist_ids"].apply(lambda x: artist_dates(x, a_df, is_birth=False))
print(df)
# df_final = pd.merge(df, df1, on="artist_ids")
# df_final.drop(["artist_full_name", "artist_ids"], axis=1, inplace=True)
# df = df_final
#
#
#
# df.to_csv("output.csv", index=False)
