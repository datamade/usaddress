from lxml import etree
import ast

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


# transform osm xml data into tagged training data
def osmToTraining(xml_file):
	address_list = xmlToAddrList(xml_file)
	train_data=[]
	addr_index = 0
	token_index = 0
	# only the osm tags below will end up in training data; others will be ignored
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
		for key, value in address.items():
			if key in osm_tags_to_addr_tags.keys():
				addr_train.append([value ,osm_tags_to_addr_tags[key]])
		train_data.append(addr_train)
	return train_data


# transform us50 address lines into tagged training data
def parseLines(addr_file):
	lines = open(addr_file, 'r')
	parsed = [[]]
	addr_index = 0
	token_index = 0
	tag_list = [None, 'street number', 'pobox', 'street', 'street type',
                'city', 'state', 'zip', 'suffix']

	for line in lines:
		print line
		if line == '\n':
			addr_index += 1
			token_index = 0
			parsed.append([])
		else:
			split = line.split(' |')
			full_token_string = split[0]
			token_num = split[1].rstrip()
			token_num = int(token_num)
			token_tag = tag_list[token_num]
			token_list = full_token_string.split()
			for token in token_list:
				parsed[addr_index].append((token, token_tag))
	return parsed
