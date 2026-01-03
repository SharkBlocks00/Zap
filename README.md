# Zap

A small, dynamically-typed interpreted programming language written in Python. This project is a learning exercise in building a language from scratch.

---

## Table of contents

- [Overview](#overview)
- [Example](#example)
- [Language Syntax](#language-syntax)
  - [Comments](#comments)
  - [Variables](#variables)
  - [Data Types](#data-types)
  - [Operators](#operators)
  - [Control Flow](#control-flow)
  - [Functions](#functions)
  - [Input/Output](#inputoutput)
- [Implementation](#implementation)
- [Future Ideas](#future-ideas)

--- 

## Overview

Zap is a simple, line-based interpreted language. Programs are executed from top to bottom. It is designed to be simple and explicit.

Zap supports:

- Variable declaration and reassignment
- Basic data types: Numbers, Strings, and Booleans
- Arithmetic and comparison operators
- Conditional statements (`if`/`elseif`/`else`)
- Functions (without parameters or return values)
- Console input and output
- Single-line comments

---

## Example

```zap
-- This is a Zap program

let name = request("What is your name? ");
output("Hello, " + name + "!");

let a = 10;
let b = 20;

if (a < b) {
    output("a is less than b");
} elseif (a > b) {
    output("a is greater than b");
} else {
    output("a is equal to b");
}

func say_hello = define() {
    output("Hello from a function!");
}

say_hello();
```

---

## Language Syntax

All statements must end with a semicolon `;`.

### Comments
Single-line comments start with `--`.

```zap
-- This is a comment
output("Hello"); -- This is an inline comment
```

### Variables

Variables are declared using the `let` keyword and can be reassigned using just their name.

```zap
-- Declaration
let x = 10;
let message = "Hello";

-- Reassignment
x = 20;
message = "World";
```

### Data Types

Zap supports the following data types:
- **Number**: e.g., `10`, `3.14` (Note: float literals are not supported yet, but `request()` can produce floats)
- **String**: e.g., `"Hello, World!"`
- **Boolean**: `true`, `false`

### Operators

Zap supports the following operators:

- **Arithmetic**: `+` (addition and string concatenation), `-` (subtraction), `*` (multiplication), `/` (division)
- **Comparison**: `==` (equal to), `!=` (not equal to), `<` (less than), `>` (greater than), `<=` (less than or equal to), `>=` (greater than or equal to)

### Control Flow

Conditional logic is handled using `if`, `elseif`, and `else` statements.

```zap
if (x > 0) {
    output("x is positive");
} elseif (x < 0) {
    output("x is negative");
} else {
    output("x is zero");
}
```

### Functions

Functions can be declared and called. Currently, they do not support parameters or return values.

```zap
func my_function = define() {
    output("This is inside a function!");
}

my_function();
```

### Input/Output

- **Output**: Use `output()` to print to the console.
- **Input**: Use `request()` to get input from the user.

```zap
output("Hello, World!");

let name = request("Enter your name: ");
output("Hello, " + name);
```

---

## Implementation

- **Core**: Zap is written entirely in Python without any external dependencies.
- **Lexer**: The source code is first processed by a lexer that turns the text into a stream of tokens.
- **Parser**: A recursive descent parser builds an Abstract Syntax Tree (AST) from the token stream.
- **Interpreter**: The AST is traversed by an interpreter which executes the code.
- **Scoping**: The language supports a global scope and block-level scopes for functions and control flow statements.

---

## Future Ideas

Check out [roadmap.md](roadmap.md) for more.

- Loops (`while`, `for`)
- Function parameters and `return` statements
- More built-in functions
- Arrays or lists
- Floating point number literals
- More detailed error messages