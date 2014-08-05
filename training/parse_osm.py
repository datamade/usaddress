from lxml import etree
import ast
import re

# parse xml data, return a list of dicts representing addresses
def xmlToAddrList(xml_file):
	tree = etree.parse(xml_file)
	root = tree.getroot()
	addr_list=[]
	for element in root:
		if element.tag == 'node' or element.tag =='way':
			address={}
			for x in element.iter('tag'):
				addr = ast.literal_eval(str(x.attrib))
				address[addr['k']]=addr['v']
			addr_list.append(address)
	return addr_list


# transform osm data into tagged training data
def osmToTraining(address_list):
	train_data=[]
	addr_index = 0
	token_index = 0
	osm_tags_to_addr_tags = {
		"addr:house:number":"AddressNumber",
		"addr:street:prefix":"StreetNamePreDirectional",
		"addr:street:name":"StreetName",
		"addr:street:type":"StreetNamePostType",
		"addr:city":"PlaceName",
		"addr:state":"StateName",
		"addr:postcode":"ZipCode"}
	for address in address_list:
		addr_train = []
		for key, value in address.items(): #iterate through dict ****
			if key in osm_tags_to_addr_tags.keys(): #if the key is one of the defined osm tags
				addr_train.append([value ,osm_tags_to_addr_tags[key]]) #add (token, tokentag)
		train_data.append(addr_train)
	return train_data

