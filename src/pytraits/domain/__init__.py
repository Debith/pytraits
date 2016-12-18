# -*- coding: utf-8 -*-
#!/usr/bin/python -tt
from pytraits.domain.shared.factory import TraitFactory
from pytraits.domain.shared.inspectors import TraitSourceInspector, TraitTargetInspector

# TODO: Look how to make this automatic
from pytraits.domain.model.class_object import ClassObject
from pytraits.domain.model.instance_object import InstanceObject
from pytraits.domain.model.property_object import PropertyObject
from pytraits.domain.model.routine_object import (FunctionObject,
                                                       RoutineObject,
                                                       MethodObject,
                                                       ClassMethodObject,
                                                       StaticMethodObject,
                                                       BuiltinObject)
from pytraits.domain.model.resolutions import Resolutions
from pytraits.domain.model.trait_object import TraitObject

from pytraits.domain.services.compiler import Compiler
from pytraits.domain.services.composer import Composer
from pytraits.domain.services.traits import Traits

# TODO: Create a base class for all these domain classes.
TraitObject.FACTORY = TraitFactory()
Compiler.FACTORY = TraitFactory()
Composer.FACTORY = TraitFactory()
Traits.FACTORY = TraitFactory()

PRIMITIVES = (ClassObject,
    InstanceObject,
    PropertyObject,
    FunctionObject,
    RoutineObject,
    MethodObject,
    ClassMethodObject,
    StaticMethodObject,
    BuiltinObject, )

assert id(TraitObject.FACTORY) == id(Compiler.FACTORY)

if not TraitFactory().exists(Traits):
    # TODO: Refactor to be more automatic
    for primitive in PRIMITIVES:
        primitive.hook_into(TraitSourceInspector)
        primitive.hook_into(TraitTargetInspector)

    TraitFactory.register(TraitSourceInspector, TraitTargetInspector)
    TraitFactory.register(*PRIMITIVES)
    TraitFactory.register(Compiler, Composer, Resolutions, Traits)

__all__ = ["TraitFactory"]