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

# TODO: Rewrite docs
from __future__ import absolute_import, division, print_function
import sys

import inspect
from collections import OrderedDict as odict

__metaclass__ = type
__all__ = ["Inspector"]


def isproperty(object):
    """ Convinience method to check if object is property. """
    return isinstance(object, property)


def isbuiltin(object):
    """ Convinience method to check if object is builtin. """
    if inspect.isbuiltin(object):
        return True

    return getattr(object, '__module__', None) == 'builtins'


def isclass(object):
    """ Convinience method to check if object is class. """
    if not inspect.isclass(object):
        return False
    if isbuiltin(object):
        return False
    return type not in inspect.getmro(object)


def ismetaclass(object):
    """ Convinience method to check if object is meta class. """
    if not inspect.isclass(object):
        return False
    if isbuiltin(object):
        return False
    return type in inspect.getmro(object)


def _get_dict_function(object):
    try:
        return object.__self__.__dict__[object.__name__]
    except (AttributeError, KeyError):
        return None


def isclassmethod(object):
    """ Convinience method to check if object is class method. """
    if isinstance(object, classmethod):
        return True

    # Let's not give up quite yet.
    original = _get_dict_function(object)
    return isinstance(original, classmethod)


def isdatatype(object):
    """ Convinience method to check if object is data type. """
    if sys.version_info.major >= 3:
        return isinstance(object, (str, int, bool, float, type(None)))
    else:
        return isinstance(object, (basestring, int, bool, float, type(None)))


def isstaticmethod(candidate):
    """ Convinience method to check if object is static method.

    >>> class Example:
    ...     @staticmethod
    ...     def i_am_static(): pass
    ...
    >>> isstaticmethod(Example.i_am_static)
    True

    """
    # TODO: This can only identify those static methods that
    #       are directly taken from object's dict. Like
    #       Class.__dict__[staticmethodname]
    if isinstance(candidate, staticmethod):
        return True

    if not inspect.isfunction(candidate):
        return False

    # Module level functions are disqualified here.
    if sys.version_info >= (3, 2) and "." not in getattr(candidate, "__qualname__", ""):
        return False

    # It is either method (accessed as Class.method) or staticfunction
    # TODO: Is this really the only way?
    args = candidate.__code__.co_varnames
    if len(args) == 0:
        return True

    return args[0] != 'self'


def isclassinstance(object):
    """ Convinience method to check if object is class instance. """
    if not hasattr(object, "__class__"):
        return False
    if isbuiltin(object.__class__):
        return False
    return True


