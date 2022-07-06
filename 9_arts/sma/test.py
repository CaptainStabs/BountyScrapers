import requests

url = "https://smaapi.unit.ku.edu/sma/fetch-object"

s = requests.Session()
s.headers.update({
    'host': 'smaapi.unit.ku.edu',
})
id = 3
p = "\r\n{\"objectID\":\"REP\"}".replace("REP", str(id))
print(p)
r = s.post(url, data=p)
print(r)
