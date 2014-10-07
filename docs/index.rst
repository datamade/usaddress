.. usaddress documentation master file, created by
   sphinx-quickstart on Thu Oct  2 15:12:14 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

================
usaddress |release|
================

usaddress is a python library for parsing unstructured address strings into address components, using advanced NLP methods.


   .. code:: python

      >>> import usaddress
      >>> usaddress.parse('123 Main St. Suite 100 Chicago, IL')
      [('123', 'AddressNumber'), 
       ('Main', 'StreetName'), 
       ('St.', 'StreetNamePostType'), 
       ('Suite', 'OccupancyType'), 
       ('100', 'OccupancyIdentifier'), 
       ('Chicago,', 'PlaceName'), 
       ('IL', 'StateName')]

Installation
============

.. code-block:: bash

   pip install usaddress

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


Important links
===============

* Documentation: http://usaddress.rtfd.org/
* Repository: https://github.com/datamade/usaddress
* Issues: https://github.com/datamade/usaddress/issues
* Distribution: https://pypi.python.org/pypi/usaddress

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

