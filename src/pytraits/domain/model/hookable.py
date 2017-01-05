#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
'''
   Copyright 2014-2017 Teppo Perä

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

from __future__ import absolute_import, division, print_function

__metaclass__ = type

class Hookable:
    def __init__(self, object):
        assert object is not None
        assert not isinstance(object, Hookable), "Detected nesting"

        self._object = object

    @classmethod
    def __str__(cls):
        return cls.__name__.lower().replace('object', '')

    @classmethod
    def hook_into(cls, inspector):
        if inspector.TYPE in cls.INSPECTORS:
            inspector.add_hook(cls.__str__(), cls)

    @property
    def object(self):
        return self._object

    @property
    def qualname(self):
        try:
            return self._object.__qualname__
        except AttributeError:
            return type(self._object).__name__
