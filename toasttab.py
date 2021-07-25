from bs4 import BeautifulSoup
import requests
import json

webpage = "https://www.toasttab.com/okiboru/v3"

# use python's requests module to fetch the webpage as plain html
html_page = requests.get(webpage).text

# use BeautifulSoup4 (bs4) to parse the returned html_page using BeautifulSoup4's html parser (html.parser)
soup = BeautifulSoup(html_page, "html.parser")

# for script in soup.find_all("script")[2]:
    # try:
    #     variable_dict = json.loads(script)["window.OO_GLOBALS"]
    #     print(variable_dict)
    # except json.decoder.JSONDecodeError:
    #     pass
    # print(script)
    # variable_dict = json.loads(script)["window.OO_GLOBALS"]
    # script = script.replace("window.OO_GLOBALS =", "")

print("   [*] Finding third script")
scripts = soup.find_all("script")[2]
# print("Scripts: " + str(scripts))

#  Regex? never heard of it
script = str(scripts).replace("window.OO_GLOBALS =", "").replace("<script>", "").replace("</script>", "").replace(";", "")
# print("Script: " + script)
data = json.loads(script)
restaurant_guid = data["restaurantGuid"]
print("   [*] Restaurant's guid: " + restaurant_guid)
