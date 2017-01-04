#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
'''
   Copyright 2014-2015 Teppo Perä

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

from pytraits.infrastructure.magic import meta_make
from pytraits.infrastructure.exception import TraitException


__metaclass__ = type

class Composer:
    """ Factory object for composers.

    This factory object is called for each pair of object that is being composed
    together. Composer object is created for identified and supported pairs of
    target and source objects. Some combinations can require special behavior
    which these composer objects need to address.

    Composing itself is a process, where source object is first recompiled
    and then bound against the new target. Compiling is required to alter the
    content of code object to match target object and binding is required to
    be able to call the function.
    """
    # Dictionary of registered composers. Each composer is identified by
    # two strings (target type names) as a key and all composers are added here
    # by ComposerMeta metaclass.
    __COMPOSERS = dict()

    @classmethod
    def register(cls, key, composer):
        """ Stores composer with given key for the future use. """
        cls.__COMPOSERS[key] = composer

    def __call__(self, target, source):
        """ Factory method that selects correct composer for target and source. """
        # Each Hookable has a string representation that can be used to
        # select correct composer.
        joined = str(target), str(source)
        try:
            return self.__COMPOSERS[joined](target, source)
        except KeyError:
            msg = "{target} '{targetqname}' and {source} '{sourceqname}' is not supported combination!"
            msg = msg.format(target=str(target),
                             targetqname=target.qualname,
                             source=str(source),
                             sourceqname=source.qualname)
            raise TraitException(msg)


class ComposerMeta(type):
    """ Automatically registers all composers to Composer factory class. """
    def __init__(cls, name, bases, attrs):
        """ Handles registering of classes to Composer factory class.

        This function is called when initializing the class object. Any class
        that is identified as a composer (=has defined CAN_COMPOSE attribute)
        is registered to factory.
        """
        for support in getattr(cls, "CAN_COMPOSE", ()):
            Composer.register(support, cls)

    def __call__(cls, target, source):
        """ Initializes class instance.

        This function is roughly equivalent to class.__init__. Here we
        initialize the composer object.
        """
        instance = super(ComposerMeta, cls).__call__()
        instance.target = target
        instance.source = source
        return instance


class BasicComposer:
    """ Basic composer for simple types.

    This class handles composition of most of the target - source pairs.
    """
    CAN_COMPOSE = [('class', 'method'), ('instance', 'method'),
                   ('class', 'classmethod'), ('instance', 'classmethod'),
                   ('class', 'staticmethod'), ('instance', 'staticmethod'),
                   ('class', 'builtin'), ('instance', 'builtin'),
                   ('class', 'property')]

    def compose(self, resolutions):
        """ Composes trait to target object.

        General flow of composition is:
            - Resolve the name of the trait in target object.
            - Compile trait against the target (as if it was written to it.)
            - Bind the compiled trait to target.
        """
        name = resolutions.resolve(self.source.name)
        compiled = self.source.recompile(self.target, name)
        bound = self.source.rebind(self.target, compiled)
        self.target[name] = bound
        assert hasattr(self.target.object, name)


class Property2Instance:
    """ Special handling for composing properties to instances. """
    CAN_COMPOSE = [('instance', 'property')]

    def compose(self, resolutions):
        """ Composes property trait to instance target.

        Composing properties to instances is bit trickier business, since
        properties are descriptors by their nature and they work only on class
        level. If we assign the property to instance's dictionary (instance.__dict__),
        it won't work at all. If we assign the property to instance's class'
        dictionary (instance.__class__.__dict__), it will work, but the property
        will go to any other instance of that class too. That's why, we create
        a clone of the class and set it to instance.
        """
        # Modify target instance so that changing its class content won't
        # affect other classes.
        self.target.forge()

        # Resolve the name and recompile
        name = resolutions.resolve(self.source.name)
        compiled = self.source.recompile(self.target, name)

        # Assing property to instance's class.
        # TODO: Figure out pretty way to do this by calling target's function.
        setattr(self.target.compile_target, name, compiled)

BasicComposer = meta_make(BasicComposer, ComposerMeta)
Property2Instance = meta_make(Property2Instance, ComposerMeta)