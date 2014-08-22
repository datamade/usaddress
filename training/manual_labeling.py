import usaddress
from lxml import etree
import sys


def consoleLabel(raw_addr_list, label_options): #should this also take the model filepath as an argument?
    finished = False
    tagged_addr_list = []
    punc_list = ['.', ',']
    valid_input_tags = []
    label_dict = {}

    for i in range(len(label_options)):
        valid_input_tags.append(str(i))

    for label in label_options:
        label_dict[label[0]] = label[1]
        label_dict[label[1]] = label[0]

    addr_index = 0
    total_addrs = len(raw_addr_list)
    while not finished:
        for addr_string in raw_addr_list:
            addr_index += 1

            addr_tokens = addr_string.split()

            valid_yn = False
            valid_tag = False
            user_input_yn = ''
            user_input_tag = ''

            print "("+str(addr_index)+" of "+str(total_addrs)+") ", "-"*50
            print "ADDRESS STRING: ", addr_string
            #tag addr tokens using model
            preds = usaddress.parse(addr_string)
            # ** check that the predicted labels match up with those in label_options?

            while not valid_yn:

                # pretty print for address tokens & tags
                for pred in preds:
                    n = 12-len(pred[0])
                    print pred[0], ' '*n, '|',
                print "\n",
                for pred in preds:
                    if pred[1] == 'Null':
                        print_tag = 'punc' # ** this could be smarter
                    else:
                        print_tag = label_dict[pred[1]]
                    n = 12-len(print_tag)
                    print print_tag, ' '*n, '|',
                #print predicted tags here
                print "\n\n",

                sys.stderr.write('Is this correct? (y)es / (n)o / (s)kip\n')
                user_input_yn = sys.stdin.readline().strip()
                if user_input_yn in ['y', 'n', 's', '']:
                    valid_yn = True


            if user_input_yn =='y':
                tagged_addr=[]
                for token in preds:
                    tagged_addr.append((token[0], token[1]))
                tagged_addr_list.append(tagged_addr)

            elif user_input_yn =='n':
                while not valid_tag:
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

                tagged_addr_list.append(tagged_addr)

            else:
                print "Skipped\n"

        print "Done! Yay!"
        finished = True

    return tagged_addr_list


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




sample_addr_list = [
    '6943 Roosevelt Road, Berwyn, IL 60402',
    '1330 West Madison Street, Chicago, IL 60607',
    '4128 14th Avenue, Rock Island, IL 61201'
    ]

# a list of labels, w/ each label represented as [label display name, label xml tag]
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
list2XMLfile( tagged_addr_list, 'training_data/TESTINGcommandline.xml' )

