# Zap

A small, dynamically-typed interpreted programming language written in Python. I have taken on this 
project because I had lots of time, and I wanted something cool & useful to do.

---

## Table of contents

- [Overview](#overview)
- [How to Run](#how-to-run)
- [Example](#example)
- [Language Syntax](#language-syntax)
  - [Comments](#comments)
  - [Variables](#variables)
  - [Data Types](#data-types)
  - [Operators](#operators)
  - [Control Flow](#control-flow)
  - [Functions](#functions)
  - [Loops](#loops)
  - [Break Statement](#break-statement)
  - [Input/Output](#inputoutput)
- [Implementation](#implementation)
- [Future Ideas](#future-ideas)

---

## Overview

Zap is a simple, line-based interpreted language. Programs are executed from top to bottom. It is designed to be simple and explicit.
In Zap source files, formatting may appear as "unique" but that is due to the Zed editor auto formatting code like this.

Zap supports:

- Variable declaration and reassignment
- Basic data types: Numbers, Strings, and Booleans
- Arithmetic and comparison operators
- Conditional statements (`if`/`elseif`/`else`)
- Loops (`while` and `foreach`)
- Functions with call support
- Console input and output
- Single-line comments
- Block-level scoping
- `break` statement to exit loops early

---

## How to Run  

At the moment, as Zap is in its early stages, you can only run zap code by putting it into the `source: str = """ <your code here> """`
and running the interpreter.  This is most definately suboptimal, and will 100% be changed/updated in future releases. 

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

Functions can be declared using `func name = define() { body }` and called with `name();`. Currently, they do not support parameters or return values.

```zap
func my_function = define() {
    output("This is inside a function!");
}

my_function();
```

### Loops

Zap supports two types of loops:

**While Loop**: Repeats while a condition is true.

```zap
let count = 0;
while (count < 5) {
    output("Count: " + count);
    count = count + 1;
}
```

**Foreach Loop**: Iterates over each element in a collection (e.g., characters in a string).

```zap
let str = "Hello";
foreach (char : str) {
    output(char);
}
```

### Break Statement

The `break` statement exits a loop early.

```zap
let count = 0;
while (count < 10) {
    if (count == 5) {
        break;
    }
    output(count);
    count = count + 1;
}
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

- Function parameters and `return` statements
- More built-in functions
- Arrays or lists
- Floating point number literals
