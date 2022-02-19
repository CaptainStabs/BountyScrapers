import yaml
import json
with open("us_zipcodes.yaml", "r") as f:
    zip_cty_cnty = yaml.safe_load(f)

with open("us_zipcodes", "w") as f:
    f.write(json.dumps(zip_cty_cnty, indent=2))
