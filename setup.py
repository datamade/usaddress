try:
    from setuptools import setup
except ImportError :
    raise ImportError("setuptools module required, please go to https://pypi.python.org/pypi/setuptools and follow the instructions for installing setuptools")

setup(
    version='0.5.8',
    url='https://github.com/datamade/usaddress',
    description='Parse US addresses using conditional random fields',
    name='usaddress',
    packages=['usaddress'],
    package_data={'usaddress' : ['usaddr.crfsuite']},
    license='The MIT License: http://www.opensource.org/licenses/mit-license.php',
    install_requires=['python-crfsuite>=0.7',
                      'future',
                      'probableparsing'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis'],
    long_description="""
    usaddress is a python library for parsing unstructured address strings into address components, using advanced NLP methods.

    From the python interpreter:

    >>> import usaddress
    >>> usaddress.parse('123 Main St. Suite 100 Chicago, IL')
    [('123', 'AddressNumber'), 
     ('Main', 'StreetName'), 
     ('St.', 'StreetNamePostType'), 
     ('Suite', 'OccupancyType'), 
     ('100', 'OccupancyIdentifier'), 
     ('Chicago,', 'PlaceName'), 
     ('IL', 'StateName')]
    """
)
