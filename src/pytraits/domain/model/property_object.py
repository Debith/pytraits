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
from ..shared.trait_object import TraitObject
from .hookable import Hookable

__metaclass__ = type

class PropertyObject(TraitObject, Hookable):
    DEPENDENCIES = dict(_compiler="Compiler", _inspector="TraitSourceInspector")
    INSPECTORS = ('source',)

    def __init__(self, property, name=None):
        assert property is not None

        self.__property = property
        self.__name = name

    def get_func(self, func_name):
        func = getattr(self.__property, func_name, None)
        if func:
            return self._inspector.inspect(func)

    @property
    def name(self):
        return self.__name or self.get_func('fget').name

    def __recompile_func(self, func_name, target, new_name):
        func = self.get_func(func_name)
        if func:
            return func.recompile(target, new_name)

    def recompile(self, target, name):
        getter = self.__recompile_func('fget', target, name)
        setter = self.__recompile_func('fset', target, name)
        deleter = self.__recompile_func('fdel', target, name)

        return property(getter, setter, deleter)

    def rebind(self, target, compiled_property):
        return compiled_property
