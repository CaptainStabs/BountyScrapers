import yaml
import csv
from tqdm import tqdm
import json
# import heartrate; heartrate.trace(browser=True, daemon=True)

columns = ["id","county", "facility_name", "facility_address", "facility_city","facility_state", "facility_zip", "is_private", "in_urban_area", "holds_greater_than_72_hours",
        "holds_less_than_1_yr","felonies_greater_than_1_yr", "hold_less_than_72_hours","facility_gender","num_inmates_rated_for"]
removed_zips = []
wrong_state = {}
with open("us_zipcodes.yaml", "r") as f:
    zip_cty_cnty = yaml.safe_load(f)
    # print(zip_cty_cnty[31419])

with open("address_updated.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("added_counties.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()
        # writer.writeheader()

        for row in tqdm(reader, total=line_count):
            success = False
            zip_error = False
            zip5 = row["facility_zip"]
            if zip5 and row["facility_city"]:
                try:
                    try:
                        county = zip_cty_cnty[zip5]["county"].capitalize()
                        city = zip_cty_cnty[zip5]["city"]
                        state = zip_cty_cnty[zip5]["state"]
                    except ValueError:
                        raise ValueError
                    except KeyError:
                        try:
                            county = zip_cty_cnty[str(int(zip5)+1)]["county"].capitalize()
                            city = zip_cty_cnty[str(int(zip5)+1)]["city"]
                            state = zip_cty_cnty[str(int(zip5)+1)]["state"]
                        except ValueError:
                            raise ValueError
                        except KeyError:
                            try:
                                county = zip_cty_cnty[str(int(zip5)-1)]["county"].capitalize()
                                city = zip_cty_cnty[str(int(zip5)-1)]["city"]
                                state = zip_cty_cnty[str(int(zip5)-1)]["state"]
                            except ValueError:
                                raise ValueError
                            except KeyError:
                                zip_error = True
                                # print(zip5)
                except ValueError:
                    zip_error = True

                if not zip_error:
                    if state == row["facility_state"]:
                        land_info = {
                            "id": row["id"],
                            "county": county,
                            "facility_name" : row["facility_name"],
                            "facility_address": row["facility_address"],
                            "facility_city": row["facility_city"],
                            "facility_state": row["facility_state"],
                            "facility_zip": row["facility_zip"],
                            "is_private": 0,
                            "in_urban_area": 0,
                            "holds_greater_than_72_hours": -9,
                            "holds_less_than_1_yr": -9,
                            "felonies_greater_than_1_yr": -9,
                            "hold_less_than_72_hours": -9,
                            "facility_gender": 3,
                            "num_inmates_rated_for": row["num_inmates_rated_for"]
                        }

                    else:
                        print("AAAA")

                    success = True


            if zip_error:
                if zip5 not in removed_zips:
                    removed_zips.append(zip5)

            if success:
                writer.writerow(land_info)

                # if zip_error:
                #     break

with open("zips_removed.txt", "a") as f:
    f.write(str(removed_zips))
    f.write("\n")
    f.write(str(wrong_state))

print(removed_zips)
print("")
print(json.dumps(wrong_state, indent=2))
