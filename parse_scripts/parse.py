from builtins import str
from lxml import etree
import ast
import re
import random

# osm xml data -> list of dicts representing osm addresses
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


# natural addresses (in addr:full from osm xml data) -> training file (xml)
def osmNaturalToTraining(xml_file):
    address_list = xmlToAddrList(xml_file)
    train_addr_list = etree.Element('AddressCollection')
    trainFileName = '../training_data/'+re.sub(r'\W+', '_', xml_file)+'.xml'
    punc_list = ',.'
    # only the osm tags below will end up in training data; others will be ignored
    osm_tags_to_addr_tags = {
        "addr:housenumber":"AddressNumber",
        "addr:street:prefix":"StreetNamePreDirectional",
        "addr:street:name":"StreetName",
        "addr:street:type":"StreetNamePostType",
        "addr:city":"PlaceName",
        "addr:state":"StateName",
        "addr:postcode":"ZipCode"}
    for address in address_list:
        addr_tokens = address['addr:full'].split()
        train_addr = etree.Element('AddressString')
        is_addr_taggable = True
        #loop through tokens & find tags for each
        for token in addr_tokens:
            is_token_taggable = False
            for key, value in list(address.items()):
                if key in list(osm_tags_to_addr_tags.keys()) and key != 'addr:full' and token in value.split():
                    is_taggable = True
                    token_xml = etree.Element(osm_tags_to_addr_tags[key])
                    #check for punctuation
                    token_xml.text = token
                    if token[-1] in punc_list:
                        token_xml.text = token[0:-1]
                        token_xml.tail = token[-1]
                    train_addr.append(token_xml)
            if is_token_taggable ==False:
                is_addr_taggable = False
        if is_addr_taggable == True:
            train_addr_list.append(train_addr)
    output = etree.tostring(train_addr_list, pretty_print=True)
    with open(trainFileName, 'w') as f:
        f.write(output)

# osm xml data -> synthetic addresses -> training & test files (xml)
def osmSyntheticToTraining(xml_file):
    address_list = xmlToAddrList(xml_file)
    train_addr_list = []

    trainFileName = 'training/training_data/synthetic_'+re.sub(r'\W+', '_', re.sub(r'.*/', '', xml_file))+'.xml'
    testFileName = 'training/test_data/synthetic_'+re.sub(r'\W+', '_', re.sub(r'.*/', '', xml_file))+'.xml'

    synthetic_order = [
            ('addr:housenumber', 'AddressNumber', 'Street'),
            ('addr:street:prefix', 'StreetNamePreDirectional', 'Street'),
            ('addr:street:name', 'StreetName', 'Street'),
            ('addr:street:type', 'StreetNamePostType', 'Street'),
            ('addr:city', 'PlaceName', 'City'),
            ('addr:state', 'StateName', 'Area'),
            ('addr:postcode', 'ZipCode', 'Area')]
    
    for address in address_list:
        train_addr = etree.Element('AddressString')
        components = {'Street' : [], 'City' : [], 'Area' : []}
        for source_tag, target_tag, tag_type in synthetic_order:
            if source_tag in list(address.keys()):
                words = address[source_tag].split()
                for word in words:
                    token_xml = etree.Element(target_tag)
                    token_xml.text = word
                    token_xml.tail = ' '
                    components[tag_type].append(token_xml)
        
        for tag_type in ('Street','City', 'Area') :
            l = components[tag_type]
            if l :
                l[-1].text += ','

        address_xml = (components['Street'] 
                       + components['City'] 
                       + components['Area'])
        
        address_xml[-1].text = address_xml[-1].text[:-1]
        address_xml[-1].tail = None

        for xml_element in address_xml:
            train_addr.append(xml_element)

        train_addr_list.append(train_addr)

    random.shuffle(train_addr_list)
    percent_20 = int(len(train_addr_list) * 0.2)

    test_data = etree.Element('AddressCollection')
    test_data.extend(train_addr_list[:percent_20])

    train_data = etree.Element('AddressCollection')
    train_data.extend(train_addr_list[percent_20:])

    with open(trainFileName, 'w') as f:
        f.write(etree.tostring(train_data, pretty_print=True))

    with open(testFileName, 'w') as f:
        f.write(etree.tostring(test_data, pretty_print=True))


# us50 data -> training or test file (xml)
def trainFileFromLines(addr_file, is_train=True):
    lines = open(addr_file, 'r')
    addr_index = 0
    token_index = 0
    if is_train == True:
        outputFileName = 'training/training_data/'+re.sub(r'\W+', '_', re.sub(r'.*/', '', addr_file))+'.xml'
    else:
        outputFileName = 'training/test_data/'+re.sub(r'\W+', '_', re.sub(r'.*/', '', addr_file))+'.xml'

    tag_list = [None, 'AddressNumber', 'USPSBox', 'StreetName', 'StreetNamePostType',
                'PlaceName', 'StateName', 'ZipCode', 'suffix']
    addr_list = etree.Element('AddressCollection')
    addr = etree.Element('AddressString')
    for line in lines:
        if line =='\n': #add addr to list & reset addr
            addr[-1].tail = None
            addr_list.append(addr)
            addr = etree.Element('AddressString')
        else:
            split = line.split(' |')
            addr_line = split[0]
            addr_tokens = addr_line.split()
            token_num = int(split[1].rstrip())
            token_tag = tag_list[token_num]
            for token in addr_tokens:
                token_xml = etree.Element(token_tag)
                token_xml.text = token
                token_xml.tail = ' '
                addr.append(token_xml)

    output = etree.tostring(addr_list, pretty_print=True)
    with open(outputFileName, 'w') as f:
        f.write(output)



if __name__ == '__main__' :
        osmSyntheticToTraining('training/data/osm_data.xml')
        #trainFileFromLines('training/data/us50.train.tagged')
        #trainFileFromLines('training/data/us50.test.tagged', False)
