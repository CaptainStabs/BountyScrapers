import requests
from lxml.html import fromstring
from dateutil import parser as dateparser

def get_deed(book, page):
    s = requests.Session()

    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Cookie': 'ASP.NET_SessionId=egggbv3gtu4lztuwve0ytdlv'
    }

    s.headers.update(headers)

    deed_url = f"http://rodweb.co.durham.nc.us/RealEstate/SearchDetail.aspx?bk={book}&pg={page}&type=BkPg"
    response = s.request("GET", deed_url)


    if "Click here to acknowledge the disclaimer and enter the site." in response.text:
        print("AAA")
        parser = fromstring(response.text)

        # Get the aspx validators from the html response
        event_validation = parser.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
        view_state = parser.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
        view_state_generator = parser.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0]

        # Add the validators to the payload
        payload= f'__EVENTARGUMENT=&__EVENTTARGET=ctl00%24cph1%24lnkAccept&__EVENTVALIDATION={event_validation}&__VIEWSTATE={view_state}&__VIEWSTATEGENERATOR={view_state_generator}'

        # Send the payload to the server, accepting the disclaimer
        response = s.request("POST", deed_url, data=payload)
        # print(response.headers)

    parser = fromstring(response.text)

    deed_info = {
        "sale_date": str(parser.xpath('//*[@id="ctl00_cphNoMargin_f_oprTab_tmpl0_documentInfoList_ctl00_DataLabel3"]/text()')[0]),
        "buyer_name": " ".join(str(parser.xpath('//*[@id="ctl00_cphNoMargin_f_oprTab_tmpl0_DataList11_ctl00_lblGrantorLastName"]/text()')[0]).split().upper().strip()),
        "seller_name": " ".join(str(parser.xpath('//*[@id="ctl00_cphNoMargin_f_oprTab_tmpl0_Datalist1_ctl00_lblGranteeLastName/text()')[0]).split().upper().strip()),
    }

    print(deed_info)

    return deed_info

get_deed("005923", "000600")
