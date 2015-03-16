.. usaddress documentation master file, created by
   sphinx-quickstart on Thu Oct  2 15:12:14 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

================
usaddress |release|
================

usaddress is a python library for parsing unstructured address strings into address components, using advanced NLP methods.

Installation
============

.. code-block:: bash

   pip install usaddress

Usage
============
The ``parse`` method will split your address string into components, and label each component.
   .. code:: python

      >>> import usaddress
      >>> usaddress.parse('Robie House, 5757 South Woodlawn Avenue, Chicago, IL 60637')
      [('Robie', 'BuildingName'), 
      ('House,', 'BuildingName'), 
      ('5757', 'AddressNumber'), 
      ('South', 'StreetNamePreDirectional'), 
      ('Woodlawn', 'StreetName'), 
      ('Avenue,', 'StreetNamePostType'), 
      ('Chicago,', 'PlaceName'), 
      ('IL', 'StateName'), 
      ('60637', 'ZipCode')]

The ``tag`` method will try to be a little smarter - it will merge consecutive components & strip commas, as well as return an address type (``Street Address``, ``Intersection``, ``PO Box``, or ``Ambiguous``)
   .. code:: python

      >>> import usaddress
      >>> usaddress.tag('Robie House, 5757 South Woodlawn Avenue, Chicago, IL 60637')
      (OrderedDict([
      ('BuildingName', 'Robie House'), 
      ('AddressNumber', '5757'), 
      ('StreetNamePreDirectional', 'South'), 
      ('StreetName', 'Woodlawn'), 
      ('StreetNamePostType', 'Avenue'), 
      ('PlaceName', 'Chicago'), 
      ('StateName', 'IL'), 
      ('ZipCode', '60637')]), 
      'Street Address')
      >>> usaddress.tag('State & Lake, Chicago')
      (OrderedDict([
      ('StreetName', 'State'), 
      ('IntersectionSeparator', '&'), 
      ('SecondStreetName', 'Lake'), 
      ('PlaceName', 'Chicago')]), 
      'Intersection')
      >>> usaddress.tag('P.O. Box 123, Chicago, IL')
      (OrderedDict([
      ('USPSBoxType', 'P.O. Box'), 
      ('USPSBoxID', '123'), 
      ('PlaceName', 'Chicago'), 
      ('StateName', 'IL')]), 
      'PO Box')


Details
=======

The address components are based upon the `United States Thoroughfare, Landmark, and Postal Address Data Standard <http://www.urisa.org/advocacy/united-states-thoroughfare-landmark-and-postal-address-data-standard/>`__, and usaddress knows about the following types of components: 

* AddressNumber
* StreetName
* PlaceName
* StateName
* ZipCode
* AddressNumberPrefix
* AddressNumberSuffix
* StreetNamePreDirectional
* StreetNamePostDirectional
* StreetNamePreModifier
* StreetNamePostType
* StreetNamePreType
* USPSBoxType
* USPSBoxID
* USPSBoxGroupType
* USPSBoxGroupID
* LandmarkName
* CornerOf
* IntersectionSeparator
* OccupancyType
* OccupancyIdentifier
* SubaddressIdentifier
* SubaddressType
* Recipient
* BuildingName
* NotAddress


Important links
===============

* Documentation: http://usaddress.rtfd.org/
* Repository: https://github.com/datamade/usaddress
* Issues: https://github.com/datamade/usaddress/issues
* Distribution: https://pypi.python.org/pypi/usaddress
* Blog Post: http://datamade.us/blog/parsing-addresses-with-usaddress/
* Web Interface: http://parserator.datamade.us/usaddress

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

