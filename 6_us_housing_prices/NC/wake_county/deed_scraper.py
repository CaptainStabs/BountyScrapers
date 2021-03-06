from lxml.html import fromstring
import requests
import csv

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}


first_page = requests.request("GET", "http://rodcrpi.wakegov.com/booksweb/genextsearch.aspx", headers=headers)

parser = fromstring(first_page.text)

viewstate_list = []
viewstate_list.append(parser.xpath('//*[@id="__VIEWSTATE"]/@value')[0])

for i in range(1, 24):
    viewstate_list.append(parser.xpath(f'//*[@id="__VIEWSTATE{i}"]/@value')[0])


event_validation = parser.xpath('//*[@id="__EVENTVALIDATION"]/@value')
view_state_generator = parser.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')
book = "007722"
page = "00137"

payload= f'RadScriptMgrMaster_TSM=%3B%3BSystem.Web.Extensions%2C%20Version%3D4.0.0.0%2C%20Culture%3Dneutral%2C%20PublicKeyToken%3D31bf3856ad364e35%3Aen-US%3Aba1d5018-bf9d-4762-82f6-06087a49b5f6%3Aea597d4b%3Ab25378d2%3BTelerik.Web.UI%2C%20Version%3D2020.3.1021.40%2C%20Culture%3Dneutral%2C%20PublicKeyToken%3D121fae78165ba3d4%3Aen-US%3A19ea68a6-ea7d-4bf3-ac58-3ac1f9c656cf%3A16e4e7cd%3Af7645509%3A24ee1bba%3A33715776%3Ae330518b%3A88144a7a%3A1e771326%3A8e6f0d33%3A1f3a7489%3Ac128760b%3A874f8ea2%3Ab2e06756%3A19620875%3A92fe8ea0%3Afa31b949%3Af46195d3%3A4877f69a%3A490a9d4e%3Abd8f85e4%3A2003d0b8%3Aaa288e2d%3A258f1c72%3Aed16cbdc%3Ab7778d6c&__EVENTARGUMENT=&__EVENTTARGET=&__EVENTVALIDATION={event_validation}&__LASTFOCUS=&__VIEWSTATE={viewstate_list[0]}&__VIEWSTATE1={viewstate_list[1]}&__VIEWSTATE2={viewstate_list[2]}&__VIEWSTATE3={viewstate_list[3]}&__VIEWSTATE4={viewstate_list[4]}&__VIEWSTATE5={viewstate_list[5]}&__VIEWSTATE6={viewstate_list[6]}&__VIEWSTATE7={viewstate_list[7]}&__VIEWSTATE8={viewstate_list[8]}&__VIEWSTATE9={viewstate_list[9]}&__VIEWSTATE10={viewstate_list[10]}&__VIEWSTATE11={viewstate_list[11]}&__VIEWSTATE12={viewstate_list[12]}&__VIEWSTATE13={viewstate_list[13]}&__VIEWSTATE14={viewstate_list[14]}&__VIEWSTATE15={viewstate_list[15]}&__VIEWSTATE16={viewstate_list[16]}&__VIEWSTATE17={viewstate_list[17]}&__VIEWSTATE18={viewstate_list[18]}&__VIEWSTATE19={viewstate_list[19]}&__VIEWSTATE20={viewstate_list[20]}&__VIEWSTATE21={viewstate_list[21]}&__VIEWSTATE22={viewstate_list[22]}&__VIEWSTATE23={viewstate_list[23]}&__VIEWSTATEFIELDCOUNT=24&__VIEWSTATEGENERATOR={view_state_generator}&ctl00%24ContentPlaceHolder1%24RadCboAddlDocType=&ctl00%24ContentPlaceHolder1%24RadCboDocType=All%20Document%20Types&ctl00%24ContentPlaceHolder1%24RadCboGranteeType=Both&ctl00%24ContentPlaceHolder1%24RadCboGrantorType=Both&ctl00%24ContentPlaceHolder1%24RadCboGuideMe=How%20do%20I%3F&ctl00%24ContentPlaceHolder1%24RadCboSearchType=Standard&ctl00%24ContentPlaceHolder1%24RadTextBook={book}&ctl00%24ContentPlaceHolder1%24RadTextGrantee=&ctl00%24ContentPlaceHolder1%24RadTextGrantor=&ctl00%24ContentPlaceHolder1%24RadTextGuideMe=&ctl00%24ContentPlaceHolder1%24RadTextPage={page}&ctl00%24ContentPlaceHolder1%24RadTextRecordedAfter=&ctl00%24ContentPlaceHolder1%24RadTextRecordedBefore=&ctl00%24ContentPlaceHolder1%24btnExtSearch=Search&ctl00_ContentPlaceHolder1_RadCboAddlDocType_ClientState=&ctl00_ContentPlaceHolder1_RadCboDocType_ClientState=&ctl00_ContentPlaceHolder1_RadCboGranteeType_ClientState=&ctl00_ContentPlaceHolder1_RadCboGrantorType_ClientState=&ctl00_ContentPlaceHolder1_RadCboGuideMe_ClientState=&ctl00_ContentPlaceHolder1_RadCboSearchType_ClientState=&ctl00_ContentPlaceHolder1_RadTextBook_ClientState=%7B%22enabled%22%3Atrue%2C%22emptyMessage%22%3A%22%22%2C%22validationText%22%3A%22{book}%22%2C%22valueAsString%22%3A%22{book}%22%2C%22lastSetTextBoxValue%22%3A%22{book}%22%7D&ctl00_ContentPlaceHolder1_RadTextGrantee_ClientState=%7B%22enabled%22%3Atrue%2C%22emptyMessage%22%3A%22%22%2C%22validationText%22%3A%22%22%2C%22valueAsString%22%3A%22%22%2C%22lastSetTextBoxValue%22%3A%22%22%7D&ctl00_ContentPlaceHolder1_RadTextGrantor_ClientState=%7B%22enabled%22%3Atrue%2C%22emptyMessage%22%3A%22%22%2C%22validationText%22%3A%22%22%2C%22valueAsString%22%3A%22%22%2C%22lastSetTextBoxValue%22%3A%22%22%7D&ctl00_ContentPlaceHolder1_RadTextGuideMe_ClientState=%7B%22enabled%22%3Atrue%2C%22emptyMessage%22%3A%22%22%2C%22validationText%22%3A%22%22%2C%22valueAsString%22%3A%22%22%2C%22lastSetTextBoxValue%22%3A%22%22%7D&ctl00_ContentPlaceHolder1_RadTextPage_ClientState=%7B%22enabled%22%3Atrue%2C%22emptyMessage%22%3A%22%22%2C%22validationText%22%3A%22{page}%22%2C%22valueAsString%22%3A%22{page}%22%2C%22lastSetTextBoxValue%22%3A%22{page}%22%7D&ctl00_ContentPlaceHolder1_RadTextRecordedAfter_ClientState=%7B%22enabled%22%3Atrue%2C%22emptyMessage%22%3A%22%22%2C%22validationText%22%3A%22%22%2C%22valueAsString%22%3A%22%22%2C%22lastSetTextBoxValue%22%3A%22%22%7D&ctl00_ContentPlaceHolder1_RadTextRecordedBefore_ClientState=%7B%22enabled%22%3Atrue%2C%22emptyMessage%22%3A%22%22%2C%22validationText%22%3A%22%22%2C%22valueAsString%22%3A%22%22%2C%22lastSetTextBoxValue%22%3A%22%22%7D&ctl00_ContentPlaceHolder1_RadWindowManagerSort_ClientState=&ctl00_RadTabStripMaster_ClientState=%7B%22selectedIndexes%22%3A%5B%220%22%5D%2C%22logEntries%22%3A%5B%5D%2C%22scrollState%22%3A%7B%7D%7D'

with open("test.html", "w") as f:
    f.write(requests.request("POST", "http://rodcrpi.wakegov.com/booksweb/GenExtSearch.aspx", headers=headers, data=payload).text)
