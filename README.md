# serializable
Base class with serialization methods for user-defined Python objects

## Usage
Classes which inherit from `Serializable` are given default implementations of
`to_json`, `from_json`, `__reduce__` (for pickling), and other serialization
helpers.

Your derived class must:

* provide a user-defined `to_dict()` method which returns a dictionary whose keys are strings and whose values are all primitive serializable types (list, dict, int, str, &c).

* The keys of the dictionary returned by `to_dict()` must match the arguments to the `__init__` of your class.

## Limitations

* Nested objects must also inherit from `Serializable` and must be manually converted
to serializable types in `to_dict()` and then reconstructed by overriding the class
method `_reconstruct_nested_objects`.

* Functions defined at the top level of a module can be converted to primtive types with
`function_to_serializable_representation`, but this helper will fail for methods.