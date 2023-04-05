import xmltodict
import json
from lxml import etree
from bs4 import BeautifulSoup

xml_file_path =  "in_network_rates_20230301.xml"
json_file_path = xml_file_path.replace(".xml", ".json")


# read the malformed XML file

with open(xml_file_path, "r") as f:
    xml_data = f.read()

# parse the XML data
parser = etree.XMLParser(recover=True)
root = etree.fromstring(xml_data, parser=parser)

# create a list to hold the in_network data
in_network_list = []

# iterate over the in_network groups
for in_network in root.iter("in_network"):
    # create a dictionary to hold the in_network data
    in_network_data = {}

    # iterate over the items in the in_network group
    items_list = []
    for item in in_network.iter("item"):
        # create a dictionary to hold the item data
        item_data = {}

        # iterate over the fields in the item
        for field in item.iter():
            if field.tag not in ["item", "provider_groups"]:
                item_data[field.tag] = field.text

        # iterate over the provider_groups in the item
        providers_list = []
        for provider_group in item.iter("provider_groups"):
            for provider in provider_group.iter("providers"):
                provider_data = {}
                for provider_field in provider.iter():
                    if provider_field.tag != "item":
                        provider_data[provider_field.tag] = provider_field.text
                providers_list.append(provider_data)
        item_data["providers"] = providers_list

        items_list.append(item_data)

    in_network_data["items"] = items_list

    in_network_list.append(in_network_data)

# convert the data to JSON format
json_data = json.dumps({"in_network": in_network_list})

# write the JSON data to a file
with open(json_file_path, "w") as f:
    f.write(json_data)