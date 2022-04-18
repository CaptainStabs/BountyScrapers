from xmlutils.xml2csv import xml2csv
import os

for filename in os.listdir("./input_files/"):
    if filename.endswith(".xml"):
        converter = xml2csv("./input_files/" + str(filename), f"./output_files/{filename.replace('.xml', '.csv')}")
        converter.convert(tag="row", delimiter=",", ignore="Rev")
