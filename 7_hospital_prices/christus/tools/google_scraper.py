import googlesearch as google
import csv
from tqdm import tqdm

columns = ["cms_certification_num","name","address","city","state","zip5","beds","phone_number","homepage_url","chargemaster_url","last_edited_by_username"]
with open("updated-hospitals.csv", "a") as output_csv:
    writer = csv.DictWriter(output_csv, fieldnames=columns)
    # writer.writeheader()
    with open("hospitals.csv", "r") as input_csv:
        reader = csv.DictReader(input_csv)

        for row in tqdm(reader):
            search_query = " ".join([row["name"], row["address"], row["city"]])
            ignored_domains = ["christushealth.org"]
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
                "chargemaster_url": "https://www.christushealth.org/patient-resources/pricing-transparency",
                "last_edited_by_username": "captainstabs"
            }

            # print(search_query)
            for results in google.search(search_query, tld="com", lang="en", num=1, start=0, stop=1, pause=0.1):
                # print("All result: " + results
                # print("   All result: " + results)

                if any(ignored_domain in results for ignored_domain in ignored_domains):
                    info["homepage_url"] = results


            writer.writerow(info)
