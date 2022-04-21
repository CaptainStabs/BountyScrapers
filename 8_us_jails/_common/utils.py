import os

def remove_file(file):
    if os.path.exists("extracted_data.csv"):
        os.remove("extracted_data.csv")
