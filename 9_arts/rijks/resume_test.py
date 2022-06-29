import glob
import os
list_of_files = glob.glob('C:\\Users\\adria\\github\\BountyScrapers\\9_arts\\rijks\\files\\*')
resumeFile = max(list_of_files, key=os.path.getctime)
print(resumeFile)
resumeFile = resumeFile.split("\\")[-1]
print(resumeFile)
