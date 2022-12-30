import requests 

headers = {
  'Cookie': 'ARRAffinity=8463e5429e576ba59e7a005d9e61f8d75b68f3275b62f9ed84bc27a0aadccf59; ARRAffinitySameSite=8463e5429e576ba59e7a005d9e61f8d75b68f3275b62f9ed84bc27a0aadccf59'
}

r = requests.head("https://www.christushealth.org/-/media/patient-resources/pricing-transparency/2022-machine-readable/720408984_coushattahealthcarecenter_standardcharges.ashx")

print(r.status_code)

from urllib.parse import urlparse


def test():
    a = urlparse("/sitecore/service/notfound.aspx")
    return all([a.scheme, a.netloc])

print(test())
test()