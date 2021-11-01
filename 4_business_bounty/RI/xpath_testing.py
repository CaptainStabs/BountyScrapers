import requests
import requests
from lxml.html import fromstring
from tqdm import tqdm
import csv
import os
import random
import pandas as pd
import usaddress
import time

url = "https://business.sos.ri.gov/CorpWeb/CorpSearch/CorpSummary.aspx?FEIN=000000005&SEARCH_TYPE=1"

response = requests.request("GET", url)
parser = fromstring(response.text)
print(str(parser.xpath('//*[@id="MainContent_lblResidentCity"]/text()')[0]).strip().rstrip(","))
print()
