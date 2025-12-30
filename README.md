# Zap Language

A small interpreted programming language written in Python.

Zap is a person learning project i am working on simply because i have lots of time.
It is designed to be simple, explicit, stupidly verbose rather than fast / feature complete.

---

## Table of contents

- [Overview](#overview)
- [Example](#example)
- [Language Syntax](#language-syntax)
  - [Comments](#comments)
  - [Variables](#variables)
  - [Reassigment](#reassignment)
  - [Output](#output)
  - [User Input](#user-input)
- [Types](#types)
- [Semantics](#semantics)
- [Error Handling](#error-handling)
- [Implementation](#implementation)
- [Future Ideas](#future-ideas)

--- 

## Overview

Zap is a line based interpreted language with not a lot of syntax. </br>
Programs execute top to bottom, and all variables are stored in a global table.

Zap supports:

- Variable declaration and reassignment
- Runtime type inference
- Console output
- user input
- Comments
- Basic syntax validation stuff

---

## Example

````zap
let hi = 3;
output(hi);

let name = "bob";
output(name);

let person = name;
output(person);

res name = "bill";
res hi = name;

output(name);
output(person);
output(hi);

let test = request("How are you? ");
output(test);

res name = request("What is your name? ");
output(name);
````
---

## Language Syntax

### Comments
Comments begin with a ``--``.
````zap
-- This is a comment
output("Hello"); -- Inline comment
````
Fully commented lines are ignored by the interpreter.

### Variables
Variables are declared using the ``let`` keyword.
```zap
let x = 3;
let name = "bob";
```
Rules:
- Variables myust be declared before use
- Redeclaring an existing variable error
- Every statement must end with a semicolon

### Reassignment
Variables can be reassigned using the ``res`` keyword.
```zap
res x = 10;
res name = "bill";
```
Rules:
- The variable must already exist
- Reassignment replaces the variable's value

### Output
Use ``output()`` to print to the console.
````zap
output("hello");
output(x);
````
Accepted values:
- String literals
- Variables

Concatenated strings are not <i>yet</i> supported.

### User input
User ``request()`` to prompt the user for input.
````zig 
let answer = request("How are you? ");
output(answer);
````
Notes:
- ``request()`` returns user input
- Input is stored like any other variable

--- 

## Types
Zap is dynamically typed, <i>for now</i>, and performs runtime type inference.

Supported types:
- int
- float
- str

Types  are inferred on assignment.
Variables may change type when reassigned.

---

## Semantics
- Zap uses value semantics
- Assigning one variable to another copies the value
- Identifiers resolve to values, not references
- There is one single global scope

Example:
```zap
let a = "bob";
let b = a;
res = "bill";

output(b); -- will still print "bob"
```

--- 

## Error handling
Zap has some error handling, and reports syntax errors such as:
- Missing semicolons
- Invalid reassignment
- Undefined variables
- Malformed ``output()`` or ``request()`` calls
- Unequal or invalid parentheses

Most errors will include column and line numbers, but some may not.

---

## Implementation
- Zap is written entirely in Python
- No external parsing/ lexer libraries
- Manual parsing and interpretation
- Only really uses loads of string & list indexing methods
- Not a tokenized language

---

## Future ideas
Here are some ideas that potentially will be added:
- Arithmetic expressions
- Conditionals
- Loops
- Functions
- Lexer / tokenizer
