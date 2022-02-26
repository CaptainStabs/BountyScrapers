import os

in_directory = "./fixed/cdm/"
with open("names.txt", "a") as out_f:
    for file in os.listdir(in_directory):
        out_f.write(f'"{file.split("-")[0]}": "",\n')
