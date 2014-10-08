import training
from training.manual_labeling import addr2XML
from lxml import etree
import unittest


class TestManualAddr2XML(unittest.TestCase) :

    def test_single_component(self) :

        test_input = [ ('Monroe', 'Component') ]
        expected_xml = '<AddressString><Component>Monroe</Component></AddressString>'

        assert etree.tostring( addr2XML(test_input) ) == expected_xml

    def test_two_components(self) :

        test_input = [ ('123', 'foo'), ('Monroe', 'bar') ]
        expected_xml = '<AddressString><foo>123</foo> <bar>Monroe</bar></AddressString>'

        assert etree.tostring( addr2XML(test_input) ) == expected_xml

    def test_multiple_components(self) :

        test_input = [ ('123', 'foo'), ('Monroe', 'bar'), ('St', 'foobar') ]
        expected_xml = '<AddressString><foo>123</foo> <bar>Monroe</bar> <foobar>St</foobar></AddressString>'

        assert etree.tostring( addr2XML(test_input) ) == expected_xml


if __name__ == '__main__' :
    unittest.main()    
