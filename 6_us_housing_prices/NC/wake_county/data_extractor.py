import csv
from dateutil import parser


with open("RealEstData01112022.csv", "r") as input_csv:
    csv_reader = DictReader(input_csv)
