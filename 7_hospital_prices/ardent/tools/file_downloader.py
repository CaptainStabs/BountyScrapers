import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

with open("./csvs/homepages.csv", "r") as f:
    with open("hospital_home_source.csv", "a") as output_csv:
        for line in tqdm(f, total=29):
            line = line.split(",")
            hospital_name = line[0]
            url = line[1].replace("\n", "")

            # url = f"https://coc.ardenthealthservices.com/2022/oklahoma/2022_{hospital_name}_standardcharges.txt"

            try:
                r = requests.request("GET", url)
                if r.status_code == 404:
                    print(hospital_name, url)
                elif "404" in r:
                    print(hospital_name, url)
            except requests.exceptions.ConnectionError:
                print(line[0])

            soup = BeautifulSoup(r.text, "html.parser")

            for link in soup.findAll("a"):
                if link.get('href') is None:
                    continue
                if not link["href"].startswith('https://coc.ardenthealthservices.com/2022'):
                    continue

                output_csv.write(",".join([hospital_name, url, link["href"]]) + "\n")

                with open("./downloads/" + link["href"].split("/")[-1], "w") as f_out:
                    f_out.write(requests.get(link["href"]).text)
