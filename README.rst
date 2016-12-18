===============================
pytraits
===============================

| |docs| |travis| |downloads| |wheel| |pyversions|

.. |docs| image:: https://readthedocs.org/projects/pytraits/badge/
    :target: https://readthedocs.org/projects/pytraits
    :alt: Documentation Status

.. |travis| image:: http://img.shields.io/travis/Debith/pytraits/master.png
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/Debith/pytraits

.. |downloads| image:: http://img.shields.io/pypi/dm/pytraits.png
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/pytraits

.. |wheel| image:: https://img.shields.io/pypi/format/pytraits.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/pytraits

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/pytraits.svg

Trait support for Python 3

* Free software: Apache license

Installation
============

::

    pip install pytraits

Documentation
=============

https://pytraits.readthedocs.org/

Development
===========

To run the all tests run::

    tox

About Traits
============

Traits are classes which contain methods that can be used to extend
other classes, similar to mixins, with exception that traits do not use
inheritance. Instead, traits are composed into other classes. That is;
methods, properties and internal state are copied to master object.

The point is to improve code reusability by dividing code into simple
building blocks that can be then combined into actual classes.

Read more from wikipedia: http://en.wikipedia.org/wiki/Traits_class

Look for examples from examples folder.
