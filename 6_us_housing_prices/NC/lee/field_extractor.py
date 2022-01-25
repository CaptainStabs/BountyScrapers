import os

directory = ".\\input_files\\"
with open("fields.txt", "a") as output:
    for file in os.listdir(directory):
        fields = []
        with open(directory +  file, "r") as f:
            first_line = f.readline()
            output.write(str(first_line))
