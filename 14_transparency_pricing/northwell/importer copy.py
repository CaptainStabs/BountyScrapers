import os
from tqdm import tqdm

folder = 'F:\\_Bounty\\northwell\\output_files\\'
for file in os.listdir(folder):
    print(file)
    os.system(f'cd /D G:\\transparency-in-pricing & dolt table import -u rate "{folder}{file}"')
os.system(f'cd /D G:\\transparency-in-pricing & dolt table import -u hospital C:\\Users\\adria\\github\\BountyScrapers\\14_transparency_pricing\\northwell\\hopsital_finished_removed.csv')