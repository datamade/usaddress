import usaddress
from lxml import etree
import sys


def consoleLabel(raw_addr_list, label_options): 

    valid_input_tags = dict((str(i), tag) 
                            for i, tag
                            in enumerate(label_options))
    valid_responses = ['y', 'n', 's', '']


    total_addrs = len(raw_addr_list)

    tagged_addr_list = []

    for i, addr_string in enumerate(raw_addr_list, 1):

        print "(%s of %s)" % (i, total_addrs)
        print "-"*50
        print "ADDRESS STRING: ", addr_string
            
        preds = usaddress.parse(addr_string)

        user_input = None 
        while user_input not in valid_responses :

            print_table(preds)

            sys.stderr.write('Is this correct? (y)es / (n)o / (s)kip\n')
            user_input = sys.stdin.readline().strip()

            if user_input =='y':
                tagged_addr_list.append(preds)

            elif user_input =='n':
                tagged_addr = manualTagging(preds, 
                                            valid_input_tags, 
                                            label_options)
                tagged_addr_list.append(tagged_addr)

            elif user_input in ('' or 's') :
                print "Skipped\n"

    print "Done! Yay!"
    
    return tagged_addr_list



def print_table(table):
    col_width = [max(len(x) for x in col) for col in zip(*table)]
    for line in table:
        print "| %s |" % " | ".join("{:{}}".format(x, col_width[i])
                                for i, x in enumerate(line))


def manualTagging(preds, valid_input_tags, label_options):
    tagged_addr = []
    for token in preds:
        valid_tag = False
        while not valid_tag:
            print 'What is \''+token[0]+'\' ? If '+token[1]+' hit return' #where should the tag list be printed?
            user_input_tag = sys.stdin.readline().strip()
            if user_input_tag in valid_input_tags or user_input_tag == '':
                valid_tag = True

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


if __name__ == '__main__' :

    sample_addr_list = [
        '6943 Roosevelt Road, Berwyn, IL 60402',
        '1330 West Madison Street, Chicago, IL 60607',
        '4128 14th Avenue, Rock Island, IL 61201'
    ]
    
    # a list of labels, w/ each label represented as [label display
    # name, label xml tag]
    labels = [
        ['punc', None],
        ['addr no', 'AddressNumber'],
        ['street dir', 'StreetNamePreDirectional'],
        ['street name', 'StreetName'],
        ['street type', 'StreetNamePostType'],
        ['unit type', 'OccupancyType'],
        ['unit no', 'OccupancyIdentifier'],
        ['box type', 'USPSBoxType'],
        ['box no', 'USPSBoxID'],
        ['city', 'PlaceName'],
        ['state', 'StateName'],
        ['zip', 'ZipCode']
    ]
    
    tagged_addr_list = consoleLabel( sample_addr_list, labels )
    print tagged_addr_list
    list2XMLfile( tagged_addr_list, 'training_data/TESTINGcommandline.xml' )

