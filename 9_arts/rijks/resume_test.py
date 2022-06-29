import glob
import os
list_of_files = glob.glob('F:\\museum-collections\\rijks\\1\\*')
resumeFile = max(list_of_files, key=os.path.getctime)
print(resumeFile)
resumeFile = resumeFile.split("\\")[-1]
print(resumeFile)
