from training.manual_labeling import addr2XML
from lxml import etree
import unittest

class TestList2XML(unittest.TestCase) :

    def test_xml(self):
        XMLequals( [('#', 'foo'), ('1', 'foo'), ('Pinto', 'foo')], '<foo>#</foo> <foo>1</foo> <foo>Pinto</foo>')

    def test_none_tag(self):
        XMLequals( [('Box', 'foo'), ('#', None), ('1', 'foo'), ('Pinto', 'foo')], '<foo>Box</foo># <foo>1</foo> <foo>Pinto</foo>')
        XMLequals( [('#', None), ('1', 'foo'), ('Pinto', 'foo')], '# <foo>1</foo> <foo>Pinto</foo>')
       
       
def XMLequals(labeled_addr, xml):
    correct_xml = '<AddressString>' + xml + '</AddressString>'
    generated_xml = etree.tostring( addr2XML(labeled_addr) )
    print "Correct:   ", correct_xml
    print "Generated: ", generated_xml
    assert correct_xml == generated_xml


if __name__ == '__main__' :
    unittest.main()    
