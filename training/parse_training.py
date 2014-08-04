from lxml import etree
import ast
import re
import training


def parseTrainingData(filepath):
	tree = etree.parse(filepath)
	root = tree.getroot()
	
	addr_list = []
	for element in root: #this ignores punctuation - need to figure out how to handle
		address = []
		for x in element.iter():
			if x.tag != 'AddressString':
				addr_list.append([x.text, x.tag])
	return addr_list

train_list = parseTrainingData('data/example_training.xml')
print train_list