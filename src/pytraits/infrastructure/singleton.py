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
__metaclass__ = type

class SingletonError(Exception): pass


class Singleton(type):
    """ Turn the class to immutable singleton.
    """
    def __call__(self, *args, **kwargs):
        try:
            return self.__instance
        except AttributeError:
            def raise_immutable_exception(*args):
                raise SingletonError('Singletons are immutable!')

            self.__instance = super(Singleton, self).__call__(*args, **kwargs)
            self.__delitem__ = raise_immutable_exception
            self.__delattr__ = raise_immutable_exception
            self.__setitem__ = raise_immutable_exception
            self.__setattr__ = raise_immutable_exception
            return self.__instance


if __name__ == "__main__":
    import doctest
    doctest.testmod()
