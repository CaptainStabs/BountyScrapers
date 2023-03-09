import requests
from tqdm import tqdm

headers = {
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-platform': '"Windows"',
    'DNT': '1',
    'traceparent': '00-73f7bd412bfc4f7e9dac0d2caf81618b-f89d32e434b2484f-01',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'Request-Id': '|73f7bd412bfc4f7e9dac0d2caf81618b.f89d32e434b2484f',
    'Request-Context': 'appId=cid-v1:4f645746-2724-4071-b97d-f3dab98adc0e',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'host': 'developers.humana.com'
    }

def get_files(display_start, headers):
    url = f"https://developers.humana.com/syntheticdata/Resource/GetData?fileType=innetwork&sEcho=3&iColumns=3&sColumns=%2C%2C&iDisplayStart={display_start}&iDisplayLength=50&mDataProp_0=name&sSearch_0=&bRegex_0=false&bSearchable_0=false&mDataProp_1=modifiedDate&sSearch_1=&bRegex_1=false&bSearchable_1=false&mDataProp_2=sizeToDisplay&sSearch_2=&bRegex_2=false&bSearchable_2=false&sSearch=&bRegex=false&_=1673446650205"

    r = requests.request("GET", url, headers=headers)
    r = r.json()
    name_list = r["aaData"]
    return name_list


with open("files.txt", "a") as csvfile:
    for i in tqdm(range(0, 9400, 50)):
        names = get_files(i, headers)

        for name in names:
            csvfile.write(f"{name['name']}\n")
