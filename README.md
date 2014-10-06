usaddress
=================
usaddress is a python library for parsing unstructured address strings into address components, using advanced NLP methods.

**What this can do:** Using a probabilistic model, it makes (very educated) guesses in identifying address components, even in tricky cases where rule-based parsers typically break down.

**What this cannot do:** It cannot identify address components with perfect accuracy, nor can it verify that a given address is correct/valid.

We currently only support `python 2.7`

### Installation
```bash
> pip install usaddress
```

To build and test development code.

```bash
> pip install -r requirements.txt
> python setup.py develop
> python training/training.py
> nosetests .
```

### Usage

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

### Important links

* Documentation: http://usaddress.rtfd.org/
* Repository: https://github.com/datamade/us-address-parser
* Issues: https://github.com/datamade/us-address-parser/issues
* Distribution: https://pypi.python.org/pypi/usaddress

### Team

* [Forest Gregg](https://github.com/fgregg), DataMade
* [Cathy Deng](https://github.com/cathydeng), DataMade

### Errors / Bugs

If something is not behaving intuitively, it is a bug, and should be reported.
[Report it here](https://github.com/datamade/us-address-parser/issues)

### Note on Patches/Pull Requests
 
* Fork the project.
* Make your feature addition or bug fix.
* Send us a pull request. Bonus points for topic branches.

### Copyright

Copyright (c) 2014 Atlanta Journal Constitution. Released under the [MIT License](https://github.com/datamade/us-address-parser/blob/master/LICENSE).
