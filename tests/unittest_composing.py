#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
import unittest

from utils import for_examples

from pytraits.infrastructure.utils import get_func_name
from pytraits.domain.composing.composer import BasicComposer
from pytraits.domain.composing.resolutions import Resolutions

__metaclass__ = type

def empty_func(self):
    pass


class TestDummy:
    def __private_func(self): pass
    def _hidden_func(self): pass
    def public_func(self): pass


class Function:
    def __init__(self, func):
        self._func = func

    @property
    def name(self):
        return self._func.__name__


class TestCompiler(unittest.TestCase):
    def setUp(self):
        self.test_class = type("TestClass", (), {})
        self.names = dict()
        self.resolutions = Resolutions(self.names)

    def test_compose_bound_function(self):
        self.composer = BasicComposer(self.test_class, Function(TestDummy.public_func))
        self.composer.compose(self.resolutions)

    def test_compose_unbound_function(self):
        pass


if __name__ == '__main__':
    unittest.main()
