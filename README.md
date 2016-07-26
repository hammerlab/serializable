# serializable
Base class with serialization methods for user-defined Python objects

## Usage
Classes which inherit from `Serializable` are given default implementations of
`to_json`, `from_json`, `__reduce__` (for pickling), and other serialization
helpers.

Your derived class must:

* provide a user-defined `to_dict()` method which returns a dictionary.

* The keys of the dictionary returned by `to_dict()` must match the arguments to the `__init__` of your class.

## Limitations

* Nested objects must be (1) other objects which inherit from `Serializable` (2) namedtuples or (3) primitive types.
