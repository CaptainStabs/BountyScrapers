from lxml import etree
import json
from tqdm import tqdm
from collections import defaultdict

def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d


def convert_xml_to_json(xml_file_path, json_file_path):
    # Open the input XML file for reading
    with open(xml_file_path, 'rb') as f:
        # Create an XML parser object
        parser = etree.iterparse(f, events=('start', 'end'), recover=True)

        # Define the root element
        root = None

        # Loop through the parser object
        for event, element in tqdm(parser):
            # If it is the start of the root element
            if event == 'start' and root is None:
                root = element
            # If it is the end of an element
            elif event == 'end':
                # Convert the element to a dictionary
                element_dict = dict(element.attrib)
                element_dict.update((child.tag, child.text or '') for child in element)
                # Delete the element to save memory
                element.clear()
                new_element = etree.Element(element.tag)
                # Add the attributes to the new element
                for key, value in element_dict.items():
                    new_element.set(key, value)
                # Append the new element to the root element
                root.append(new_element)

        # Convert the root element to a dictionary
        # root_dict = etree_to_dict(root)
        root_dict = etree_to_dict(root)

        # Write the JSON output to a file
        with open(json_file_path, 'w') as outfile:
            json.dump(root_dict, outfile, indent=4)

xml_file_path =  "in_network_rates_20230301.xml"
json_file_path = xml_file_path.replace(".xml", ".json")

convert_xml_to_json(xml_file_path, json_file_path)