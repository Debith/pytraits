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
import os
import sys
import inspect
import itertools
import functools
import importlib
import pkgutil
from os.path import dirname

if sys.version_info >= (3, 5):
    import importlib.util
elif (3, 3) <= sys.version_info < (3, 5):
    from importlib.machinery import SourceFileLoader
else:
    import imp

from pytraits.infrastructure.inspector import inspector
from pytraits.infrastructure.utils import is_sysname


__metaclass__ = type
__all__ = ["meta_make"]


class ErrorMessage:
    """
    Encapsulates building of error message.
    """
    def __init__(self, main_msg, repeat_msg, get_func_name):
        self.__errors = []
        self.__get_func_name = get_func_name
        self.__main_msg = main_msg
        self.__repeat_msg = repeat_msg

    def __bool__(self):
        return bool(self.__errors)

    def __str__(self):
        msg = [self.__main_msg.format(self.__get_func_name)]
        for error in self.__errors:
            msg.append("   - " + self.__repeat_msg.format(**error))
        return "\n".join(msg)

    def set_main_messsage(self, msg):
        self.__main_msg = msg

    def set_repeat_message(self, msg):
        self.__repeat_msg = msg

    def add(self, **kwargs):
        self.__errors.append(kwargs)

    def reset(self):
        self.__errors = []

def iter_package_content(folder):
    for item in os.listdir(folder):
        print(item)


def iter_package_content(folder):
    if sys.version_info >= (3, 5):
        spec = importlib.util.spec_from_file_location("module.name", "/path/to/file.py")
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        foo.MyClass()
    elif (3, 3) <= sys.version_info < (3, 5):
        foo = SourceFileLoader("module.name", "/path/to/file.py").load_module()
        foo.MyClass()
    else:  # For Python 2
        foo = imp.load_source('module.name', '/path/to/file.py')
        foo.MyClass()

    for w1, module_name, w3 in pkgutil.iter_modules([dirname(filename)]):
        module = importlib.import_module("{}.{}".format(package, module_name))

        for object_name in dir(module):
            if is_sysname(object_name):
                continue

            yield getattr(module, object_name)
#            object = getattr(module, object_name)
#
#            try:
#                object.hook_into(TraitSourceInspector)
#                object.hook_into(TraitTargetInspector)
#            except AttributeError:
#                pass


def mangle_name(member, owner=None):
    """ Do Python's name mangling magic here. """
    if hasattr(member, "im_class"):
        owner = member.im_class
        member = member.__name__

    if is_sysname(member):
        return member

    if not member.startswith('__'):
        return member

    return "_%s%s" % (owner, member)


def meta_make(cls, mcls, *members):
    assert inspector.is_metaclass(mcls), "parameter mcls must be metaclass!"

    name = cls.__name__
    bases = cls.__bases__
    attrs = dict([(k, v) for k, v in cls.__dict__.items()])

    return mcls(name, bases, attrs)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
