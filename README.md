[![Build Status](https://travis-ci.org/iskandr/serializable.svg?branch=master)](https://travis-ci.org/iskandr/serializable)

# serializable
Base class with serialization methods for user-defined Python objects

## Usage
Classes which inherit from `Serializable` are given default implementations of
`to_json`, `from_json`, `__reduce__` (for pickling), and other serialization
helpers.

A class inheriting from `Serializable` must either have a member data field for every argument to `__init__` or, alternatively, must provide a user-defined `to_dict()` method which returns a dictionary whose keys match the arguments to `__init__`.

## Limitations

* Serializable objects must inherit from `Serializable`, be tuples or namedtuples, be serializble primitive types such as dict, list, int, float, or str.

* The serialized representation of objects relies on reserved keywords (such as `"__name__"`, and `"__class__"`), so dictionaries are expect to not contain any keys which begin with two underscores.
