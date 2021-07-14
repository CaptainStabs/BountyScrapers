import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from urllib.parse import urlparse
import os
import pandas as pd
import csv
import sys
import doltcli as dolt
from doltpy.cli.write import write_pandas
import json
from size_scraper import size_scraper

webpage = "https://fastfoodnutrition.org/smoothie-king"
identifier = "NATIONAL"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

parsed = urlparse(webpage) # Parse url
web_path = parsed.path # Extract info from parse
domain = parsed.netloc
scheme = parsed.scheme

web_path_split = web_path.split('/')
restaurant_name = web_path_split[1].upper().replace("-", " ")

print("    [*] Selecting Menus...")
db = dolt.Dolt("menus")
print("    [*] Switching to Master...")
db.checkout(branch="master")
print("    [*] Pulling remote")
db.pull(remote="dolt-origin")
branch_name = "add_" + web_path_split[1]
print("    [*] Created and checked out branch " + branch_name)
try:
    db.checkout(branch=branch_name, checkout_branch=True)
except Exception as error:
    print("      [!] Branch probably already exists, but I can't tell due to non-existant exceptions")
    print("        " + str(error))
    db.checkout(branch=branch_name)
    pass

# print("    [*] One last pull for fun")
# db.pull(remote="origin")

html_page = requests.get(webpage, headers=headers).text

print(restaurant_name)
ignored_list = [f"/weight-watchers", "/popular", "/discontinued", "/calculator"]
columns = ["name", "restaurant_name", "identifier", "calories", "fat_g", "cholesterol_mg", "sodium_mg", "carbohydrates_g", "fiber_g", "sugars_g", "protein_g"]

soup = BeautifulSoup(html_page, "html.parser")
#
# for ignored_words in ignored_list:
#     print(ignored_words)

# Extract every food item
try:
    os.remove("url_name.txt")
except:
    pass

for link in soup.findAll("a"):
    if link.get("href") is None:
        # print(link)
        continue
    if not link["href"].startswith(web_path):
        # print("href not startswith")
        # print(link)
        continue
    if any(ignored_words in link["href"] for ignored_words in ignored_list):
        print("Ignoring: " + link["href"])
        # print("fdjaskfhasdklh")
        continue
    print("link: " + link.get("href"))
    url = str(link["href"])
    with open("url_name.txt", "a+") as output:
        if url not in output.read():
            if url.count("/") > 1:
                output.write(url+"\n")

filename = restaurant_name.replace(" ", "_") + ".csv"


