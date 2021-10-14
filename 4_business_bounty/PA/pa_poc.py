import requests
from lxml.html import fromstring

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

# Get search page
url = "https://www.corporations.pa.gov/search/corpsearch"
response = requests.request("GET", url)

# Parse raw html with lxml
parser = fromstring(response.text)

event_validation = parser.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
view_state = parser.xpath('//*[@id="__VIEWSTATE"]/@value')[0]

# Setup payload
payload = {
    '__EVENTARGUMENT': '',
    '__EVENTTARGET': '',
    '__EVENTVALIDATION': event_validation,
    '__VIEWSTATE': view_state,
    'ctl00$MainContent$btnSearch': 'Search',
    'ctl00$MainContent$ddlSearchType': '1',
    'ctl00$MainContent$txtSearchTerms': '710774'
}

# Get "Select Business Entity page"
result_page = requests.request("POST", url, data=payload)

with open("test.html", "w") as f:
    f.write(result_page.text)

# Get view stuff from this page, and buttons daat
result_parser = fromstring(result_page.text)

# Get aspx junk
event_validation = parser.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
view_state = parser.xpath('//*[@id="__VIEWSTATE"]/@value')[0]

payload = {
    '__EVENTARGUMENT': '',
    '__EVENTTARGET': 'ctl00$MainContent$gvResults$ctl02$lnkBEName',
    '__EVENTVALIDATION': event_validation,
    '__VIEWSTATE': view_state
}

business_page = requests.request("POST", url, headers=headers, data=payload)
with open("response")
business_parser = fromstring(business_page.text)


print("Name: " + str(business_parser.xpath('//*[@id="gvBusinessNameHistory"]/tr/td[1]/text()')))
print(business_parser.xpath('//*[@id="MainContent_lblTitleOrder"]/text()'))
