from bs4 import BeautifulSoup
import requests
import json

webpage = "https://www.toasttab.com/okiboru/v3"
url = "https://ws.toasttab.com/consumer-app-bff/v1/graphql" #  API endpoint

# use python's requests module to fetch the webpage as plain html
html_page = requests.get(webpage).text

# use BeautifulSoup4 (bs4) to parse the returned html_page using BeautifulSoup4's html parser (html.parser)
soup = BeautifulSoup(html_page, "html.parser")

# for script in soup.find_all("script")[2]:
    # try:
    #     variable_dict = json.loads(script)["window.OO_GLOBALS"]
    #     print(variable_dict)
    # except json.decoder.JSONDecodeError:
    #     pass
    # print(script)
    # variable_dict = json.loads(script)["window.OO_GLOBALS"]
    # script = script.replace("window.OO_GLOBALS =", "")

print("   [*] Finding third script")
scripts = soup.find_all("script")[2]
# print("Scripts: " + str(scripts))

#  Regex? never heard of it
script = str(scripts).replace("window.OO_GLOBALS =", "").replace("<script>", "").replace("</script>", "").replace(";", "")
# print("Script: " + script)
data = json.loads(script)
restaurant_guid = data["restaurantGuid"]
print("   [*] Restaurant's guid: " + restaurant_guid)


payload = json.dumps([
    {
        "operationName": "RESTAURANT_INFO",
        "variables": {
            "restaurantGuid": f"{restaurant_guid}"
        },
        "query": "query RESTAURANT_INFO($restaurantGuid: ID!) {\n  restaurantV2(guid: $restaurantGuid) {\n    ... on Restaurant {\n      guid\n      whiteLabelName\n      location {\n        city\n        state\n }\n  }\n    ... on GeneralError {\n      code\n      message\n      __typename\n    }\n    __typename\n  }\n}\n"
    }
])
headers = {
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'apollographql-client-name': 'takeout-web',
    'DNT': '1',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'toast-customer-access': '',
    'content-type': 'application/json',
    'accept': '*/*',
    'apollographql-client-version': '542',
    'Toast-Restaurant-External-ID': '59b9a2ee-a68e-46d9-a638-be93aa6ae27f',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty'
}

response = requests.request("POST", url, headers=headers, data=payload)

parsed = json.loads(response.text)
# print(json.dumps(parsed, indent=4))
restaurant_info = 
restaurant_name = parsed[0]["data"]["restaurantV2"]["whiteLabelName"]
city = parsed[0]["data"]["restaurantV2"]["location"]["city"].upper()

identifier = parsed[0]["data"]["restaurantV2"]["whiteLabelName"]
print(restaurant_name)
