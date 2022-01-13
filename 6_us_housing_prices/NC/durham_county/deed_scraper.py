import requests
from lxml.html import fromstring
from dateutil import parser as dateparser

def get_deed(book, page):
    s = requests.Session()

    headers = {
      'Content-Type': 'text/plain',
      'Cookie': 'ASP.NET_SessionId=egggbv3gtu4lztuwve0ytdlv'
    }

    s.headers.update(headers)

    response = s.request("GET", f"http://rodweb.co.durham.nc.us/RealEstate/SearchDetail.aspx?bk={book}&pg={page}&type=BkPg")

    if "Click here to acknowledge the disclaimer and enter the site." in response.text:
        parser = fromstring(response.text)
        event_validation = parser.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
        view_state = parser.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
        view_state_generator = parser.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0]
        with open("disclaimer.html", "w") as f:
            f.write(response.text)


        payload= f'LoginForm1_txtLogonName=&LoginForm1_txtLogonName_clientState=%7C0%7C01%7C%7C%5B%5B%5B%5B%5D%5D%2C%5B%5D%2C%5B%5D%5D%2C%5B%7B%7D%2C%5B%5D%5D%2C%2201%22%5D&LoginForm1_txtPassword=&LoginForm1_txtPassword_clientState=%7C0%7C01%7C%7C%5B%5B%5B%5B%5D%5D%2C%5B%5D%2C%5B%5D%5D%2C%5B%7B%7D%2C%5B%5D%5D%2C%2201%22%5D&RangeContextMenu_clientState=%5B%5B%5B%5Bnull%2Cnull%2Cnull%2Cnull%2C1%5D%5D%2C%5B%5B%5B%5B%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%5D%5D%2C%5B%5D%2C%5B%5D%5D%2C%5B%7B%7D%2C%5B%5D%5D%2Cnull%5D%5D%2Cnull%5D%2C%5B%7B%7D%2C%5B%7B%7D%2C%7B%7D%5D%5D%2Cnull%5D&__EVENTARGUMENT=&__EVENTTARGET=ctl00%24cph1%24lnkAccept&__EVENTVALIDATION={event_validation}&__VIEWSTATE={view_state}&__VIEWSTATEGENERATOR={view_state_generator}&ctl00%24LoginForm1%24logonType=rdoPubCpu&ctl00%24_IG_CSS_LINKS_=~%2Flocalization%2Fstyle.css%7C~%2Flocalization%2Fstyleforsearch.css%7C~%2Ffavicon.ico%7C~%2Flocalization%2FstyleFromCounty.css%7Cig_res%2FDefault%2Fig_texteditor.css%7Cig_res%2FDefault%2Fig_datamenu.css%7Cig_res%2FElectricBlue%2Fig_dialogwindow.css%7Cig_res%2FElectricBlue%2Fig_shared.css%7Cig_res%2FDefault%2Fig_shared.css&dlgOptionWindow_clientState=%5B%5B%5B%5Bnull%2C3%2Cnull%2Cnull%2C%22700px%22%2C%22550px%22%2C1%2C1%2C0%2C0%2Cnull%2C0%5D%5D%2C%5B%5B%5B%5B%5Bnull%2C%22Copy%20Options%22%2Cnull%5D%5D%2C%5B%5B%5B%5B%5B%5D%5D%2C%5B%5D%2Cnull%5D%2C%5Bnull%2Cnull%5D%2C%5Bnull%5D%5D%2C%5B%5B%5B%5B%5D%5D%2C%5B%5D%2Cnull%5D%2C%5Bnull%2Cnull%5D%2C%5Bnull%5D%5D%2C%5B%5B%5B%5B%5D%5D%2C%5B%5D%2Cnull%5D%2C%5Bnull%2Cnull%5D%2C%5Bnull%5D%5D%5D%2C%5B%5D%5D%2C%5B%7B%7D%2C%5B%5D%5D%2Cnull%5D%2C%5B%5B%5B%5Bnull%2Cnull%2Cnull%2Cnull%5D%5D%2C%5B%5D%2C%5B%5D%5D%2C%5B%7B%7D%2C%5B%5D%5D%2Cnull%5D%5D%2C%5B%5D%5D%2C%5B%7B%7D%2C%5B%5D%5D%2C%223%2C0%2C%2C%2C700px%2C550px%2C0%22%5D'

        response = s.request("POST", "http://rodweb.co.durham.nc.us/", data=payload)
        print(response.headers)

    parser = fromstring(response.text)

    deed_info = {
        "sale_date": str(parser.xpath('//*[@id="ctl00_cphNoMargin_f_oprTab_tmpl0_documentInfoList_ctl00_DataLabel3"]/text()')[0]),
        "buyer_name": " ".join(str(parser.xpath('//*[@id="ctl00_cphNoMargin_f_oprTab_tmpl0_DataList11_ctl00_lblGrantorLastName"]/text()')[0]).split().upper().strip()),
        "seller_name": " ".join(str(parser.xpath('//*[@id="ctl00_cphNoMargin_f_oprTab_tmpl0_Datalist1_ctl00_lblGranteeLastName/text()')[0]).split().upper().strip()),
    }

    return deed_info
