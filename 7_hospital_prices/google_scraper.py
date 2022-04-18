import googlesearch as google
import csv
from tqdm import tqdm

cdm = {
"110083":"https://www.piedmont.org/media/file/580566213_piedmont-atlanta-hospital_standardcharges.xls",
"110074":"https://www.piedmont.org/media/file/582179986_piedmont-athens-hospital_standardcharges.xls",
"110064":"https://www.piedmont.org/media/file/581685139_piedmont-columbus-regional-midtown-hospital_standardcharges.xls",
"110200":"https://www.piedmont.org/media/file/331216751_piedmont-columbus-regional-northside-hospital_standardcharges.xls",
"110215":"https://www.piedmont.org/media/file/582322328_piedmont-fayette-hospital_standardcharges.xls",
"110191":"https://www.piedmont.org/media/file/582200195_piedmont-henry-hospital_standardcharges.xls",
"110225":"https://www.piedmont.org/media/file/352228583_piedmont-mountainside-hospital_standardcharges.xls",
"110229":"https://www.piedmont.org/media/file/205077249_piedmont-newnan-hospital_standardcharges.xls",
"110018":"https://www.piedmont.org/media/file/582155150_piedmont-newton-hospital_standardcharges.xls",
"110091":"https://www.piedmont.org/media/file/300999841_piedmont-rockdale-hospital_standardcharges.xls",
"110046":"https://www.piedmont.org/media/file/824194264_piedmont-walton-hospital_standardcharges.xls",
}

columns = ["cms_certification_num","name","address","city","state","zip5","beds","phone_number","homepage_url","chargemaster_url","last_edited_by_username"]
with open("updated-hospitals.csv", "a") as output_csv:
    writer = csv.DictWriter(output_csv, fieldnames=columns)
    writer.writeheader()

    with open("hospitals.csv", "r") as input_csv:
        reader = csv.DictReader(input_csv)

        for row in tqdm(reader):
            try:
                search_query = str(row["name"]) + " " + str(row["city"])
                ignored_domains = ["piedmont.org"]
                remove_words = ["?mode=create"]
                # print("   [*] Loop start")
                info = {
                    "cms_certification_num": row["cms_certification_num"],
                    "name": row["name"],
                    "address": row["address"],
                    "city": row["city"],
                    "state": row["state"],
                    "zip5": row["zip5"],
                    "beds": row["beds"],
                    "phone_number": row["phone_number"],
                    "chargemaster_url": cdm[row["cms_certification_num"]],
                    "last_edited_by_username": "captainstabs"
                }


                for results in google.search(search_query, tld="com", lang="en", num=1, start=0, stop=1, pause=0.3):
                    # print("All result: " + results
                    # print("   All result: " + results)

                    if any(ignored_domain in results for ignored_domain in ignored_domains):
                        info["homepage_url"] = results

                writer.writerow(info)
            except KeyError:
                print(row)
