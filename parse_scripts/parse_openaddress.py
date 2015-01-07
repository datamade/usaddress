import json
from lxml import etree
from usaddress import tokenize


def json2trainingxml(infile, outfile, tagmapping):

    with open(infile) as f:
        data = json.load(f)
    addr_list = json2addrlist(data, tagmapping)
    
    list2xml(addr_list, outfile)


def json2addrlist(data, tagmapping):

    addr_list = []
    for raw_addr in data["features"]:
        addr = []
        for tagset in tagmapping:
            if tagset[1]:
                addr.append([tagset[0], raw_addr["properties"][tagset[2]]])
            else:
                addr.append([tagset[0], tagset[2]])
        addr_list.append(addr)

    return addr_list

def list2xml(addr_list, outfile):

    xml_addr_list = etree.Element('AddressCollection')
    for addr in addr_list:
        xml_addr = etree.Element('AddressString')
        #handle commas?
        for component in addr:
            if component[1]:
                for token in tokenize(component[1]):
                    token_xml = etree.Element(component[0])
                    token_xml.text = token
                    token_xml.tail = ' '
                    xml_addr.append(token_xml)
        xml_addr[-1].tail = None
        xml_addr_list.append(xml_addr)

    output = etree.tostring(xml_addr_list, pretty_print = True)
    with open(outfile, 'w') as f:
        f.write(output)


#this determines the ordering of training xml tags, & the mapping of address strings
#xml address tag, whether raw data has this tag, corresponding json tag in raw data or predetermined value
tag_mapping = [
    ["AddressNumber",               True,   "HOUSENO"],
    ["StreetNamePreDirectional",    True,   "PREDIR"],
    ["StreetNamePreType",           True,   "PRETYPE"],
    ["StreetName",                  True,   "NAME"],
    ["StreetNamePostType",          True,   "SUFTYPE"],
    ["StreetNamePostDirectional",   True,   "SUFDIR"],
    ["OccupancyType",               True,   "UNITTYPE"],
    ["OccupancyIdentifier",         True,   "UNITNO"],
    ["PlaceName",                   True,   "CITY"],
    ["StateName",                   False,  "IA"],
    ["ZipCode",                     True,   "ZIP"]]


infile = "../data/openaddresses/us-ia-linn.json"
outfile = "../training_data/openaddress_us_ia_linn.xml"

json2trainingxml(infile, outfile, tag_mapping)
