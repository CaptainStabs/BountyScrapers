import os
from tqdm import tqdm

folder = 'C:\\Users\\adria\\github\\BountyScrapers\\14_transparency_pricing\\mercyone\\output_files\\other_schema\\'
for file in os.listdir(folder):
    print(file)
    os.system(f'cd /D F:\\_Bounty\\transparency-in-pricing\\ & dolt table import -u rate "{folder}{file}"')
os.system(f'cd /D F:\\_Bounty\\transparency-in-pricing\\ & dolt table import -u hospital C:\\Users\\adria\github\\BountyScrapers\\14_transparency_pricing\\mercyone\\hospitals.csv')