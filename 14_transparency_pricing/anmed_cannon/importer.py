import os

folder = 'C:\\Users\\adria\\github\\BountyScrapers\\14_transparency_pricing\\anmed_cannon\\output_files\\'
for file in os.listdir(folder):
    print(file)
    os.system(f'cd /D F:\\_Bounty\\transparency-in-pricing\\ & dolt table import -u rates "{folder}{file}"')