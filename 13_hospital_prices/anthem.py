from mrfutils import index_file_to_csv

url = "https://antm-pt-prod-dataz-nogbd-nophi-us-east1.s3.amazonaws.com/anthem/2023-03-01_anthem_index.json.gz"
out = ".\\anthem\\"

index_file_to_csv(url=url, out_dir=out)
