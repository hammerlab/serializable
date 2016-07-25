# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Helper functions for deconstructing classes, functions, and user-defined
objects into serializable types.
"""

from types import FunctionType, BuiltinFunctionType

from .primtive_types import return_primitive


def _lookup_value(module_string, name, _cache={}):
    key = (module_string, name)
    if key in _cache:
        value = _cache[key]
    else:
        module_parts = module_string.split(".")
        attribute_list = module_parts[1:] + name.split(".")
        # traverse the chain of imports and nested classes to get to the
        # actual class value
        value = __import__(module_parts[0])
        for attribute_name in attribute_list:
            value = getattr(value, attribute_name)
        _cache[key] = value
    return value


def class_from_serializable_representation(class_repr):
    """
    Given the name of a module and a class it contains, imports that module
    and gets the class object from it.
    """
    return _lookup_value(class_repr["__module__"], class_repr["__name__"])

def class_to_serializable_representation(cls):
    """
    Given a class, return two strings:
        - fully qualified import path for its module
        - name of the class

    The class can be reconstructed from these two strings by calling
    class_from_serializable_representation.
    """
    return {"__module__": cls.__module__, "__name__": cls.__name__}

@return_primitive
def function_from_serializable_representation(fn_repr):
    """
    Given the name of a module and a function it contains, imports that module
    and gets the class object from it.
    """
    return _lookup_value(fn_repr["__module__"], fn_repr["__name__"])

@return_primitive
def function_to_serializable_representation(fn):
    """
    Converts a Python function into a serializable representation. Does not
    currently work for methods or functions with closure data.
    """
    if type(fn) not in (FunctionType, BuiltinFunctionType):
        raise ValueError(
            "Can't serialize %s : %s, must be globally defined function" % (
                fn, type(fn),))

    if hasattr(fn, "__closure__") and fn.__closure__ is not None:
        raise ValueError("No serializable representation for closure %s" % (fn,))

    return {"__module__": fn.__module__, "__name__": fn.__name__}

@return_primitive
def object_to_serializable_representation(obj):
    """
    Given an instance of a Python object, returns a tuple whose
    first element is a primitive representation of the class and whose
    second element is a dictionary of instance data.
    """
    if not hasattr(obj, 'to_dict'):
        raise ValueError("Expected %s to have method to_dict()" % (obj,))

    state_dict = obj.to_dict()
    class_representation = class_to_serializable_representation(obj.__class__)
    state_dict["__class__"] = class_representation
    return state_dict

@return_primitive
def object_from_serializable_representation(obj_repr):
    """
    Given a primitive representation of some object, reconstructs
    the class from its module and class names and then instantiates. Returns
    instance object.
    """
    class_repr = obj_repr.pop("__class__")
    subclass = class_from_serializable_representation(class_repr)
    return subclass.from_dict(obj_repr)


@return_primitive
def to_serializable(x):
    """
    Convert an instance of Serializable or a primitive collection containing
    such instances into serializable types.
    """
    if isinstance(x, (tuple, list)):
        return x.__class__([to_serializable(element) for element in x])
    elif isinstance(x, dict):
        result = x.__class__()
        for (k, v) in x.items():
            result[k] = to_serializable(v)
        return result
    # if value wasn't a primitive scalar or collection then it needs to
    # either implement to_dict (instances of Serializable) or _asdict
    # (named tuples)

    state_dictionary = None
    if hasattr(x, "to_dict"):
        state_dictionary = x.to_dict()
    elif hasattr(x, "_asdict"):
        state_dictionary = x._asdict()
    if state_dictionary is None:
        raise ValueError(
            "Cannot convert %s : %s to serializable representation" % (
                x, type(x)))
    state_dictionary = to_serializable(state_dictionary)
    state_dictionary["__class__"] = class_to_serializable_representation(x.__class__)
    return state_dictionary

@return_primitive
def from_serializable(x):
    t = type(x)
    if t in (tuple, list):
        return t([from_serializable(element) for element in x])
    elif t is dict:
        if "__name__" in x:
            return
        result = x.__class__()
        for (k, v) in x.items():
            result[k] = to_serializable(v)
        return result
    else:
        raise TypeError(
            "Cannot convert %s : %s to serializable representation" % (
                x, type(x)))
