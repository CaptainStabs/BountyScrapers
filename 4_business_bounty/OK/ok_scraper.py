import requests
from lxml.html import fromstring
from tqdm import tqdm



payload={}
headers = {
  'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'DNT': '1',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Sec-Fetch-Site': 'none',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-User': '?1',
  'Sec-Fetch-Dest': 'document'
}
columns = ["name", "business_type", "state_registered","street_registered","city_registered","zip5_registered", "corp_id"]

# for corp_id in tqdm(range(175, 9999999999)):
corp_id = 3512384626
url = f"https://www.sos.ok.gov/corp/corpInformation.aspx?id={corp_id}"
response = requests.request("GET", url, headers=headers, data=payload)
parser = fromstring(response.text)

status = parser.xpath('//*[@id="printDiv"]/dl[1]/dd[3]/text()')
business_info = {}

if "EXISTENCE" in str(status[0]).strip().upper():
    print(status[0].strip())
    name = str(parser.xpath('//*[@id="printDiv"]/h3/text()')[0]).strip().upper().replace("  ", " ")
    business_type_string = str(parser.xpath('//*[@id="printDiv"]/dl[1]/dd[4]/text()')[0]).strip().upper().replace("  ", " ")
    if "COOPERATIVE" in business_type_string:
        business_info["business_type"] = "COOP"
        print("      [?] Translated type 1: COOP")

    if "COOP " in business_type_string:
        business_info["business_type"] = "COOP"
        print("      [?] Translated type 2: COOP")
    if "CORP" in business_type_string:
        business_info["business_type"] = "CORPORATION"
        print("      [?] Translated type 1: CORPORATION")

    if "CORP " in business_type_string:
        business_info["business_type"] = "CORPORATION"
        print("      [?] Translated type 2: CORPORATION")

    if "CORPORATION" in business_type_string:
        business_info["business_type"] = "CORPORATION"
        print("      [?] Translated type 3: CORPORATION")

    if "DBA" in business_type_string:
        business_info["business_type"] = "DBA"
        print("      [?] Translated type: DBA")

    if "LIMITED LIABILITY COMPANY" in business_type_string:
        business_info["business_type"] = "LLC"
        print("      [?] Translated type 1: LLC")

    if "LLC" in business_type_string:
        business_info["business_type"] = "LLC"
        print("      [?] Translated type 2: LLC")

    if "L.L.C." in business_type_string:
        business_info["business_type"] = "LLC"
        print("      [?] Translated type 3: LLC")

    if "L.L.C" in business_type_string:
        business_info["business_type"] = "LLC"
        print("      [?] Translated type 4: LLC")

    if "NON-PROFIT" in business_type_string:
        business_info["business_type"] = "NONPROFIT"
        print("      [?] Translated type 1: NON-PROFIT")

    if "NONPROFIT" in business_type_string:
        business_info["business_type"] = "NONPROFIT"
        print("      [?] Translated type 2: NONPROFIT")

    if "PARTNERSHIP" in business_type_string:
        business_info["business_type"] = "PARTNERSHIP"
        print("      [?] Translated type: PARTNERSHIP")

    if "SOLE PROPRIETORSHIP" in business_type_string:
        business_info["business_type"] = "SOLE PROPRIETORSHIP"
        print("      [?] Translated type: SOLE PROPRIETORSHIP")

    if "TRUST" in business_type_string:
        business_info["business_type"] = "TRUST"
        print("      [?] Translated type: TRUST")

    if "INC " in business_type_string:
        business_info["business_type"] = "CORPORATION"
        print("      [?] Translated type 1: INC")

    if "INC" in business_type_string:
        business_info["business_type"] = "CORPORATION"
        print("      [?] Translated type 2: INC")

    if "INCORPORATED" in business_type_string:
        business_info["business_type"] = "CORPORATION"
        print("      [?] Translated type 3: INC")

    # if "LIMITED" in business_type_string:
    #     business_info["business_type"] = "LTD"
    #     print("      [?] Translaetd type1: LTD")

    if "LTD" in business_type_string:
        business_info["business_type"] = "LTD"
        print("      [?] Translaetd type 2: LTD")

    if "L.T.D" in business_type_string:
        business_info["business_type"] = "LTD"
        print("      [?] Translaetd type 3: LTD")


    print(business_type)
    print(name)


    # print(parser.xpath('//*[@id="printDiv"]/dl[1]/dd[3]/text()'))

    # print(response.text)
