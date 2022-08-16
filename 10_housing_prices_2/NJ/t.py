sale_date = "2099-01-01 00:00:00"
year = "2099"

if int(year) > 2022:
    sale_date = "19" + str(year)[2:] + sale_date.replace(year, "")
    print(sale_date)
