import requests

url = "http://onlinecollections.anchoragemuseum.org/apiv2/api/getPageData/"

payload = {"pageNumber":1,"seachType":"seeall"}

r = requests.post(url, data=payload)
print(r.text)
print(len(r.json()["artifacts"]))
print(r.text())
