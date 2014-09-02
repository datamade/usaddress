us-address-parser
=================
us-address-parser is a python library for parsing unstructured address strings into address components, using advanced NLP methods.

To build and test development code.

```bash
> pip install -r requirements.txt
> python setup.py develop
> python training/training.py
> nosetests .
```

From the python interpereter, you can

```python
>>> import usaddress
>>> usaddress.parse('123 Main St. Suite 100 Chicago, IL')
[('123', 'AddressNumber'), ('Main', 'StreetName'), ('St.', 'StreetNamePostType'), 
('Suite', 'OccupancyType'), ('100', 'OccupancyIdentifier'), ('Chicago', 'PlaceName'), 
(',', 'Null'), ('IL', 'StateName')]
```
