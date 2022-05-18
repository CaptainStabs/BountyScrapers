import os

for file in os.listdir("./pdfs/"):
    file = os.path.join("./pdfs/", file)
    os.rename(file, file[:-4])
