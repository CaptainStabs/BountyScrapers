from utilities.utilities import get_proxy_cycle, get_open_proxy_cycle
import requests

proxy_cycle = get_open_proxy_cycle()
proxy = next(proxy_cycle)
print(proxy)

# response = requests.get("https://arc-sos.state.al.us/cgi/corpdetail.mbr/detail?page=number&num1=000001",  proxies={"http": proxy, "https": proxy})
# print(respsonse.status_code)
# print(next(get_proxy_cycle()))
# print(next(get_proxy_cycle()))
