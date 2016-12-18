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
import sys


def for_examples(*parameters):
    """
    From StackOverflow:
    http://stackoverflow.com/questions/2798956/python-unittest-generate-multiple-tests-programmatically
    """
    def tuplify(x):
        if not isinstance(x, tuple):
            return (x,)
        return x

    def decorator(method, parameters=parameters):
        for parameter in (tuplify(x) for x in parameters):
            def method_for_parameter(self, method=method, parameter=parameter):
                method(self, *parameter)
            args_for_parameter = ",".join(repr(v) for v in parameter)
            name_for_parameter = method.__name__ + "(" + args_for_parameter + ")"
            frame = sys._getframe(1)
            frame.f_locals[name_for_parameter] = method_for_parameter
        return None
    return decorator
