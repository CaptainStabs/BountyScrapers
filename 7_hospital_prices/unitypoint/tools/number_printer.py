import os

for file in os.listdir("./output_files/"):
    print(f'"{file.split("_")[0]}":')
