import requests

url = "http://rodweb.co.durham.nc.us/RealEstate/SearchDetail.aspx?bk=5923&pg=600&type=BkPg"

payload='LoginForm1_txtLogonName=&LoginForm1_txtLogonName_clientState=%7C0%7C01%7C%7C%5B%5B%5B%5B%5D%5D%2C%5B%5D%2C%5B%5D%5D%2C%5B%7B%7D%2C%5B%5D%5D%2C%2201%22%5D&LoginForm1_txtPassword=&LoginForm1_txtPassword_clientState=%7C0%7C01%7C%7C%5B%5B%5B%5B%5D%5D%2C%5B%5D%2C%5B%5D%5D%2C%5B%7B%7D%2C%5B%5D%5D%2C%2201%22%5D&RangeContextMenu_clientState=%5B%5B%5B%5Bnull%2Cnull%2Cnull%2Cnull%2C1%5D%5D%2C%5B%5B%5B%5B%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%5D%5D%2C%5B%5D%2C%5B%5D%5D%2C%5B%7B%7D%2C%5B%5D%5D%2Cnull%5D%5D%2Cnull%5D%2C%5B%7B%7D%2C%5B%7B%7D%2C%7B%7D%5D%5D%2Cnull%5D&__EVENTARGUMENT=&__EVENTTARGET=ctl00%24cph1%24lnkAccept&__EVENTVALIDATION=%2FwEdAAUYPJI1%2FHoeqom9Pc4d%2Bqhf4K3DppXWfyM2jA5SVFnKZelpzquvG%2FYFWErcLu0B1w%2FRX4voneI4VOxMlObPwzUUiOZklp0ZzYteOWw32i4ghEKeow%2Bt5ueZ7EuE74SYE%2Fqk3ljWITIiPfKxs9HxN8W7&__VIEWSTATE=%2FwEPDwUKMTkzMzM0NzE2OA9kFgJmD2QWAgICD2QWCgIDDw8WAh4HVmlzaWJsZWhkFgICBw8WAxYHDxYCHg5fZGF0YUtleUZpZWxkc2VkZBQrAAIWAh4LY2xpZW50U3RhdGUUKwABZGRkZBcAFgBkZGQCBQ9kFgICBQ8PFgIfAGhkZAILD2QWBGYPFCsAAmRkZAIBDxQrAAQUKwACZGRkZBYCHgF2Z2QCDQ8WAxYEZGQUKwACFgIeEGNvbGxlY3Rpb25zU3RhdGUFqwtbeycwJzpbW251bGwsbnVsbCxudWxsLG51bGwsIlRvZGF5IixudWxsLCJUT0RBWSIsIiIsIiIsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsXV0sJzEnOltbbnVsbCxudWxsLG51bGwsbnVsbCwiWWVzdGVyZGF5IixudWxsLCJZRVNURVJEQVkiLCIiLCIiLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbF1dLCcyJzpbW251bGwsbnVsbCxudWxsLG51bGwsIlRoaXMgV2VlayIsbnVsbCwiVEhJU1dFRUsiLCIiLCIiLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbF1dLCczJzpbW251bGwsbnVsbCxudWxsLG51bGwsIkxhc3QgV2VlayIsbnVsbCwiTEFTVFdFRUsiLCIiLCIiLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbF1dLCc0JzpbW251bGwsbnVsbCxudWxsLG51bGwsIlRoaXMgTW9udGgiLG51bGwsIlRISVNNT05USCIsIiIsIiIsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsXV0sJzUnOltbbnVsbCxudWxsLG51bGwsbnVsbCwiTGFzdCBNb250aCIsbnVsbCwiTEFTVE1PTlRIIiwiIiwiIixudWxsLG51bGwsbnVsbCxudWxsLG51bGxdXX0seyctMSc6W1tudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCwiLTEiXV0sJzAnOltbbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsIjAiXV0sJzEnOltbbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsIjEiXV0sJzInOltbbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsIjIiXV0sJzMnOltbbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsIjMiXV0sJzQnOltbbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsIjQiXV0sJzUnOltbbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsIjUiXV19XWRkD2QWBg9mFCsAAhQrAAIWBB4CTjFlHgJOOWVkZA8CARQrAAIUKwACFgQfBWUfBmVkZA8CAhQrAAIUKwACFgQfBWUfBmVkZA8CAxQrAAIUKwACFgQfBWUfBmVkZA8CBBQrAAIUKwACFgQfBWUfBmVkZA8CBRQrAAIUKwACFgQfBWUfBmVkZGRkAg8PZBYGAgIPDxYCHgFFZWRkAgoPZBYCAgIPZBYEAgIPZBYCAgMPEGRkFgBkAgMPZBYUAgMPPCsABQECFCsAAhYCHwIUKwABZGRkAgkPPCsABQECFCsAAhYCHwIUKwABZGRkAg8PPCsABQECFCsAAhYCHwIUKwABZGRkAhcPPCsABQECFCsAAhYCHwIUKwABZGRkAh8PEGRkFgFmZAIjDzwrAAUBAhQrAAIWAh8CFCsAAWRkZAIlDzwrAAUBAhQrAAIWAh8CFCsAAWRkZAIpDzwrAAUBAhQrAAIWAh8CFCsAAWRkZAIrDxBkZBYBZmQCLw88KwAFAQIUKwACFgIfAhQrAAFkZGQCCw9kFgICAg8WCRYCFgcPFgQeFWNvbHVtbnNJbnRlcm5hbEluaXRlZGgfAWVkZBQrAAIWBB8CPCsABAAfBAUtW3t9LHsnMCc6W1siZ3JpZEJhc2tldF9Ecm9wRG93blByb3ZpZGVyMSJdXX1dZGRkFwAWBRYCaBYEHgZERk5hbWUFDl9pbWdfTU9EVUxFX0lEHgZERlR5cGUFWlN5c3RlbS5TdHJpbmcsIG1zY29ybGliLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49Yjc3YTVjNTYxOTM0ZTA4ORYCaBYEHwkFEl9pbWdfRE9DVU1FTlRfVFlQRR8KBVpTeXN0ZW0uU3RyaW5nLCBtc2NvcmxpYiwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODkWAmgWBB8JBRJfaW1nX1NFTlRfVE9fUVVFVUUfCgVaU3lzdGVtLlN0cmluZywgbXNjb3JsaWIsIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1iNzdhNWM1NjE5MzRlMDg5FgJoFgQfCQUIRkVFVkFMVUUfCgVaU3lzdGVtLlN0cmluZywgbXNjb3JsaWIsIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1iNzdhNWM1NjE5MzRlMDg5FgJoFgQfCQUFTm90ZXMfCgVaU3lzdGVtLlN0cmluZywgbXNjb3JsaWIsIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1iNzdhNWM1NjE5MzRlMDg5ZA9kFhkPZhYCFgMWDh4CRjAFDUEyX1NFU1NJT05fSUQeBEJERjMFDFN5c3RlbS5JbnQzMh4EQkRGMAUNQTJfU0VTU0lPTl9JRB4DR0YxGwAAAAAAgFFAAQAAAB4OaGlkZGVuSW50ZXJuYWwLKYoBSW5mcmFnaXN0aWNzLldlYi5VSS5EZWZhdWx0YWJsZUJvb2xlYW4sIEluZnJhZ2lzdGljczQuV2ViLnYxMy4yLCBWZXJzaW9uPTEzLjIuMjAxMzIuMjI5NCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj03ZGQ1YzMxNjNmMmNkMGNiAR4Pcm93U3BhbkludGVybmFsZh4WaGlkZGVuQnlQYXJlbnRJbnRlcm5hbGgWAmQFCVNlc3Npb24gIxYCZGVkDwIBFgIWAxYQHwsFCEJBVENIX0lEHwwFDFN5c3RlbS5JbnQzMh8NBQhCQVRDSF9JRB4DR0YwBQxjZW50ZXJlZENlbGwfDhsAAAAAAIBRQAEAAAAfDwsrBAAfEGYfEWgWAmQFCVJlcXVlc3QgIxYCZGVkDwICFgIWAxYSHwwFD1N5c3RlbS5EYXRlVGltZR4ERkdGMAUXezA6TU0vZGQveXl5eSBoaDptbSB0dH0fEWgfCwULQUNUSU9OX1RJTUUfDwsrBAAfDhsAAAAAAEBgQAEAAAAfDQULQUNUSU9OX1RJTUUfEGYfEgUMY2VudGVyZWRDZWxsFgJkBQpEYXRlIEFkZGVkFgJkZWQPAgMWAhYDFgwfCwUJTU9EVUxFX0lEHw0FCU1PRFVMRV9JRB8OGwAAAAAAAGlAAQAAAB8PCysEAR8QZh8RaBYCZAUJTW9kdWxlIElkFgJkZWQPAgQWAhYDFgwfCwUNRE9DVU1FTlRfVFlQRR8NBQ1ET0NVTUVOVF9UWVBFHw4bAAAAAAAAaUABAAAAHw8LKwQBHxBmHxFoFgJkBQtBY3Rpb24gVHlwZRYCZGVkDwIFFgIWAxYMHwsFDVNFTlRfVE9fUVVFVUUfDQUNU0VOVF9UT19RVUVVRR8OGwAAAAAAAFRAAQAAAB8PCysEAR8QZh8RaBYCZAULRGVzdGluYXRpb24WAmRlZA8CBhYDFgofCwUOX2ltZ19NT0RVTEVfSUQfDhsAAAAAAAA%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l0aW5nQ29yZWQPZBYBD2YWAhYCFgIfAhQrAAEFC0NlbGxFZGl0aW5nZA9kFgEPZhYGHxQFDURPQ1VNRU5UX1RZUEUeA0NFMAUcZ3JpZEJhc2tldF9Ecm9wRG93blByb3ZpZGVyMR8CFCsAAWRkD2QWAQ9mFgIfAhQrAAEFHGdyaWRCYXNrZXRfRHJvcERvd25Qcm92aWRlcjFkZGRkFgJmDxYCFgcPFgIfAWVkZBQrAAEUKwACFgQfAjwrADMFAQspmAFJbmZyYWdpc3RpY3MuV2ViLlVJLkxpc3RDb250cm9scy5Ecm9wRG93bkRpc3BsYXlNb2RlLCBJbmZyYWdpc3RpY3M0LldlYi52MTMuMiwgVmVyc2lvbj0xMy4yLjIwMTMyLjIyOTQsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49N2RkNWMzMTYzZjJjZDBjYgICAsgBFwUDdHh0J2gqaB8EBUFbeycwJzpbW251bGwsbnVsbCxudWxsLG51bGwsbnVsbCwidHh0IiwidmFsIiwwLG51bGwsbnVsbCxudWxsXV19XWRkZBcAFgAPZBYBD2YUKwACFgIfAhQrAAtkZGRkZAUDdHh0BQN2YWxoZGRkZGQYBAUaY3RsMDAkSGVhZGVyMSRXZWJEYXRhTWVudTEPZWQFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYKBRVjdGwwMCRkbGdPcHRpb25XaW5kb3cFFmN0bDAwJFJhbmdlQ29udGV4dE1lbnUFHWN0bDAwJExvZ2luRm9ybTEkdHh0TG9nb25OYW1lBRxjdGwwMCRMb2dpbkZvcm0xJHR4dFBhc3N3b3JkBRpjdGwwMCRMb2dpbkZvcm0xJHJkb1B1YkNwdQUaY3RsMDAkTG9naW5Gb3JtMSRyZG9QdnRDcHUFGmN0bDAwJExvZ2luRm9ybTEkcmRvUHZ0Q3B1BRljdGwwMCRMb2dpbkZvcm0xJGJ0bkxvZ29uBRJjdGwwMCRfaWdfZGVmX2VwX24FEmN0bDAwJF9pZ19kZWZfZXBfZAUpY3RsMDAkTG9naW5Gb3JtMSRCYXNrZXQxJGdyaWRCYXNrZXQkY3RsMDAPFCsABAUDdHh0ZgL%2F%2F%2F%2F%2FDwL%2F%2F%2F%2F%2FD2QFFmN0bDAwJFJhbmdlQ29udGV4dE1lbnUPZWST3Xi5ZjsUak5849aNWE8X64E9ashyLwtieZCaccSOag%3D%3D&__VIEWSTATEGENERATOR=CA0B0334&ctl00%24LoginForm1%24logonType=rdoPubCpu&ctl00%24_IG_CSS_LINKS_=~%2Flocalization%2Fstyle.css%7C~%2Flocalization%2Fstyleforsearch.css%7C~%2Ffavicon.ico%7C~%2Flocalization%2FstyleFromCounty.css%7Cig_res%2FDefault%2Fig_texteditor.css%7Cig_res%2FDefault%2Fig_datamenu.css%7Cig_res%2FElectricBlue%2Fig_dialogwindow.css%7Cig_res%2FElectricBlue%2Fig_shared.css%7Cig_res%2FDefault%2Fig_shared.css&dlgOptionWindow_clientState=%5B%5B%5B%5Bnull%2C3%2Cnull%2Cnull%2C%22700px%22%2C%22550px%22%2C1%2C1%2C0%2C0%2Cnull%2C0%5D%5D%2C%5B%5B%5B%5B%5Bnull%2C%22Copy%20Options%22%2Cnull%5D%5D%2C%5B%5B%5B%5B%5B%5D%5D%2C%5B%5D%2Cnull%5D%2C%5Bnull%2Cnull%5D%2C%5Bnull%5D%5D%2C%5B%5B%5B%5B%5D%5D%2C%5B%5D%2Cnull%5D%2C%5Bnull%2Cnull%5D%2C%5Bnull%5D%5D%2C%5B%5B%5B%5B%5D%5D%2C%5B%5D%2Cnull%5D%2C%5Bnull%2Cnull%5D%2C%5Bnull%5D%5D%5D%2C%5B%5D%5D%2C%5B%7B%7D%2C%5B%5D%5D%2Cnull%5D%2C%5B%5B%5B%5Bnull%2Cnull%2Cnull%2Cnull%5D%5D%2C%5B%5D%2C%5B%5D%5D%2C%5B%7B%7D%2C%5B%5D%5D%2Cnull%5D%5D%2C%5B%5D%5D%2C%5B%7B%7D%2C%5B%5D%5D%2C%223%2C0%2C%2C%2C700px%2C550px%2C0%22%5D'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': 'ASP.NET_SessionId=egggbv3gtu4lztuwve0ytdlv'
}

response = requests.request("POST", url, headers=headers, data=payload)

# print(response.text)
print(response.headers)

with open("aaa.html", "w") as f:
    f.write(response.text)

if "Click here to acknowledge the disclaimer and enter the site." in response.text:
    print("AAAAAAAAA")
