try:
    from setuptools import setup, Extension
except ImportError :
    raise ImportError("setuptools module required, please go to https://pypi.python.org/pypi/setuptools and follow the instructions for installing setuptools")


setup(
    name='usaddress',
    packages=['usaddress'],
    license='The MIT License: http://www.opensource.org/licenses/mit-license.php',
    )
