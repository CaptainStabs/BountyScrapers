import requests
from lxml.html import fromstring



headers = {
    'Cookie': '.ASPXANONYMOUS=wxVoOcpA2AEkAAAAZDM3M2YwNTQtNThjMC00MTViLTg2ZWEtOTM2MWRmM2UxNzM50; ASP.NET_SessionId=q1hxvc45vlldco55p03jnw55; DotNetNukeAnonymous=a23253f0-aa99-4557-9dc8-7dbac4c50061; ViewHistory1397=R7049 314; cSearchFor1397=R7049 314; language=en-US; search-view1397=s'
}

def escape_insert(string):
    string = str(string).zfill(7)
    return string[:4] + "%2" + string[4:]

# for id in range(1, 9999999):
for id in range(52060324, 52060325):
    # id = 52069335
    id = escape_insert(id)


    url = f"http://www.gwinnettassessor.manatron.com/IWantTo/PropertyGISSearch/PropertyDetail.aspx?p=R{id}"


    response = requests.request("GET", url, headers=headers)
    
    land_info = {
        "state": "GA",
        "county": "GWINNETT",
        "source_url": url
    }

    parser = fromstring(response.text)


    # | physical_address | varchar(1024) | NO   | PRI |         |       |
    # | sale_date        | datetime      | NO   | PRI |         |       |
    # | property_type    | varchar(255)  | YES  |     |         |       |
    # | sale_price       | bigint        | NO   |     |         |       |
    # | seller_name      | varchar(1024) | YES  |     |         |       |
    # | buyer_name       | varchar(1024) | YES  |     |         |       |
    # | num_units        | int           | YES  |     |         |       |
    # | year_built       | int           | YES  |     |         |       |
    # | source_url       | varchar(2048) | YES  |     |         |       |
    # | book             | int           | YES  |     |         |       |
    # | page             | int           | YES  |     |         |       |
    # +------------------+---------------+------+-----+---------+-------+

    if not parser.xpath('//*[@id="lxT1385"]/p/text()'):

        land_info["property_id"] = parser.xpath('//*[@id="lxT1385"]/table/tbody/tr[2]/td/text()')[0]
        land_info["property_type"] = parser.xpath('//*[@id="lxT1385"]/table/tbody/tr[5]/td/text()')[0]

        land_info["physical_address"] = parser.xpath('//*[@id="lxT1385"]/table/tbody/tr[4]/td/text()')[0]

        transfer_table = parser.xpath('//*[@id="lxT1696"]/table/tbody/tr')
        print(transfer_table)

        for tr in transfer_table:
            print("A")
            print(tr.xpath('//td/text()'))
