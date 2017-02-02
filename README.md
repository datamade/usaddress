usaddress
=================
[![Build Status](https://travis-ci.org/datamade/usaddress.svg?branch=master)](https://travis-ci.org/datamade/usaddress)[![Build status](https://ci.appveyor.com/api/projects/status/5mbcd8ku0tm66noq?svg=true)](https://ci.appveyor.com/project/fgregg/usaddress)

usaddress is a Python library for parsing unstructured address strings into address components, using advanced NLP methods. Try it out on our [web interface](https://parserator.datamade.us/usaddress)! For those who aren't Python developers, we also have an [API](https://parserator.datamade.us/api-docs).

**What this can do:** Using a probabilistic model, it makes (very educated) guesses in identifying address components, even in tricky cases where rule-based parsers typically break down.

**What this cannot do:** It cannot identify address components with perfect accuracy, nor can it verify that a given address is correct/valid.

## How to use the usaddress python library

1. Install usaddress with [pip](https://pip.readthedocs.io/en/latest/quickstart.html), a tool for installing and managing python packages ([beginner's guide here](http://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/)).

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

### Building & testing the code in this repo

To build a development version of usaddress on your machine, run the following code in your command line:
  
  ```
  git clone https://github.com/datamade/usaddress.git  
  cd usaddress  
  pip install -r requirements.txt  
  python setup.py develop  
  parserator train training/labeled.xml usaddress  
  ```  

Then run the testing suite to confirm that everything is working properly:

   ```
   nosetests .
   ```
   
Having trouble building the code? [Open an issue](https://github.com/datamade/usaddress/issues/new) and we'd be glad to help you troubleshoot.

### Adding new training data

If usaddress is consistently failing on particular address patterns, you can adjust the parser's behavior by adding new training data to the model. [Follow our guide in the training directory](https://github.com/datamade/usaddress/blob/master/training/README.md), and be sure to make a pull request so that we can incorporate your contribution into our next release!

## Important links

* Web Interface: https://parserator.datamade.us/usaddress
* Python Package Distribution: https://pypi.python.org/pypi/usaddress
* Python Package Documentation: https://usaddress.readthedocs.io/
* API Documentation: https://parserator.datamade.us/api-docs
* Repository: https://github.com/datamade/usaddress
* Issues: https://github.com/datamade/usaddress/issues
* Blog post: http://datamade.us/blog/parsing-addresses-with-usaddress

## Team

* [Forest Gregg](https://github.com/fgregg), DataMade
* [Cathy Deng](https://github.com/cathydeng), DataMade
* [Miroslav Batchkarov](http://mbatchkarov.github.io), University of Sussex
* [Jean Cochrane](https://github.com/jeancochrane), DataMade

## Bad Parses / Bugs

Report issues in the [issue tracker](https://github.com/datamade/usaddress/issues)

If an address was parsed incorrectly, please let us know! You can either [open an issue](https://github.com/datamade/usaddress/issues/new) or (if you're adventurous) [add new training data to improve the parser's model.](https://github.com/datamade/usaddress/blob/master/training/README.md) When possible, please send over a few real-world examples of similar address patterns, along with some info about the source of the data - this will help us train the parser and improve its performance.

If something in the library is not behaving intuitively, it is a bug, and should be reported.

## Note on Patches/Pull Requests
 
* Fork the project.
* Make your feature addition or bug fix.
* Send us a pull request. Bonus points for topic branches!

## Copyright

Copyright (c) 2014 Atlanta Journal Constitution. Released under the [MIT License](https://github.com/datamade/usaddress/blob/master/LICENSE).
