from lxml import etree
import json
from tqdm import tqdm

xml_file =  "F:\\_Bounty\\chorus health group innetwrok\\InNetwork.xml"
json_file = xml_file.replace(".xml", ".json")

# read input xml file
with open(xml_file, 'rb') as f:
    xml_data = f.read()

# create an ElementTree object from the xml data
parser = etree.XMLParser(recover=True)
root = etree.fromstring(xml_data, parser=parser)

# Create empty dictionary to store JSON data
json_dict = {}

# Create a dictionary to hold the converted JSON data
json_data = {}

# Iterate through each element in the XML file
for element in tqdm(root.iter()):
    if element.tag == 'InNetworkRow':
        # Create a dictionary to hold the data for this row
        row_data = {}
        for child in element.iter():
            if child.tag == 'negotiated_type':
                negotiated_data = {}
                negotiated_data['negotiated_type'] = child.text
                negotiated_data['negotiated_rate'] = float(child.getnext().text)
                negotiated_data['expiration_date'] = child.getnext().getnext().text
                negotiated_data['billing_class'] = child.getnext().getnext().getnext().text
                negotiated_data['additional_information'] = child.getnext().getnext().getnext().getnext().text
                if 'negotiated_rates' in row_data:
                    row_data['negotiated_rates'].append(negotiated_data)
                else:
                    row_data['negotiated_rates'] = [negotiated_data]
            elif child.tag == 'npi':
                if 'provider_groups' in row_data:
                    row_data['provider_groups'][-1]['npi'].append(int(child.text))
                else:
                    row_data['provider_groups'][-1]['npi'] = [int(child.text)]
            elif child.tag == 'tin':
                tin_data = {}
                tin_data['type'] = child.get('type')
                tin_data['value'] = child.text
                row_data['provider_groups'].append({'tin': tin_data})
            else:
                row_data[child.tag] = child.text
        if 'in_network' in json_data:
            json_data['in_network'].append(row_data)
        else:
            json_data['in_network'] = [row_data]
    elif element.tag != 'InNetwork':
        json_data[element.tag] = element.text

# Save JSON to file
with open(json_file, "w") as f:
    json.dump(json_dict, f, indent=4)