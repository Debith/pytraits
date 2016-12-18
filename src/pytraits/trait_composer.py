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
from pytraits.domain import TraitFactory

__metaclass__ = type

def add_traits(target, *traits, **resolutions):
    """ Bind new traits to given object.

    Args:
        target: Object of any type that is going to be extended with traits
        traits: Tuple of traits as object and strings or callables or functions.
        resolutions: dictionary of conflict resolutions to solve situations
                     where multiple methods or properties of same name are
                     encountered in traits.

    >>> class ExampleClass:
    ...    def example_method(self):
    ...        return None
    ...
    >>> class ExampleTrait:
    ...    def other_method(self):
    ...        return 42
    ...
    >>> add_traits(ExampleClass, ExampleTrait)
    >>> ExampleClass().other_method()
    42
    """
    # Return immediately, if no traits provided.
    if not len(traits):
        return

    # TODO: DI here
    trait_target = TraitFactory["TraitTargetInspector"](target)
    trait_resolutions = TraitFactory["Resolutions"](resolutions)

    # Just prepare object to start the work and get done with it.
    trait_collection = TraitFactory["Traits"](traits)

    # This call puts all gears moving. Each trait in turn is being added
    # to target object. Resolutions are used to solve any conflicts along
    # the way.
    trait_collection.compose(trait_target, trait_resolutions)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
