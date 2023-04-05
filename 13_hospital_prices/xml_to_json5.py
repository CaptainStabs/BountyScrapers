from lxml import etree
import json
from tqdm import tqdm

def xml_to_json(input_file, output_file):
    # create an iterator for the input XML file
    context = etree.iterparse(input_file, events=("start", "end"))
    _, root = next(context)

    # create a dictionary to hold the common fields data
    common_data = {}

    # create an empty list to hold the in-network data
    in_network_data = []

    # iterate through the XML elements
    for event, elem in tqdm(context):
        if event == "end" and elem.tag == "InNetworkRow":
            # create a dictionary to hold the current in-network row data
            in_network_row = {}

            # iterate through the child elements of the current in-network row element
            for child_elem in elem.iterchildren():
                # add the child element data to the in_network_row dictionary
                if child_elem.tag in ["reporting_entity_name", "reporting_entity_type", "last_updated_on", "version"]:
                    # add the common data to the common_data dictionary
                    common_data[child_elem.tag] = child_elem.text
                elif child_elem.tag == "negotiated_rate":
                    in_network_row['negotiated_rates'] = [child_elem.text]
                else:
                    in_network_row[child_elem.tag] = child_elem.text

            # add the in_network_row dictionary to the in_network_data list
            in_network_data.append(in_network_row)

            # clear the current element from memory
            elem.clear()

    # add the common data to the output_data dictionary
    output_data = common_data.copy()

    # add the in-network data to the output_data dictionary
    output_data["in_network"] = in_network_data

    # write the output data to a JSON file
    with open(output_file, "w") as outfile:
        json.dump(output_data, outfile, indent=4)

    # release the memory used by the root element
    del root


if __name__ == "__main__":
    input_file =  "F:\\_Bounty\\chorus health group innetwrok\\InNetwork.xml"
    output_file = input_file.replace(".xml", ".json")
    xml_to_json(input_file, output_file)
