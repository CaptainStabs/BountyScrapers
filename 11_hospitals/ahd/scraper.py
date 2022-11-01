import requests
import csv
from lxml.html import fromstring
from tqdm import tqdm
import sys
import time
import webbrowser
import random


def solve_captcha(website, headers):
    webbrowser.open(website)
    input("\nPress enter to continue...")
    return requests.get(website, headers=headers).text


def get_user_agent():
    user_agents = user_agents = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
    ]

    user_agent = random.choice(user_agents)
    headers = {
        "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "host": "www.ahd.com",
    }
    return headers


columns = ["name", "ccn", "homepage_url", "state_code"]
with open("hospitals_state_code.csv", "r") as input_csv:
    total = line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("url_added.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        # writer.writeheader()

        for row in tqdm(reader, total=total):
            url = f"https://www.ahd.com/free_profile/{row['ccn']}/"
            t_headers = get_user_agent()
            r = requests.get(url, headers=t_headers).text

            with open("t.html", "w") as f:
                f.write(r)

            if "Please check the box or solve the question below to proceed." in r:
                r = solve_captcha(url, t_headers)

            if "You've reached your limit of free hospital profiles." in r:
                print("\nFree limit reached")
                break

            p = fromstring(r)
            homepage_url = p.xpath(
                '//*[@id="main"]/div[2]/table[1]/tr/td[1]/table/tr[3]/td[2]/a/@href'
            )
            if len(homepage_url):
                homepage_url = homepage_url[0]
            else:
                time.sleep(1)
                continue


            if homepage_url == "http://":
                time.sleep(1)
                continue

            data = {
                "name": row["name"],
                "ccn": row["ccn"],
                "homepage_url": homepage_url,
                "state_code": row["state_code"],
            }

            writer.writerow(data)
            # print(homepage_url)
            # sys.stdout.write("\r")
            # sys.stdout.write(str(homepage_url))
            # sys.stdout.flush()
            time.sleep(1)
            # with open("t.html", "w") as f:
            #     f.write(r)
