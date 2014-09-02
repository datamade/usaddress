import usaddress
from lxml import etree
import sys


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


def list2XMLfile(addr_list, filepath):
    address_list_xml = etree.Element('AddressCollection')

    for addr in addr_list:
        addr_xml = etree.Element('AddressString')
        xml_token_list = []
        for token in addr:
            if token[1] == None or token[1] == 'Null': #make this smarter
                if len(xml_token_list) > 0:
                    xml_token_list[-1].tail = token[0] + ' '
            else:
                token_xml = etree.Element(token[1])
                token_xml.text = token[0]
                token_xml.tail = ' '
                xml_token_list.append(token_xml)
        xml_token_list[-1].tail = ''
        addr_xml.extend(xml_token_list)
        address_list_xml.append(addr_xml)

    with open( filepath, 'w' ) as f:
        f.write(etree.tostring(address_list_xml, pretty_print = True))

def list2file(addr_list, filepath):
    file = open( filepath, 'w' )
    for addr in addr_list:
        file.write('"%s"\n' % addr)


if __name__ == '__main__' :

    import csv
    from argparse import ArgumentParser
    import unidecode

    labels = [
        ['punc', None],
        ['addr #', 'AddressNumber'],
        ['street dir pre', 'StreetNamePreDirectional'],
        ['street name', 'StreetName'],
        ['street type, post', 'StreetNamePostType'],
        ['street type, pre', 'StreetNamePreType'],
        ['street dir post', 'StreetNamePostDirectional'],
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
        ['streetname modifer, pre', 'StreetNamePreModifier']

    ]


    parser = ArgumentParser(description="Label some addresses")
    parser.add_argument(dest="filename", 
                        help="input csv with addresses", metavar="FILE")
    args = parser.parse_args()

    
    with open(args.filename) as infile :
        reader = csv.reader(infile)

        address_strings = set([unidecode.unidecode(row[0]) for row in reader])

    tagged_addr_list, remaining_addrs = consoleLabel(address_strings, labels) 
    list2XMLfile(tagged_addr_list, 'labeled.xml')
    list2file(remaining_addrs, 'unlabeled.csv')
