# -*- coding: utf-8 -*-
#!/usr/bin/python -tt
from pytraits.domain.shared.factory import TraitFactory
from pytraits.domain.shared.inspectors import TraitSourceInspector, TraitTargetInspector
from pytraits.infrastructure.exception import TraitException

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

from pytraits.domain.services.compiler import Compiler
from pytraits.domain.services.composer import Composer
from pytraits.domain.services.traits import Traits

# TODO: Create a base class for all these domain classes.
factory = TraitFactory()

PRIMITIVES = (ClassObject,
    InstanceObject,
    PropertyObject,
    FunctionObject,
    RoutineObject,
    MethodObject,
    ClassMethodObject,
    StaticMethodObject,
    BuiltinObject, )

INJECTANBLES = PRIMITIVES + (Traits, RoutineObject)

if not TraitFactory().exists(Traits):
    # TODO: Refactor to be more automatic
    # TODO: Injecting should know difference between factory and service, so that no need
    #       to do decisions here.
    TraitFactory.register(TraitSourceInspector, TraitTargetInspector, Composer, autoinit=False)
    TraitFactory.register(*PRIMITIVES)
    TraitFactory.register(Compiler, Resolutions, Traits)

    for primitive in PRIMITIVES:
        primitive.hook_into(TraitSourceInspector)
        primitive.hook_into(TraitTargetInspector)

    for injectable in INJECTANBLES:
        deps = getattr(injectable, "DEPENDENCIES", {}) or {}
        for name, dep in deps.items():
            try:
                setattr(injectable, name, factory[dep]())
            except:
                print(factory[dep])
                raise TraitException("Error when injecting '%s' dependency to '%s'" % (dep, injectable))


__all__ = ["TraitFactory"]