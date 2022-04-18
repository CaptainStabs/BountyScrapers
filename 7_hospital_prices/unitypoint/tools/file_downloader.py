import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

with open("unitypoint.csv", "r") as f:
    with open("hospital_home_source.csv", "a") as output_csv:
        for line in tqdm(f, total=13):
            line = line.split(",")
            url_part = line[0].replace(" ", "").lower()
            url = f"https://www.unitypoint.org/{url_part}/patient-charges-and-costs.aspx"

            # Get the page with the urls to HPI
            try:
                r = requests.request("GET", url)
                if r.status_code == 404:
                    print(url)
                elif "404" in r:
                    print(url)
            except requests.exceptions.ConnectionError:
                print(line[0])

            soup = BeautifulSoup(r.text, "html.parser")

            for link in soup.findAll("a"):
                if link.get('href') is None:
                    continue
                if not link["href"].startswith('https://search.hospitalpriceindex.com'):
                    continue

                print(link["href"])
                # output_csv.write(",".join([hospital_name, url, link["href"]]) + "\n")
                #
                # with open("./downloads/" + link["href"].text.replace(" ", ""), "w") as f_out:
                #     f_out.write(requests.get(link["href"]).text)
