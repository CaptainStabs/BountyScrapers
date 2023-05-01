import os
from tqdm import tqdm

folder = 'C:\\Users\\adria\\github\\BountyScrapers\\14_transparency_pricing\\bsw\\output_files\\'
for file in os.listdir(folder):
    print(file)
    os.system(f'cd /D F:\\_Bounty\\transparency-in-pricing\\ & dolt table import -u rate "{folder}{file}"')