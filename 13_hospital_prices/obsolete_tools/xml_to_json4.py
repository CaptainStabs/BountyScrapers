from lxml import etree
import json
from tqdm import tqdm

def xml_to_json(input_file, output_file):
    # create an iterator for the input XML file
    context = etree.iterparse(input_file, events=("start", "end"))
    _, root = next(context)

    # create an empty dictionary to hold the output JSON data
    output_data = {}

    # iterate through the XML elements
    for event, elem in tqdm(context):
        if event == "end" and elem.tag == "InNetworkRow":
            # create a dictionary to hold the current in-network row data
            in_network_row = {}

            # iterate through the child elements of the current in-network row element
            for child_elem in elem.iterchildren():
                # add the child element data to the in_network_row dictionary
                in_network_row[child_elem.tag] = child_elem.text

            # add the in_network_row dictionary to the output_data list
            if "in_network" not in output_data:
                output_data["in_network"] = []
            output_data["in_network"].append(in_network_row)

            # clear the current element from memory
            elem.clear()

    # write the output data to a JSON file
    with open(output_file, "w") as outfile:
        json.dump(output_data, outfile)

    # release the memory used by the root element
    del root

if __name__ == "__main__":
    input_file =  "F:\\_Bounty\\chorus health group innetwrok\\InNetwork.xml"
    output_file = input_file.replace(".xml", ".json")
    xml_to_json(input_file, output_file)