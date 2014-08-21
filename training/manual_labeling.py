import pycrfsuite
from lxml import etree
import sys


def consoleLabel(raw_addr_list, label_options): #should this also take the model filepath as an argument?
    finished = False
    tagged_addr_list = []
    punc_list = ['.', ',']
    valid_input_tags = []
    for i in range(len(label_options)):
        valid_input_tags.append(str(i))

    while not finished:
        for addr_string in raw_addr_list:

            addr_tokens = addr_string.split()

            valid_yn = False
            valid_tag = False
            user_input_yn = ''
            user_input_tag = ''

            #tag addr tokens using model here

            while not valid_yn:

                print addr_string
                #print predicted tags here

                sys.stderr.write('Is this correct? (y)es / (n)o / (s)kip\n')
                user_input_yn = sys.stdin.readline().strip()
                if user_input_yn[0] in ['y', 'n', 's']:
                    valid_yn = True

            if user_input_yn[0] =='y':
                print "OK"
                # generate addr_xml based on predicted tags & append to tagged_address_list
                # would we only want to add addresses that were predicted incorrectly?

            if user_input_yn[0] =='n':
                while not valid_tag:
                    addr_xml = etree.Element('AddressString')
                    for token in addr_tokens:
                        valid_tag = False
                        while not valid_tag:
                            print 'What is \''+token+'\' ?' #where should the tag list be printed?
                            user_input_tag = sys.stdin.readline().strip()
                            if user_input_tag in valid_input_tags:
                                valid_tag = True

                        token_xml = etree.Element(label_options[int(user_input_tag)][1])
                        punc = ''
                        if token[-1] in punc_list:
                            punc = token[-1]
                            token = token[:-1]
                        token_xml.text = token
                        token_xml.tail = punc + ' '
                        addr_xml.append(token_xml)

                addr_xml[-1].tail = None
                tagged_addr_list.append(addr_xml)

        print "Done! Yay!"
        finished = True

    return tagged_addr_list


def XMLtoFile (xml_list, filepath):
    address_list_xml = etree.Element('AddressCollection')
    address_list_xml.extend(xml_list)
    with open( filepath, 'w' ) as f:
        f.write(etree.tostring(address_list_xml, pretty_print = True))







sample_addr_list = [
    '6943 Roosevelt Road, Berwyn, IL 60402',
    '1330 West Madison Street, Chicago, IL 60607',
    '4128 14th Avenue, Rock Island, IL 61201'
    ]

# a list of labels, w/ each label represented as [label display name, label xml tag]
labels = [
    ['punctuation', None],
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
XMLtoFile( tagged_addr_list, 'training_data/TESTINGcommandline.xml' )

