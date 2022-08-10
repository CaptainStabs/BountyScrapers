import csv
import requests
from tqdm import tqdm

with open("F:\\museum-collections\\gonzo\\vam.csv", "r") as input_csv:
    cols = input_csv.readline().split(",")
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)

    data = csv.DictReader(input_csv, columns=cols)


with open("F:\museum-collections\gonzo\\fixed_vam.csv", "r") as input_csv:
