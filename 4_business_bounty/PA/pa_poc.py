import requests
from lxml.html import fromstring
import pandas as pd
import usaddress

headers = {
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document'
}

'''
Step 1:
Need to get the first search page to search for ID
'''
# Get search page
url = "https://www.corporations.pa.gov/search/corpsearch"
response = requests.request("GET", url, headers=headers)

# Parse raw html with lxml
parser = fromstring(response.text)

event_validation = parser.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
view_state = parser.xpath('//*[@id="__VIEWSTATE"]/@value')[0]

# Setup payload
payload = {
    '__EVENTTARGET': '',
    '__EVENTVALIDATION': event_validation,
    '__VIEWSTATE': view_state,
    'ctl00$MainContent$btnSearch': 'Search',
    'ctl00$MainContent$ddlSearchType': '1',
    'ctl00$MainContent$txtSearchTerms': '710774'
}


# Get "Select Business Entity page"
result_page = requests.request("POST", url, data=payload)

# Get view stuff from this page, and buttons daat
result_parser = fromstring(result_page.text)

# Get aspx junk for step 2 request
event_validation_2 = result_parser.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
view_state_2 = result_parser.xpath('//*[@id="__VIEWSTATE"]/@value')[0]

'''
Step 2:
After searching, we need to get the view_state and event_validation once again
EVENTTARGET is from the result list link pointing to entity name
This step (finally) gets the actual business info
'''

payload = {
    '__EVENTARGUMENT': '',
    '__EVENTTARGET': 'ctl00$MainContent$gvResults$ctl02$lnkBEName',
    '__EVENTVALIDATION': event_validation_2,
    '__VIEWSTATE': view_state_2
}


business_page = requests.request("POST", url, headers=headers, data=payload)
business_parser = fromstring(business_page.text)

with open("test.html", 'w') as f:
    f.write(business_page.text)

print("Name: " + str(business_parser.xpath('//td[@align="left"]/text()')[0]).strip())
print(business_parser.xpath('/html/body/div/form/div[5]/div[2]/div[3]/div/div[5]/div[1]/table/tr[1]/td[2]/text()'))
# //*[@id="MainContent_pnlEntityDetails"]/div[3]/div/div[5]/div[1]/table/tbody/tr[3]/td[2]
df = pd.read_html(business_page.text)
entity_details = df[1]
info_dict = entity_details.set_index(0).to_dict()
print(info_dict)
raw_registered_address = info_dict[1]['Address']
print(raw_registered_address)
