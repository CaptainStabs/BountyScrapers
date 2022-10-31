import pandas as pd

df = pd.read_html("https://gis.hcpafl.org/propertysearch/#/parcel/basic/172714001000000092600U")
print(df)
