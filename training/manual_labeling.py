import usaddress
from lxml import etree
import sys
import os.path


def consoleLabel(raw_addr, label_options): 

    friendly_tag_dict = dict((label[1], label[0])
                            for label in label_options)
    friendly_tag_dict['Null'] = friendly_tag_dict[None] #this could be smarter
    valid_responses = ['y', 'n', 's', 'f', '']
    addrs_left_to_tag = []
    finished = False

    addrs_left_to_tag = raw_addr.copy()

    total_addrs = len(raw_addr)

    tagged_addr = set([])

    for i, addr_string in enumerate(raw_addr, 1):
        if not finished:

            print "(%s of %s)" % (i, total_addrs)
            print "-"*50
            print "ADDRESS STRING: ", addr_string
                
            preds = usaddress.parse(addr_string)

            user_input = None 
            while user_input not in valid_responses :


                friendly_addr = [(token[0], friendly_tag_dict[token[1]]) for token in preds]
                print_table(friendly_addr)

                sys.stderr.write('Is this correct? (y)es / (n)o / (s)kip / (f)inish tagging\n')
                user_input = sys.stdin.readline().strip()

                if user_input =='y':
                    tagged_addr.add(tuple(preds))
                    addrs_left_to_tag.remove(addr_string)

                elif user_input =='n':
                    corrected_addr = manualTagging(preds, 
                                                label_options,
                                                friendly_tag_dict)
                    tagged_addr.add(tuple(corrected_addr))
                    addrs_left_to_tag.remove(addr_string)


                elif user_input in ('' or 's') :
                    print "Skipped\n"
                elif user_input == 'f':
                    finished = True

    print "Done! Yay!"
    
    return tagged_addr, addrs_left_to_tag



def print_table(table):
    col_width = [max(len(x) for x in col) for col in zip(*table)]
    for line in table:
        print "| %s |" % " | ".join("{:{}}".format(x, col_width[i])
                                for i, x in enumerate(line))
        


def manualTagging(preds, label_options, friendly_tag_dict):
    valid_input_tags = dict((str(i), tag[0]) 
                            for i, tag
                            in enumerate(label_options))
    tagged_addr = []
    for token in preds:
        valid_tag = False
        while not valid_tag:
            print 'What is \''+token[0]+'\' ? If '+ friendly_tag_dict[token[1]]+' hit return' #where should the tag list be printed?
            user_input_tag = sys.stdin.readline().strip()
            if user_input_tag in valid_input_tags or user_input_tag == '':
                valid_tag = True
            else:
                print 'These are the valid inputs:'
                for i in range(len(label_options)):
                    print i, ": ", valid_input_tags[str(i)]

        xml_tag = ''
        if user_input_tag == '':
            xml_tag = token[1]
        else:
            xml_tag = label_options[int(user_input_tag)][1]

        tagged_addr.append((token[0], xml_tag))
    return tagged_addr

def appendListToXML(addr_list, collection) :
    for addr in addr_list:
        addr_xml = addr2XML(addr)
        collection.append(addr_xml)
    return collection

def addr2XML(addr) :
    addr_xml = etree.Element('AddressString')
    for token, label in addr:
        if label == None or label == 'Null': #make this smarter
            if len(addr_xml) > 0:
                addr_xml[-1].tail = token + ' '
        else:
            component_xml = etree.Element(label)
            component_xml.text = token
            component_xml.tail = ' '
        addr_xml.append(component_xml)
    addr_xml[-1].tail = ''
    return addr_xml


def stripFormatting(collection) :
    collection.text = None 
    for element in collection :
        element.text = None
        element.tail = None
        
    return collection


def appendListToXMLfile(addr_list, filepath):

    if os.path.isfile(filepath):
        with open( filepath, 'r+' ) as f:
            tree = etree.parse(filepath)
            address_collection = tree.getroot()
            address_collection = stripFormatting(address_collection)

    else:
        address_collection = etree.Element('AddressCollection')


    address_collection = appendListToXML(addr_list, address_collection)


    with open(filepath, 'w') as f :
        f.write(etree.tostring(address_collection, pretty_print = True)) 



def list2file(addr_list, filepath):
    file = open( filepath, 'w' )
    for addr in addr_list:
        file.write('"%s"\n' % addr)


if __name__ == '__main__' :

    import csv
    from argparse import ArgumentParser
    import unidecode

    labels = [
        ['not addr', None],
        ['addr #', 'AddressNumber'],
        ['st dir pre', 'StreetNamePreDirectional'],
        ['st dir post', 'StreetNamePostDirectional'],
        ['st name', 'StreetName'],
        ['st type post', 'StreetNamePostType'],
        ['st type pre', 'StreetNamePreType'],
        ['intersection separator', 'IntersectionSeparator'],
        ['unit type', 'OccupancyType'],
        ['unit no', 'OccupancyIdentifier'],
        ['box type', 'USPSBoxType'],
        ['box no', 'USPSBoxID'],
        ['city', 'PlaceName'],
        ['state', 'StateName'],
        ['zip', 'ZipCode'],
        ['landmark', 'LandmarkName'],
        ['box group type', 'USPSBoxGroupType'],
        ['box group id', 'USPSBoxGroupID'],
        ['address number suffix', 'AddressNumberSuffix'],
        ['subaddress id', 'SubaddressIdentifier'],
        ['subaddress type', 'SubaddressType'],
        ['recipient', 'Recipient'],
        ['streetname modifer, pre', 'StreetNamePreModifier'],
        ['building name', 'BuildingName']

    ]


    parser = ArgumentParser(description="Label some addresses")
    parser.add_argument(dest="infile", 
                        help="input csv with addresses", metavar="FILE")
    parser.add_argument(dest="outfile", 
                        help="input csv with addresses", metavar="FILE")
    args = parser.parse_args()


    # Check to make sure we can write to outfile
    if os.path.isfile(args.outfile):
        with open(args.outfile, 'r+' ) as f:
            try :
                tree = etree.parse(f)
            except :
                raise ValueError("%s does not seem to be a valid xml file"
                                 % args.outfile)

    
    with open(args.infile, 'rU') as infile :
        reader = csv.reader(infile)

        address_strings = set([unidecode.unidecode(row[0]) for row in reader])

    tagged_addr_list, remaining_addrs = consoleLabel(address_strings, labels) 
    appendListToXMLfile(tagged_addr_list, args.outfile)
    list2file(remaining_addrs, 'unlabeled.csv')
