import requests
from lxml.html import fromstring
import datetime


headers = {
  'Upgrade-Insecure-Requests': '1',
  'DNT': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-User': '?1',
  'Sec-Fetch-Dest': 'document',
  'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'Cookie': 'ASP.NET_SessionId=jif2ft4iolkxeifpsengcvhj; DISCLAIMER=1'
}

headers2 = {
  'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'Upgrade-Insecure-Requests': '1',
  'DNT': '1',
  'Content-Type': 'application/x-www-form-urlencoded',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-User': '?1',
  'Sec-Fetch-Dest': 'document',
  'Cookie': 'ASP.NET_SessionId=jif2ft4iolkxeifpsengcvhj; DISCLAIMER=1'
}


s = requests.Session()
s.headers.update(headers)
#
# # Get the disclaimer validation ID
# url = "https://publicaccess.columbusga.org/Search/Disclaimer.aspx?FromUrl=../search/advancedsearch.aspx?mode=advanced"
#
# disclaimer_page = s.request("GET", url)
#
#
# parser = fromstring(disclaimer_page.text)



url = "https://publicaccess.columbusga.org/search/advancedsearch.aspx?mode=advanced"

# Get search page
response = s.request("GET", url)
# parser = fromstring(response.text)

with open("1.html", "w") as f:
    f.write(response.text)

# # Needed to progress from disclaimer page to search page
# view_state = parser.xpath('//*[@id="__VIEWSTATE"]/@value')
# view_state_generator = parser.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')
# event_validation = parser.xpath('//*[@id="__EVENTVALIDATION"]/@value')
#
# payload= '__EVENTVALIDATION={}&__VIEWSTATE={}&__VIEWSTATEGENERATOR={}&action=&btAgree=&hdURL=..%2Fsearch%2Fadvancedsearch.aspx%3Fmode%3Dadvanced'.format(event_validation, view_state, view_state_generator)
#
# response = s.request("POST", url, data=payload)
# with open("search_page.html", "w") as f:
#     f.write(response.text)

parser = fromstring(response.text)


event_validation = parser.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
view_state = parser.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
view_state_generator = parser.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0]
# print(event_validation)

# After disclaimer page
start_date = datetime.date(2020, 1, 1)
end_date = datetime.date(2021, 12, 31)
delta = datetime.timedelta(days=5)

while start_date <= end_date:
    ctl101_cal1 = start_date.strftime('%Y-%m-%d')
    ctl101_cal1_dateinput = str(start_date.strftime('%m/%d/%Y')).replace("/", "%2F")

    start_date += delta
    end_search_date_cal1 = start_date.strftime('%Y-%m-%d')
    end_search_date_dateinput = str(start_date.strftime('%m/%d/%Y')).replace("/", "%2F")

    payload= f'AkaCfgResults%24hdPins=&PageNum=1&PageSize=1&SortBy=PARID&SortDir=%20asc&__EVENTARGUMENT=&__EVENTTARGET=&__EVENTVALIDATION={event_validation}&__VIEWSTATE={view_state}&__VIEWSTATEGENERATOR={view_state_generator}&ctl01%24cal1={ctl101_cal1}&ctl01%24cal1%24dateInput={ctl101_cal1_dateinput}&ctl01%24cal2={end_search_date_cal1}&ctl01%24cal2%24dateInput={end_search_date_dateinput}&ctl01_cal1_ClientState=%7B%22minDateStr%22%3A%221900-01-01-00-00-00%22%2C%22maxDateStr%22%3A%222099-12-31-00-00-00%22%7D&ctl01_cal1_calendar_AD=%5B%5B1900%2C1%2C1%5D%2C%5B2099%2C12%2C30%5D%2C%5B2022%2C1%2C11%5D%5D&ctl01_cal1_calendar_SD=%5B%5D&ctl01_cal1_dateInput_ClientState=%7B%22enabled%22%3Atrue%2C%22emptyMessage%22%3A%22%22%2C%22validationText%22%3A%22{ctl101_cal1}-00-00-00%22%2C%22valueAsString%22%3A%22{ctl101_cal1}-00-00-00%22%2C%22minDateStr%22%3A%221900-01-01-00-00-00%22%2C%22maxDateStr%22%3A%222099-12-31-00-00-00%22%2C%22lastSetTextBoxValue%22%3A%2201%2F01%2F2020%22%7D&ctl01_cal2_ClientState=%7B%22minDateStr%22%3A%221900-01-01-00-00-00%22%2C%22maxDateStr%22%3A%222099-12-31-00-00-00%22%7D&ctl01_cal2_calendar_AD=%5B%5B1900%2C1%2C1%5D%2C%5B2099%2C12%2C30%5D%2C%5B2022%2C1%2C11%5D%5D&ctl01_cal2_calendar_SD=%5B%5D&ctl01_cal2_dateInput_ClientState=%7B%22enabled%22%3Atrue%2C%22emptyMessage%22%3A%22%22%2C%22validationText%22%3A%22{end_search_date_cal1}-00-00-00%22%2C%22valueAsString%22%3A%22{end_search_date_cal1}-00-00-00%22%2C%22minDateStr%22%3A%221900-01-01-00-00-00%22%2C%22maxDateStr%22%3A%222099-12-31-00-00-00%22%2C%22lastSetTextBoxValue%22%3A%22{end_search_date_dateinput}%22%7D&hdAction=&hdCriteria=salesdate%7C{ctl101_cal1_dateinput}~{end_search_date_dateinput}&hdCriteriaGroup=&hdCriteriaLov=&hdCriteriaTypes=C%7CC%7CC%7CN%7CC%7CC%7CN%7CD%7CC%7CC%7CN%7CN%7CN%7CN&hdCriterias=Book%7Cluc%7CClass%7Csfla%7Cnbhd%7CPage%7Cprice%7Csalesdate%7Csaletype%7CSaleValid%7Ccom_sf%7Cstories%7Cyr_com%7Cyr_buitl&hdIndex=1&hdLastState=1&hdLink=&hdListType=&hdName=&hdReset=&hdSearchType=AdvSearch&hdSelectAllChecked=false&hdSelected=&hdSelectedQuery=0&hdTaxYear=&mode=&sCriteria=0&searchOptions%24hdBeta=&selSortBy=PARID&selSortDir=%20asc&txCriterias=8&txtCrit={ctl101_cal1_dateinput}&txtCrit2={end_search_date_dateinput}'
    print(payload)
    # s.headers.update(headers2)
    search_results = s.request("POST", url, data=payload)

    parser = fromstring(search_results.text)

    print(parser.xpath('//*[@id="searchResults"]/tbody/tr[3]/td[2]/div/text()'))
    with open("search_results.html", "w") as f:
        f.write(search_results.text)

    break
