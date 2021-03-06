import mysql.connector
import functools
import usaddress
import logging
import polars as pl
import pandas as pd
import os
import secrets


@functools.lru_cache(maxsize=None)
def jail_name_search(jail_name, state, conn, county=None, split=True, exact=False):
    b = jail_name
    if split:
        jail_name = " ".join(jail_name.split()[:2])
    else:
        jail_name = jail_name

    cursor = conn.cursor()
    if not exact:
        if not county:
            cursor.execute(f'''SELECT id from jails where facility_name like "{jail_name}%" and facility_state in ("{state}");''')
        else:
            cursor.execute(f'''SELECT id from jails where facility_name like "{jail_name}%" and facility_state in ("{state}") and county like "{county}%";''')
        # print(f"SELECT id from jails where facility_name like '{jail_name}%' and facility_state in ('{state}') and county like '{county}%';")
    else:
        if not county:
            cursor.execute(f'''SELECT id from jails where facility_name = "{jail_name}" and facility_state in ("{state}");''')
        else:
            cursor.execute(f'''SELECT id from jails where facility_name = "{jail_name}" and facility_state in ("{state}") and county like "{county}%";''')


    id = list()
    for r in cursor:
        id.append(r)

    if len(id) > 1:
        print("\nTOO MANY IDS:", id, b)

    elif not len(id):
        # print("NOTHING FOUND:", id, jail_name)
        a = "a"

    else:
        id = id[0][0]
        return id

@functools.lru_cache(maxsize=None)
def search_and_add(jail_name, state, conn, file="added_jails.csv", county=None, address=None, verbosity=30, split=False):
    logging.basicConfig(level=verbosity)
    b = jail_name
    if split:
        jail_name = " ".join(jail_name.split()[:2])
    else:
        jail_name = jail_name

    cursor = conn.cursor()
    if not county:
        cursor.execute(f"SELECT id from jails where facility_name like '{jail_name}%' and facility_state in ('{state}');")
    else:
        cursor.execute(f"SELECT id from jails where facility_name like '{jail_name}%' and facility_state in ('{state}') and county like '{county}%';")
        # print(f"SELECT id from jails where facility_name like '{jail_name}%' and facility_state in ('{state}') and county like '{county}%';")

    id = list()
    for r in cursor:
        id.append(r)

    if len(id) > 1:
        print("\nTOO MANY IDS:", id, b)

    elif not len(id):
        if address and "N/A" not in address:
            parse_address(b, state, county, address, file, verbosity)

    else:
        id = id[0][0]
        return id

@functools.lru_cache(maxsize=None)
def parse_address(jail_name, state, county, address, file, verbosity):
    if "N/A" not in address:
        address_dict = {"id": "STABS" + str(secrets.token_hex(8)), "county": county, "facility_name": jail_name, "facility_address": None, "facility_city": None,  "facility_state": state, "facility_zip": None, "is_private":0, "in_urban_area": 0, "holds_greater_than_72_hours": -9, "holds_less_than_1_yr": -9, "felonies_greater_than_1_yr": -9, "hold_less_than_72_hours": -9, "facility_gender": 1, "num_inmates_rated_for": 0}
        dtype = {"id":str,
                "facility_zip":str,
                "is_private": int,
                "in_urban_area": int,
                "holds_greater_than_72_hours": int,
                "holds_less_than_1_yr": int,
                "felonies_greater_than_1_yr": int,
                "hold_less_than_72_hours":int,
                "facility_gender":int,
                "num_inmates_rated_for":int
                }
        if not os.path.exists(file):
            header = True
            # df = pl.from_pandas(pd.DataFrame(columns=["id","county","facility_name","facility_address","facility_city","facility_state","facility_zip","is_private","in_urban_area","holds_greater_than_72_hours","holds_less_than_1_yr","felonies_greater_than_1_yr","holds_greater_than_1_yr","hold_less_than_72_hours","facility_gender","num_inmates_rated_for"], dtype=int))

        elif os.path.exists(file) and os.stat(file).st_size > 271:
            # df = pl.read_csv(file, has_header=True, dtype=dtype)
            header = False
            # os.remove(file)
        else:
            header = True
            # df = pl.from_pandas(pd.DataFrame(columns=["id","county","facility_name","facility_address","facility_city","facility_state","facility_zip","is_private","in_urban_area","holds_greater_than_72_hours","holds_less_than_1_yr","felonies_greater_than_1_yr","holds_greater_than_1_yr","hold_less_than_72_hours","facility_gender","num_inmates_rated_for"], dtype=str))

        raw_address = str(address).upper().strip()
        try:
            parsed_address = usaddress.tag(raw_address)
            parse_success = True
        except usaddress.RepeatedLabelError as e:
            parse_success = False
            logging.warning(e)

        if parse_success:
            try:
                address_dict["facility_address"] = " ".join(str(raw_address.split(parsed_address[0]["PlaceName"])[0]).strip(",").strip().split())
            except usaddress.RepeatedLabelError as e:
                logging.warning(e)

            try:
                address_dict["facility_city"] = " ".join(str(parsed_address[0]["PlaceName"]).strip(",").strip().split())
            except KeyError:
                logging.warning("  [!] City key error!")

            try:
                address_dict["facility_zip"] = str(parsed_address[0]["ZipCode"]).strip()

            except KeyError:
                logging.warning("   [!] Zip key error")

            adl = list(address_dict.items())

            # Append the parsed data to the dataframe
            df = pd.DataFrame(address_dict.values(), dtype=str)

            # # print(df)
            df = pl.from_pandas(df)
            df = df.transpose(include_header=False, column_names=address_dict.keys())
            #
            # df = pd.concat([df, df2.to_pandas()])
            # df = df.drop_duplicates(subset=["id","facility_name", "facility_address", "county"])
            df = df.to_pandas()

            if header:
                df.to_csv(file, mode="a", index=False)
            else:
                df.to_csv(file, mode="a", index=False, header=False)

            return address_dict["id"]

    else:
        print("A")
