# Zap Roadmap

## The following features are features that will potentially roll out to future Zap versions. (Developers to cross off completed features)
### Each feature will have a list of features (if fitting) that will need to be implemented before that feature will be added.

---

## Contents
- [Const modifier](#const-modifier)
- [Request statement](#request-statement)
- [Error if code after ';' on each line](#semi-colon-code-error)
- [More error handling](#better-errors)
- [Comments](#comments)
- [While Loops](#while-loops)
- [For Loops](#for-loops)
- [.zap Files](#filing)

--- 

## Const Modifier
### - [ ] Completed

"const" will be a keyword you can place before/after a let statement, and will change the mutability allowance of that variable.
Suggested way to add: Implement a self.mutable in VarDecleration, and when looking up object in environment in interpreter, check
the mutable value, if True, allow mutability, otherwise throw error.

---

## Request Statement
### - [X] Completed

"request" as a keyword can be put after a ``let <var_name> = request();`` and any information inside the request parenthesis will be 
passed into a python ``input()`` statement, and the value assigned to the declared/reassigned variable. Not too sure on implementation methods currently, however, will figure it out.

--- 

## Semi Colon Code Error
### - [ ] Completed 

Currently, you can put infinite amounts of code on a singular line. This could lead to developers using Zap (for whatever reason) to 
be annoying to themselves and other developers, by coding an entire program on line 1. Instead, this should make it so that if there is any code after a semi colon, it will throw an error, as long as it is not inside a loop and so like a '}' for example. Implementation idea: Simply just check for code after a semi colon token, and check if it is a right curly brace, and if not, error.

--- 

## Better Errors
### - [X] Completed

At the moment, all errors in Zap are not at all descriptive, Ie. ``Exception: Undefined variable x``. This is somewhat descriptive, but 
line numbers & even just slightly more information will make errors much more developer friendly. Also add in custom error classes
for example, Zap_Parser_Error, etc as well as terminal colors. This will be not only more developer friendly, but much easier for when debugging Zap itself. Implementation idea: Check atleast the character, what word etc, and add in custom errors in place of all the ``raise Exception(<exception>)``

--- 

## Comments
### - [X] Completed

Comments are basically an essential feature of any good modern programming language. Inline comments may be relatively easy, as we can 
simple implement a comment ``TokenKind`` and check in the program if there is a Comment TokenKind, and simple ignore all tokens until EOL.
(Also meaning must change how parsing/interpreting is done slightly to allow for EOL support) And for full line comments, can just check comment token and skip until EOL token. Implementation will be relatively easy to do for the actual comments, however changing parsing/interpreting to support EOL may prove to be slightly harder to do.

---  

## While Loops
### - [ ] Completed

While loops are a pretty prominent feature of good programming languages, so therefore zap needs them. Syntax kept relatively simple, ie ``while (<condition>) { <body> }``.
Probably follow similar logic to if statements/functions, however simply checking if the condition is still true on each run of the loop. This will also involve adding in 
some new keywords, such as ``break``, ``continue`` and possibly even ``return``, although that might be added when functions recieve paramater support.

---

## For Loops
### - [ ] Completed

As with while loops, for loops are also a necessary feature of good programming languages. For loops will also probably follow if statement/function/while loop (if implemented)
structure, except incrementing for each something. Possible syntax could be something like ``for (char : string) { <body> }`` Implementation of for loops will 
also probably mean that each ``TokenKind`` has different behaviour when iterated over. For example, ``BOOLEAN`` ``TokenKind`` will be uniterable but say the ``STRING`` will 
iterate over each character in the string.

---

## Filing
### - [ ] Completed

The filing update would mean that you can create & run .zap files instead of having to type out zap code in the lexer file. We can instead perhaps implement a zap_main.py file, 
which you can run standalone for an interactive REPL or provide a .zap file's path, which will then get ran. This is the last feature aimed to be added before a beta release of
sorts is packaged and downloadable. Implementation will be pretty simple, but the REPL may prove to be slightly trickier.