question_mark = False
with open("url_name.txt", "r") as input_file:
    print(" [*] Getting files")
    with open(filename, "a") as output:
        writer = csv.DictWriter(output, fieldnames=columns)
        if not os.path.isfile(filename) or os.stat(filename).st_size == 0:
            writer.writeheader()

        for line in input_file:
            line_list = line.split("/")
            line_url = line_list[-1]  # Could concat scheme + domain but im lazy
            info_url = webpage + "/" + line_url
            print("PAGE: " + info_url)

            food_name = line_url.upper().replace("-"," ") # For exporting
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            }
            info_html = requests.get(info_url.strip(), headers=headers)
            info_soup = BeautifulSoup(info_html.text, "html.parser")
            # with open("test2.html", "w", encoding="utf-8") as output:
            #     output.write(str(info_html.text))
            fail1 = False
            failed = False

            try:
                rows = info_soup.find("table").find_all("tr")
            except AttributeError as error:
                print(error)
                fail1 = True

            if not fail1:
                nutrition_facts = {}

                nutrition_facts["name"] = food_name.strip()
                nutrition_facts["restaurant_name"] = restaurant_name.strip()
                nutrition_facts["identifier"] = identifier.strip()
                # failed = False
                for row in rows:
                    cells = row.find_all("td")
                    try:
                        rn = cells[0].get_text().strip()
                        rd = cells[1].get_text().strip()
                    except IndexError:  # This happens when there are multiple sizes
                        with open("url.txt", "a") as url2:
                            for buttons in info_soup.findAll("a", {"class": "stub_box:"}):
                                url2.write(buttons.get("href") +"\n")
                                print("       [!] LNIKSKSKSK: " + buttons.get("href"))
                        print(cells)
                        failed = True
                        pass

                    if "?" in rd:
                        question_mark = True
                        bad_rn, bad_rd = rn, rd
                        rd = "40489"

                    if not failed:
                        if rn == "Calories":  # Needs to be exact match
                            nutrition_facts["calories"] = int(float(rd))
                            # print(nutrition_facts)

                        elif "Total Fat" in rn:
                            if "mg" in rd:
                                print("MG ALERT")
                                print(food_name, rn, rd)
                                rd_int = rd.replace("mg", "")
                                rd_converted = int(float(rd)) / 1000
                                nutrition_facts["fat_g"] = rd_converted.strip()

                                print(nutrition_facts)
                            else:
                                nutrition_facts["fat_g"] = int(float(rd.strip('g')))

                        elif "Carbohydrates" in rn:
                            if "mg" in rd:
                                print("MG ALERT")
                                print(food_name, rn, rd)
                                rd_int = rd.replace("mg", "")
                                rd_converted = int(float(rd)) / 1000
                                nutrition_facts["carbohydrates_g"] = rd_converted.strip()

                            else:
                                nutrition_facts["carbohydrates_g"] = int(float(rd.strip('g')))

                        elif "Protein" in rn:
                            if "mg" in rd:
                                print("MG ALERT")
                                print(food_name, rn, rd)
                                rd_int = rd.replace("mg", "")
                                rd_converted = int(float(rd)) / 1000
                                nutrition_facts["carbohydrates_g"] = rd_converted.strip()

                            else:
                                nutrition_facts["protein_g"] = int(float(rd.strip('g')))
                            # print(nutrition_facts)

                        elif "Sodium" in rn:
                            if "mg" in rd:
                                nutrition_facts["sodium_mg"] = int(float(rd.strip('mg')))
                            elif "g" in rd:
                                print("G ALERT")
                                print(food_name, rn, rd)
                                rd_int = rd.strip("g")
                                rd_converted = int(float(rd_int)) * 1000
                                nutrition_facts["sodium_mg"] = rd_converted.strip()

                        elif "Cholesterol" in rn:
                            if "mg" in rd:
                                nutrition_facts["cholesterol_mg"] = int(float(rd.strip('mg')))
                            elif "g" in rd:
                                print("G ALERT")
                                print(food_name, rn, rd)
                                rd_int = rd.strip("g")
                                rd_converted = int(float(rd_int)) * 1000
                                nutrition_facts["cholesterol_mg"] = rd_converted.strip()

                        elif "Fiber" in rn:
                            if "mg" in rd:
                                print("MG ALERT")
                                print(food_name, rn, rd)
                                rd_int = rd.replace("mg", "")
                                rd_converted = int(float(rd)) / 1000
                                nutrition_facts["fiber_g"] = rd_converted.strip()
                            elif "g" in rd:
                                nutrition_facts["fiber_g"] = int(float(rd.strip('g')))

                        elif "Sugars" in rn:
                            if "mg" in rd:
                                print("MG ALERT")
                                print(food_name, rn, rd)
                                rd_int = rd.replace("mg", "")
                                rd_converted = int(float(rd)) / 1000
                                nutrition_facts["sugars_g"] = rd_converted.strip()
                            else:
                                nutrition_facts["sugars_g"] = int(float(rd.strip('g')))

                if not failed:
                    writer.writerow(nutrition_facts)

                    # print(nutrition_facts)
                    # df = pd.DataFrame.from_dict(nutrition_facts)

                    # columns = ["name", "restaurant_name", "identifier", "calories", "fat_g", "cholesterol_mg", "sodium_mg", "carbohydrates_g", "fiber_g", "sugars_g", "protein_g"]
                    # dc = df.to_csv(columns=columns, index=False)


                    print("   [*] Writing to database...")
                    # write_pandas(dolt=db, table="menus", df=df, import_mode="create")

                    # print(df)
                    print("\n")

                    # break
                    # table_rows = table.find_all('tr')
                    # print(table_rows)

if question_mark:
    print(bad_rd, bad_rn)
    print("Replace 40489 with Null")

try:
    os.remove("url_name.txt")
except:
    pass

size_scraper(webpage, identifier, headers)
