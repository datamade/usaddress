usaddress
=================
[![Build Status](https://travis-ci.org/datamade/usaddress.svg?branch=master)](https://travis-ci.org/datamade/usaddress)

usaddress is a python library for parsing unstructured address strings into address components, using advanced NLP methods. Try it out on our [web interface](https://parserator.datamade.us/usaddress)! For those who aren't python developers, we also have an [API](https://parserator.datamade.us/api-docs).

**What this can do:** Using a probabilistic model, it makes (very educated) guesses in identifying address components, even in tricky cases where rule-based parsers typically break down.

**What this cannot do:** It cannot identify address components with perfect accuracy, nor can it verify that a given address is correct/valid.

## How to use the usaddress python library

1. Install usaddress with [pip](http://pip.readthedocs.org/en/latest/quickstart.html), a tool for installing and managing python packages ([beginner's guide here](http://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/))

  In the terminal,
  
  ```bash
  pip install usaddress
  ```
2. Parse some addresses!

  ![usaddress](https://cloud.githubusercontent.com/assets/1406537/7869001/65c6ae62-0545-11e5-8b65-5d9e71dface5.gif)

  Note that `parse` and `tag` are different methods:
  ```python
  import usaddress
  addr='123 Main St. Suite 100 Chicago, IL'
  
  # The parse method will split your address string into components, and label each component.
  # expected output: [(u'123', 'AddressNumber'), (u'Main', 'StreetName'), (u'St.', 'StreetNamePostType'), (u'Suite', 'OccupancyType'), (u'100', 'OccupancyIdentifier'), (u'Chicago,', 'PlaceName'), (u'IL', 'StateName')]
  usaddress.parse(addr)
  
  # The tag method will try to be a little smarter
  # it will merge consecutive components, strip commas, & return an address type
  # expected output: (OrderedDict([('AddressNumber', u'123'), ('StreetName', u'Main'), ('StreetNamePostType', u'St.'), ('OccupancyType', u'Suite'), ('OccupancyIdentifier', u'100'), ('PlaceName', u'Chicago'), ('StateName', u'IL')]), 'Street Address')
  usaddress.tag(addr)
  ```

## How to use this development code (for the nerds)
usaddress uses [parserator](https://github.com/datamade/parserator), a library for making and improving probabilistic parsers - specifically, parsers that use [python-crfsuite](https://github.com/tpeng/python-crfsuite)'s implementation of conditional random fields. Parserator allows you to train the usaddress parser's model (a .crfsuite settings file) on labeled training data, and provides tools for adding new labeled training data.
#### Building & testing the code in this repo
  
  ```
  git clone https://github.com/datamade/usaddress.git  
  cd usaddress  
  pip install -r requirements.txt  
  python setup.py develop  
  parserator train training/labeled.xml usaddress  
  nosetests .  
  ```  
#### Creating/adding labeled training data (.xml outfile) from unlabeled raw data (.csv infile)  
  If there are address formats that the parser isn't performing well on, you can add them to training data. As the usaddress parser continually learns about new cases, it will continually become smarter and more robust.  
  
 ```
parserator label [infile] [outfile] usaddress  
```  
  Our main training file is `training/labeled.xml` so you can do

```
parserator label [infile] training/labeled.xml usaddress  
```  


  This will start a console labeling task, where you will be prompted to label raw strings via the command line. For more info on using parserator, see the [parserator documentation](https://github.com/datamade/parserator/blob/master/README.md). 
  
### Creating training data from existing labeled data
If you already have existing labeled data from another project, you'll need to convert it to our format. See https://github.com/lemgandi/FGDCMultiword for an example of how to do this.
  
#### Re-training the model  
  If you've added new training data, you will need to re-train the model. 
  
  ```
  parserator train [traindata] usaddress  
  ```  
  
  So, you could do 
  
  ```
  parserator train training/labeled.xml usaddress  
  ```  
  
  To set multiple files as traindata, separate them with commas (e.g. ```training/foo.xml,training/bar.xml```)

  Contribute back by making a pull request with your added training examples.

## Important links

* Web Interface: https://parserator.datamade.us/usaddress
* Python Package Distribution: https://pypi.python.org/pypi/usaddress
* Python Package Documentation: http://usaddress.rtfd.org/
* API Documentation: https://parserator.datamade.us/api-docs
* Repository: https://github.com/datamade/usaddress
* Issues: https://github.com/datamade/usaddress/issues
* Blog post: http://datamade.us/blog/parsing-addresses-with-usaddress

## Team

* [Forest Gregg](https://github.com/fgregg), DataMade
* [Cathy Deng](https://github.com/cathydeng), DataMade
* [Miroslav Batchkarov](http://mbatchkarov.github.io), University of Sussex

## Bad Parses / Bugs

Report issues in the [issue tracker](https://github.com/datamade/usaddress/issues)

If an address was parsed incorrectly, please let us know! If possible, please send over a few real-world examples of similar address patterns, along with some info about the source of the data - this will help us train the parser and improve its performance.

If something in the library is not behaving intuitively, it is a bug, and should be reported.

## Note on Patches/Pull Requests
 
* Fork the project.
* Make your feature addition or bug fix.
* Send us a pull request. Bonus points for topic branches.

## Copyright

Copyright (c) 2014 Atlanta Journal Constitution. Released under the [MIT License](https://github.com/datamade/usaddress/blob/master/LICENSE).
