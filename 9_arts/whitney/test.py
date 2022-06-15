import pandas as pd
from cachetools import cached
from cachetools.keys import hashkey
import heartrate; heartrate.trace(browser=True, daemon=True)

artist_id = "4780, 4781, 4855, 4856, 4631, 615, 3913, 4782"
is_birth = True
a_df = pd.read_csv("artists.csv")


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

print(artist_dates(artist_id, a_df))
