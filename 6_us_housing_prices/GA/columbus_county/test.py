import requests

url = "https://publicaccess.columbusga.org/search/advancedsearch.aspx?mode=advanced"

payload='AkaCfgResults%24hdPins=&PageNum=1&PageSize=1&SortBy=PARID&SortDir=%20asc&__EVENTARGUMENT=&__EVENTTARGET=&__EVENTVALIDATION=WWa3YiM9iTgImi5n8IK5HRIRYl4BLcGlVAxfbhQ0hmYaTLWjS5EUMVnY2mLnRjIh78FTdwnMwh8ojlnYRv4muKPkiCn19xYoDR0A5ORsXwXGISYUpa8HTlriNO4OEG%2BLtHBdCPJV33jnklzPZgMHotxrm4s8q77h6hKEG0gJa2%2BSi7Lzc%2Fzl98GXOn4riE0mhudBsDlKMbzKS%2BoT13ilCMSgSAdnuYrBB5FMWBdV9Tq0%2BSny6I595H%2FylAacLo9muXhQHkZiHOH6l9Zs2t0qqeJjeBInKgNhmHotdWZ1OtVnDOLVu3T8q0FN%2Bu69VBSdvg89uWtqs4VUJw9vFc32twxNcBgHU%2Fvzvx8bU9UdUVyuno2YTjrwIlGTFJ0q9Wdvg6D8tfxVic4Ye1wjsaUJIPxBmUa7poTGminCsEE53%2BYieWmv4llTk7N9WmngVdQyqPXJtFPKN3H9ji0Q1v5i4tykinFFTnX%2F5NhVOSUM2dv0jCivPLxxrvlheIdqOUoqiX%2Fre4XLRArVNMkEKRXJFjn5ue1TR5J5Q3khxsebZpV0O82MTpNPumNjyUPrGBc1&__VIEWSTATE=1Hphl4%2FwMFPF0gKafJO6yb4X1ZPKUO4jLbNhBvTTNT20ShIx75WgpBzwzygmB%2FQWnSLkDFm38wLAK4yHv3qjZD%2FZGgQOQvmRQqKr2vsLp1XSJeBJG6slz%2FCl%2Fodw7rKIeIZnSCDN4BJ0g1jUla089DkbHLwzWl82ap7%2FxdA7duBf%2FG5I3bCarJrmWXtiyUElxaX9w8rXttP7wxclEXRXFssfuWJdX2lHaV7tiODV1%2B56hi9wysHDfjcDyK%2BYY%2F4yjJP1Caggk8v0teqyntL2KuMnWRUD8lA0dOPFNqgijL%2BDm7UfE6SKzjWIv7FOMhF1abqowpF6Zza%2F3a6YIto6EbpbjwF200W33JJSnM6MDYOY2jIi0%2FatuFv8pKTWzdQd2jDOa4abEgSIzH6gWMTSGDkl6PEtyOaMnTCGU2Hk4db8T3gvIYVwMnK6EXhZLKYDSihewqD2h5Y%2Fx8ZG9zgV8EPpzK7%2F67HRq3TWEmb7zCAGIN75aAHCLnfvcIin0Uef%2BSJi00ws%2BfRx5kbETruGUzB688v8GHOBEqycj6i2FocGbk%2BReOU7bEmeh6PmSIo1ZGH3UZeO%2Fkd0ZJRCr1EGR7FQcuwQvnjYflT8B0QgCbw%3D&__VIEWSTATEGENERATOR=81E50120&ctl01%24cal1=2020-01-01&ctl01%24cal1%24dateInput=01%2F01%2F2020&ctl01%24cal2=2020-01-06&ctl01%24cal2%24dateInput=01%2F06%2F2020&ctl01_cal1_ClientState=%7B%22minDateStr%22%3A%221900-01-01-00-00-00%22%2C%22maxDateStr%22%3A%222099-12-31-00-00-00%22%7D&ctl01_cal1_calendar_AD=%5B%5B1900%2C1%2C1%5D%2C%5B2099%2C12%2C30%5D%2C%5B2022%2C1%2C11%5D%5D&ctl01_cal1_calendar_SD=%5B%5D&ctl01_cal1_dateInput_ClientState=%7B%22enabled%22%3Atrue%2C%22emptyMessage%22%3A%22%22%2C%22validationText%22%3A%222020-01-01-00-00-00%22%2C%22valueAsString%22%3A%222020-01-01-00-00-00%22%2C%22minDateStr%22%3A%221900-01-01-00-00-00%22%2C%22maxDateStr%22%3A%222099-12-31-00-00-00%22%2C%22lastSetTextBoxValue%22%3A%2201%2F01%2F2020%22%7D&ctl01_cal2_ClientState=%7B%22minDateStr%22%3A%221900-01-01-00-00-00%22%2C%22maxDateStr%22%3A%222099-12-31-00-00-00%22%7D&ctl01_cal2_calendar_AD=%5B%5B1900%2C1%2C1%5D%2C%5B2099%2C12%2C30%5D%2C%5B2022%2C1%2C11%5D%5D&ctl01_cal2_calendar_SD=%5B%5D&ctl01_cal2_dateInput_ClientState=%7B%22enabled%22%3Atrue%2C%22emptyMessage%22%3A%22%22%2C%22validationText%22%3A%222020-01-06-00-00-00%22%2C%22valueAsString%22%3A%222020-01-06-00-00-00%22%2C%22minDateStr%22%3A%221900-01-01-00-00-00%22%2C%22maxDateStr%22%3A%222099-12-31-00-00-00%22%2C%22lastSetTextBoxValue%22%3A%2201%2F06%2F2020%22%7D&hdAction=&hdCriteria=salesdate%7C01%2F01%2F2020~01%2F06%2F2020&hdCriteriaGroup=&hdCriteriaLov=&hdCriteriaTypes=C%7CC%7CC%7CN%7CC%7CC%7CN%7CD%7CC%7CC%7CN%7CN%7CN%7CN&hdCriterias=Book%7Cluc%7CClass%7Csfla%7Cnbhd%7CPage%7Cprice%7Csalesdate%7Csaletype%7CSaleValid%7Ccom_sf%7Cstories%7Cyr_com%7Cyr_buitl&hdIndex=1&hdLastState=1&hdLink=&hdListType=&hdName=&hdReset=&hdSearchType=AdvSearch&hdSelectAllChecked=false&hdSelected=&hdSelectedQuery=0&hdTaxYear=&mode=&sCriteria=0&searchOptions%24hdBeta=&selSortBy=PARID&selSortDir=%20asc&txCriterias=8&txtCrit=&txtCrit2='
headers = {
  'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'Upgrade-Insecure-Requests': '1',
  'DNT': '1',
  'Content-Type': 'application/x-www-form-urlencoded',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-User': '?1',
  'Sec-Fetch-Dest': 'document',
  'Cookie': 'ASP.NET_SessionId=iped4f1hegf43ioknoq440bq; DISCLAIMER=1'
}

response = requests.request("POST", url, headers=headers, data=payload)

with open("test.html", "w") as f:
    f.write(response.text)
