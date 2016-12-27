#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
import unittest

from pytraits.infrastructure.utils import flatten
from pytraits.domain.model.class_object import ClassObject

from testdata import *

__metaclass__ = type


class TestClassObject(unittest.TestCase):
    def setUp(self):
        self.classtype = ClassObject(ExampleClass)
        self.dir = dir(self.classtype)
        self.items = dict(self.classtype.items())

    def __getitem__(self, key):
        return self.items[key]

    def typename(self, key):
        return type(self[key]).__name__

    def test_has_a_custom_dir(self):
        self.assertEqual(self.dir,
                         ['TEST_ATTR_PUB', 'test_classmethod', 'test_method',
                          'test_property', 'test_staticmethod'])

    def test_supports_showing_items(self):
        self.assertEqual(self.typename("TEST_ATTR_PUB"), "str")
        self.assertEqual(self.typename("test_classmethod"), "classmethod")
        self.assertEqual(self.typename("test_method"), "function")
        self.assertEqual(self.typename("test_property"), "property")
        self.assertEqual(self.typename("test_staticmethod"), "staticmethod")

    def test_supports_iteration(self):
        iterated = sorted([str(f) for f in self.classtype])
        self.assertEqual(iterated[0], "classmethod")
        self.assertEqual(iterated[1], "method")
        self.assertEqual(iterated[2], "property")
        self.assertEqual(iterated[3], "staticmethod")


if __name__ == '__main__':
    unittest.main()
