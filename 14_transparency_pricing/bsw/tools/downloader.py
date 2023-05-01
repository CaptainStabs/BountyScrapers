from tqdm import tqdm
import pandas as pd
import requests

tqdm = tqdm.pandas()

def get_files(filename, url):
    r = requests.get(url)
    with open('.\\input_files\\' + filename, 'wb') as f:
        f.write(r.content)

df = pd.read_csv('hospital_import.csv')

df[['file_name', 'stdchg_file_url']].progress_apply(lambda x: get_files(x[0], x[1]), axis=1)



