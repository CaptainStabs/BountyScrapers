import requests
import urllib.urlparse
import json

headers = {
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'DNT': '1',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty'
}

def upserve_scraper(webpage, headers):
    url = "https://d2evh2mef3r450.cloudfront.net/"

    parsed = urlparse(webpage) # Parse url
    web_path = parsed.path # Extract info from parse

    menu_url = url + web_path + ".json"

    menu_response = requests.get(menu_url, headers=headers)
    json.loads(menu_response.text)
