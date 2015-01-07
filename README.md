usaddress
=================
usaddress is a python library for parsing unstructured address strings into address components, using advanced NLP methods. Try it out on our [web interface](http://usaddress.datamade.us/)!

**What this can do:** Using a probabilistic model, it makes (very educated) guesses in identifying address components, even in tricky cases where rule-based parsers typically break down.

**What this cannot do:** It cannot identify address components with perfect accuracy, nor can it verify that a given address is correct/valid.

We currently only support `python 2.7`

## How to use usaddress
1. Install usaddress
  
  ```bash
  pip install usaddress
  ```
2. Parse some addresses!
  
  ```python
  >>> import usaddress
  >>> usaddress.parse('123 Main St. Suite 100 Chicago, IL')
  [('123', 'AddressNumber'), 
  ('Main', 'StreetName'), 
  ('St.', 'StreetNamePostType'), 
  ('Suite', 'OccupancyType'), 
  ('100', 'OccupancyIdentifier'), 
  ('Chicago,', 'PlaceName'), 
  ('IL', 'StateName')]
  ```

## For the nerds:
usaddress uses parserator, a library for making and improving probabilistic parsers - specifically, parsers that use [python-crfsuite](https://github.com/tpeng/python-crfsuite)'s implementation of conditional random fields. Parserator allows you to train the usaddress parser's model (a .crfsuite settings file) on labeled training data, and provides tools for easily adding new labeled training data.
#### Building & testing development code
  
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
  This will start a console labeling task, where you will be prompted to label raw strings via the command line. For more info on using parserator, see the [parserator documentation](https://github.com/datamade/parserator/blob/master/README.md).  
#### Re-training the model  
  If you've added new training data, you will need to re-train the model. 
  
  ```
  parserator train [traindata] usaddress  
  ```  
  To set multiple files as traindata, separate them with commas (e.g. ```training/foo.xml,training/bar.xml```)


### Important links

* Documentation: http://usaddress.rtfd.org/
* Repository: https://github.com/datamade/usaddress
* Issues: https://github.com/datamade/usaddress/issues
* Distribution: https://pypi.python.org/pypi/usaddress

### Team

* [Forest Gregg](https://github.com/fgregg), DataMade
* [Cathy Deng](https://github.com/cathydeng), DataMade
* [Miroslav Batchkarov](http://mbatchkarov.github.io), University of Sussex

### Errors / Bugs

If something is not behaving intuitively, it is a bug, and should be reported.
[Report it here](https://github.com/datamade/usaddress/issues)

### Note on Patches/Pull Requests
 
* Fork the project.
* Make your feature addition or bug fix.
* Send us a pull request. Bonus points for topic branches.

### Copyright

Copyright (c) 2014 Atlanta Journal Constitution. Released under the [MIT License](https://github.com/datamade/usaddress/blob/master/LICENSE).
