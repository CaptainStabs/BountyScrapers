from mrfutils import toc_file_to_csv

url = "https://antm-pt-prod-dataz-nogbd-nophi-us-east1.s3.amazonaws.com/anthem/2023-03-01_anthem_index.json.gz"
file = "F:\\_Bounty\\2023-03-01_anthem_index.json.gz"
out = "F:\\_Bounty\\anthem_toc\\"

toc_file_to_csv(url=url, file=file, out_dir=out)
