import os
from tqdm import tqdm

directory = "C:\\Users\\adria\\github\\BountyScrapers\\6_us_housing_prices\\OR\\marion\\files\\"
header_list = []
for file in tqdm(os.listdir(directory)):
    with open(directory + file, "r", encoding="utf-8") as f:
        header = f.readline().rstrip()

    if header not in header_list:
        header_list.append(header)
        folder = str(header_list.index(header)) + "\\"

        if not os.path.isdir(directory + folder):
            os.mkdir(directory + folder)

        os.rename(os.path.join(directory, file), os.path.join(directory, folder, file))

    else:
        folder = str(header_list.index(header)) + "\\"

        os.rename(os.path.join(directory, file), os.path.join(directory, folder, file))
