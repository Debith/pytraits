#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
'''
   Copyright 2017 Teppo Perä

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

from pytraits.infrastructure.utils import is_container
from pytraits.infrastructure.exception import TraitException
from pytraits.domain.shared.trait_object import TraitObject


__metaclass__ = type


class Composer:
    """
    This class encapsulates logic to compile and bind traits into their new host.

    Depending on type of target object and type of trait, different behavior exist.
    As an attempt to make it simpler to call this composer, fascinating mechanism
    is created. That is, resulting function depends on arguments given for this class.

    Usage:
        composer = Composer[<class>, <function>](<resolutions>)
    """
    def __init__(self):
        self._rules = {
            ('class', 'method'): self._compose,
            ('class', 'classmethod'): self._compose,
            ('class', 'staticmethod'): self._compose,
            ('class', 'builtin'): self._compose,
            ('class', 'property'): self._compose,
            ('instance', 'method'): self._compose,
            ('instance', 'classmethod'): self._compose,
            ('instance', 'staticmethod'): self._compose,
            ('instance', 'builtin'): self._compose,
            ('instance', 'property'): self._compose_property_to_instance
        }
        self._target = None
        self._source = None

    def __getitem__(self, keys):
        """
        Accessor function to determine correct method to handle composing. Stores
        passed objects in order to avoid resending them in function call.
        """
        assert is_container(keys), "Ensure keys is tuple or list containing target and source"
        assert len(keys) == 2, "Expected 2 keys, got %d" % len(keys)

        self._target = keys[0]
        self._source = keys[1]

        return self._rules[str(self._target), str(self._source)]

    def _compose(self, resolutions):
        """ Composes trait to target object.

        This function is able compile and bind most of the traits into new host.
        """
        assert self._target and self._source

        name = resolutions.resolve(self._source.name)
        compiled = self._source.recompile(self._target, name)
        bound = self._source.rebind(self._target, compiled)
        self._target[name] = bound
        assert hasattr(self._target.object, name)


    def _compose_property_to_instance(self, resolutions):
        """ Composes property trait to instance target.

        Composing properties to instances is bit trickier business, since
        properties are descriptors by their nature and they work only on class
        level. If we assign the property to instance's dictionary (instance.__dict__),
        it won't work at all. If we assign the property to instance's class'
        dictionary (instance.__class__.__dict__), it will work, but the property
        will go to any other instance of that class too. That's why, we create
        a clone of the class and set it to instance.
        """
        assert self._target and self._source

        # Modify target instance so that changing its class content won't
        # affect other classes.
        self._target.forge()

        # Resolve the name and recompile
        name = resolutions.resolve(self._source.name)
        compiled = self._source.recompile(self._target, name)

        # Assing property to instance's class.
        # TODO: Figure out pretty way to do this by calling target's function.
        setattr(self._target.compile_target, name, compiled)


if __name__ == "__main__":
    import doctest
    doctest.testmod()