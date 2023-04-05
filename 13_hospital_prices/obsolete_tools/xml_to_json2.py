from lxml import etree
import json
from tqdm import tqdm

xml_file =  "in_network_rates_20230301.xml"
json_file = xml_file.replace(".xml", ".json")

# read input xml file
with open(xml_file, 'rb') as f:
    xml_data = f.read()

# create an ElementTree object from the xml data
parser = etree.XMLParser(recover=True)
root = etree.fromstring(xml_data, parser=parser)

# create a list to hold the in_network data
in_network_list = []

# iterate over all in_network elements
for in_network in tqdm(root.xpath('//in_network'), position=1, leave=False, desc="in_network"):
    in_network_dict = {}
    in_network_items = []

    # iterate over all item elements under each in_network element
    for item in in_network.xpath('./item'):
        item_dict = {}
        negotiated_rates_items = []

        # iterate over all negotiated_rates elements under each item element
        for negotiated_rates in item.xpath('./negotiated_rates/item'):
            negotiated_rates_dict = {}
            provider_groups_items = []

            # iterate over all provider_groups elements under each negotiated_rates element
            for provider_groups in negotiated_rates.xpath('./provider_groups/item'):
                providers_items = []

                # iterate over all providers elements under each provider_groups element
                for providers in provider_groups.xpath('./providers'):
                    npi_items = []
                    tin_items = {}

                    # iterate over all npi elements under each providers element
                    for npi in providers.xpath('./npi/item'):
                        npi_items.append(npi.text)

                    # get the tin elements under each providers element
                    tin = providers.xpath('./tin')
                    if len(tin) > 0:
                        tin_type = tin[0].xpath('./type')[0].text
                        tin_value = tin[0].xpath('./value')[0].text
                        tin_items['type'] = tin_type
                        tin_items['value'] = tin_value

                    # add the npi and tin data to the providers_items list
                    providers_items.append({'npi': npi_items, 'tin': tin_items})

                # add the providers data to the provider_groups_items list
                provider_groups_items.append({'providers': providers_items})

            # get the negotiated_price data under each negotiated_rates element
            negotiated_price = negotiated_rates.xpath('./negotiated_price')[0]
            expiration_date = negotiated_price.xpath('./expiration_date')[0].text
            negotiated_rate = negotiated_price.xpath('./negotiated_rates')[0].text
            negotiated_type = negotiated_price.xpath('./negotiated_type')[0].text
            service_code = negotiated_price.xpath('./service_code')[0].text

            # add the negotiated_rates and provider_groups data to the negotiated_rates_items list
            negotiated_rates_dict['negotiated_price'] = {'expiration_date': expiration_date, 'negotiated_rates': negotiated_rate, 'negotiated_type': negotiated_type, 'service_code': service_code}
            negotiated_rates_dict['provider_groups'] = provider_groups_items

            # add the negotiated_rates data to the item_dict
            negotiated_rates_items.append(negotiated_rates_dict)
        item_dict['billing_code'] = item.xpath('./billing_code')[0].text
        item_dict['billing_code_type'] = item.xpath('./billing_code_type')[0].text
        item_dict['billing_code_type_version'] = item.xpath('./billing_code_type_version')[0].text
        item_dict['description'] = item.xpath('./description')[0].text if len(item.xpath('./description')) > 0 else ''
        item_dict['name'] = item.xpath('./name')[0].text
        item_dict['negotiated_rates'] = negotiated_rates_items

        # add the item data to the in_network_items list
        in_network_items.append(item_dict)

    # add the in_network data to the in_network_dict
    in_network_dict['item'] = in_network_items

    # add the in_network_dict to the in_network_list
    in_network_list.append(in_network_dict)
    #create a dictionary to hold the root data
    root_dict = {'in_network': in_network_list}

    #convert the dictionary to JSON
    json_data = json.dumps(root_dict, indent=4)

    #print the JSON data
    # print(json_data)

    #write the JSON data to a file
    with open(json_file, 'w') as f:
        f.write(json_data)