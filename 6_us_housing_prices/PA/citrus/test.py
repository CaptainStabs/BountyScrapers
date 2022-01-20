from dateutil import parser
# year = 2022

sale_date = str(parser.parse("01-01-2075"))
year = sale_date.split("-")[0]
sale_date = "19" + str(year)[2:] + sale_date.replace(year, "")
print(sale_date)
