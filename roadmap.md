# Zap Roadmap

## The following features are features that will potentially roll out to future Zap versions. (Developers to cross off completed features)
### Each feature will have a list of features (if fitting) that will need to be implemented before that feature will be added.

---

## Contents
- [Namespaces](#namespaces)
- [Module Imports](#module-imports)
- [Local Module Imports](#local-module-imports)
- [Arrays](#arrays)
- [Dictionaries](#dictionaries)
- [Standard Library](#standard-library)
- [File I/O](#file-i/o)

---

## Namespaces
### - [ ] Completed

Namespaces would provide a method of organising modules, compiler directives and other language
features easily. It would use the ``::`` namespace operator to access values inside a namespace.
This feature would come AFTER module imports and local module imports, and the Standard Library.

## Module Imports
### - [ ] Completed

A method of importing modules off of the base preprogrammed Zap modules. Possibly with syntax similar to ``let <local_module_name> = require();`` or just simply ``require();``, however ``using();`` as importing syntax
could also be plausible. This feature would only be for the as aforementioned preprogrammed Zap modules that come with the language. Local module imports would be a later stage, as they could potentially be much 
easier and cleaner to implement if bootstrapped off of this system.

---

## Local Module Imports
### - [ ] Completed

This system would be very similar to the previous module imports, however would be for local files. Once predefined module imports are implemented, it would be very easy to implement this. This would be the same syntax as 
before, however, the local module would always take priority over the preprogrammed module. For example, if importing the module ``math``, and the user has a ``math.zap`` file in their working directory, the code in 
``math.zap`` would be imported instead of the ``math`` preprogrammed module.

---

## Arrays
### - [ ] Completed

Arrays are a fundamental data structure in every modern programming language, and Zap is lacking
in these. Arrays would really increase the usefulness of Zap, and should be capable of storing
any valid Zap value, including strings, numbers, booleans, and potentially even functions.
Some syntax could be ``let nums = [1,2,3];`` and ``output(nums[0])``, so relatively the same
as languages such as Python.

---

## Dictionaries
### - [ ] Completed

Dictionaries allow data to be stored as key value pairs. This would make storing structured
information much easier than relying on variables or arrays. Once again, the syntax would
be similar to Python with `` let user = {
  "name": "Bob",
  "age": 20
};

output(user["name"])

Future versions of this may add methods for retrieving keys, values and checking if a key
exists.

---

## Standard Library
### - [ ] Completed

As Zap grows, a collection of built in modules must be provided to avoid users repeadedly
implementing commen functionality themselves. These modules would come with the language,
and be importable through the module import system.
Some potential candidates for modules may be:
``let math = require("math");
  let random = require("random");
  let string = require("string");
``

---

## File I/O
### - [ ] Completed

File input/output would allow Zap programs to read from and write to files on disk. This would
expand the actually practical applications of the language to things far beyond simple console
programs.