class Inspector:
    """ Class for inspecting objects.

    This class can be used to identify type of objects passed in. For that
    purpose, the inspector provides 'inspect' and 'inspect_many' functions
    as well as the instance is directly callable for inspecting single object.

    >>> inspector = Inspector()
    >>> inspector(Inspector) == 'class'
    True
    >>> inspector.inspect(inspector) == 'instance'
    True
    >>> inspector.inspect_many(inspect, min) == [u'module', u'builtin']
    True

    For further convenience, and to behave similarily with inspect
    module, this class implements special behavior for checking types.
    Any known type in this class will automatically have corresponding
    function with 'is_'-prefix. That special function will essentially
    call Inspector.inspect function with given object as parameter and
    compares whether the types are matching. Passing Inspector instance
    to dir() function reveals these special functions.

    >>> inspector.is_module(inspect)
    True
    """
    TYPES = odict([('builtin', isbuiltin),
                   ('module', inspect.ismodule),
                   ('property', isproperty),
                   ('code', inspect.iscode),
                   ('generator', inspect.isgenerator),
                   ('traceback', inspect.istraceback),
                   ('frame', inspect.isframe),
                   ('staticmethod', isstaticmethod),
                   ('classmethod', isclassmethod),
                   ('method', inspect.ismethod),
                   ('function', inspect.isfunction),
                   ('routine', inspect.isroutine),
                   ('methoddescriptor', inspect.ismethoddescriptor),
                   ('generatorfunction', inspect.isgeneratorfunction),
                   ('datadescriptor', inspect.isdatadescriptor),
                   ('memberdescriptor', inspect.ismemberdescriptor),
                   ('getsetdescriptor', inspect.isgetsetdescriptor),
                   ('descriptor', isclassmethod),
                   ('metaclass', ismetaclass),
                   ('class', isclass),
                   ('data', isdatatype),
                   ('instance', isclassinstance)])
    TYPENAMES = tuple(TYPES.keys())

    def __init__(self, custom_types = None):
        self.__custom_types = custom_types or odict()
        self.__hooks = odict()
        self.__default_hook = None

    def __iter__(self):
        # Favor custom types. It is possible to override default behavior.
        for custom_type in self.__custom_types.items():
            yield custom_type
        for default_type in self.TYPES.items():
            yield default_type

    def __getitem__(self, typename):
        """ Get check function for typename

        >>> Inspector()["class"].__name__
        'isclass'
        """
        try:
            return self.TYPES[typename]
        except KeyError:
            return self.__custom_types[typename]

    def __dir__(self):
        """ Returns a list of known attributes.

        In addition to list of written functions, any special
        function with 'is_'-prefix are included in the list.

        >>> "is_module" in dir(Inspector)
        False
        >>> "is_module" in dir(Inspector())
        True
        """
        extras = ["is_%s" % typename for typename in self.typenames]

        return dir(self.__class__) + extras

    def __getattr__(self, attr):
        """ Retrieves attribute or constructed inspect method.

        Convenience mechanism to make object identification simple.
        """
        try:
            # TODO: Why super call does not work here?
            return object.__getattr__(self, attr)
        except AttributeError:
            # normal way does not work, but maybe user is wanting to
            # make a direct check. To directly refer known types, the
            # attribute needs to have special prefix 'is'.
            if not attr.startswith("is_"):
                raise

            typename = attr[3:]

            if typename not in self.typenames:
                raise TypeError("Unidentified type '%s'" % typename)

            return lambda obj: self(obj) == typename

    def inspect_many(self, *objects):
        """ Identify all arguments to certain type.

        This function identifies all arguments to certain type and for those
        types that have a registered hook, will be called with given object for
        any special handling needed for that type.

        Returns:
            List of identified objects.
        """
        return [self.inspect(o) for o in objects]

    def inspect(self, object, hooked_only=True):
        """ Identifies type of single object.

        Loops over every type check defined in Inspector.TYPES dictionary and
        returns type for the first check that qualifies the object.

        Args:
            object (anything): Object needs to be identified.
            hooked_only (bool): Switch to decide whether all types are checked
                                or only hooks. If no hooks are defined then
                                check is done against all types.
                                Default is only hooked.

        Return:
            If no hook found, then name of object type.
            If hook is found, then any object returned by hook.
        """
        for typename, check in self:
            # Skip checks if it is not required for this type.
            if hooked_only and len(self.__hooks) and typename not in self.__hooks:
                continue

            # Keep going if object is not matching.
            if not check(object):
                continue

            if typename in self.__hooks:
                return self.__hooks[typename](object)
            elif self.__default_hook:
                return self.__default_hook(object)
            else:
                return typename

        # Situation that occurs when receiving a type checks are not covering.
        if self.__default_hook:
            return self.__default_hook(object)

        type_name = getattr(object, "__name__", object.__class__.__name__)
        raise TypeError("Could not identify object '%s' from list: %s" % (type_name, self.typenames))

    __call__ = inspect

    def add_typecheck(self, name, callable=None):
        """ Adds typecheck for given name.

        This method allows adding custom typechecks. It's possible to either
        add completely new checks or override existing ones.

        Args:
            name: Name of the type check. If the name is found from the
                  Inspector.TYPES list, it will be overridden as new check for
                  that type. If name is completely new one, then it will be
                  added as a custom typecheck.
            callable: Any callable object taking single argument as parameter
                      and returns True or False as an answer. If None, existing
                      type check is promoted to be custom. This changes priority
                      of checks so that desired checks are run earlier.

        Raises:
            ValueError when there already is a custom type check for given name.
        """
        if name in self.__custom_types:
            raise ValueError("Type '{}' already exists".format(name))
        self.__custom_types[name] = callable or self.TYPES[name]

    def del_typecheck(self, name):
        """ Removes custom type checks by name. """
        try:
            del self.__custom_types[name]
        except KeyError:
            pass

    def add_hook(self, name, callable):
        """ Add hook that is called for given type.

        Args:
            name: Type name.
            callable: Any callable taking object as an argument.
        """
        assert name in self.typenames, "'{}' not in '{}'".format(name, self.typenames)
        self.__hooks[name] = callable

    def del_hook(self, name):
        """ Removes a hook by name. """
        try:
            del self.__hooks[name]
        except KeyError:
            pass

    def set_default_hook(self, callable):
        self.__default_hook = callable

    def del_default_hook(self):
        self.__default_hook = None

    def clear(self):
        """ Removes all the hooks. """
        self.__hooks = odict()

    @property
    def hooks(self):
        """ Tuple of registered hooks. """
        return tuple(self.__hooks.keys())

    @property
    def typenames(self):
        """ Tuple of supported types """
        return tuple((item[0] for item in self))


# Default inspector instance, that can be used directly for general
# type checks. It can be modified, but recommendation is to create
# own instances which can be customized freely.
inspector = Inspector()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
