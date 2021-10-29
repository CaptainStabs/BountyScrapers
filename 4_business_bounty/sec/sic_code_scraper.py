import pandas as pd
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

tables = pd.read_html('https://en.m.wikipedia.org/wiki/Standard_Industrial_Classification#List')
df = tables[1]
df.iloc[0]['SIC Code'] = '0100'
df.to_csv('sic_codes_wikipedia.csv', index = False)
