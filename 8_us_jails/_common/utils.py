import os

def remove_file(file="extracted_data.csv"):
    if os.path.exists(file):
        os.remove(file)
