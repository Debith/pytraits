#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
import unittest

from pytraits import Singleton, SingletonError
from pytraits.infrastructure.magic import meta_make

__metaclass__ = type

class TestSingleton(unittest.TestCase):
    def test_there_can_only_be_one(self):
        class One:
            pass
        One = meta_make(One, Singleton)

        first = One()
        second = One()

        self.assertEqual(id(first), id(second))

    def test_second_initialization_with_arguments_are_ignored(self):
        class OneWithArgs:
            def __init__(self, one, two):
                self.one = one
                self.two = two
        OneWithArgs = meta_make(OneWithArgs, Singleton)

        this = OneWithArgs(1, 2)
        other = OneWithArgs(3, 4)

        self.assertEqual(this.one, 1)
        self.assertEqual(this.two, 2)
        self.assertEqual(other.one, 1)
        self.assertEqual(other.two, 2)
        self.assertEqual(id(this), id(other))

    def test_second_initialization_with_kwarguments_are_ignored(self):
        class OneWithKwArgs:
            def __init__(self, **kwargs):
                self.one = kwargs['one']
                self.two = kwargs['two']
        OneWithKwArgs = meta_make(OneWithKwArgs, Singleton)


        this = OneWithKwArgs(one=1, two=2)
        other = OneWithKwArgs(three=3, four=4)

        self.assertEqual(this.one, 1)
        self.assertEqual(this.two, 2)
        self.assertEqual(other.one, 1)
        self.assertEqual(other.two, 2)
        self.assertEqual(id(this), id(other))

    def test_enforces_immutability(self):
        class NoWrite:
            def __init__(self, begin):
                self.begin = begin
        NoWrite = meta_make(NoWrite, Singleton)

        no_write = NoWrite(3)
        with self.assertRaises(SingletonError):
            no_write.test = 5
        with self.assertRaises(SingletonError):
            no_write.begin = 1
        self.assertEqual(no_write.begin, 3)

if __name__ == '__main__':
    unittest.main()
