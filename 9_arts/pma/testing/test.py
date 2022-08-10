import requests
import json
#
# with open("test.json", "w") as f:
#     r = requests.get("https://hackathon.philamuseum.org/api/v0/collection/object?query=1&api_token=jnFV09XMKDJ0yVYrcQd3si72VFN4EUeM15B479G6RkMfiu4BstY2GuaR19kI", verify=False)
#     json.dump(r.json(), f)
#

with open("test.json", "r") as f:
    j = json.load(f)
    print(j["Geography"].replace("\\u", "\\u"))
