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

--- 

## Const Modifier
### [] Completed

"const" will be a keyword you can place before/after a let statement, and will change the mutability allowance of that variable.
Suggested way to add: Implement a self.mutable in VarDecleration, and when looking up object in environment in interpreter, check
the mutable value, if True, allow mutability, otherwise throw error.

---

## Request Statement
### [] Completed

"request" as a keyword can be put after a ``let <var_name> = request();`` and any information inside the request parenthesis will be 
passed into a python ``input()`` statement, and the value assigned to the declared/reassigned variable. Not too sure on implementation methods currently, however, will figure it out.

--- 

## Semi Colon Code Error
### [] Completed 

Currently, you can put infinite amounts of code on a singular line. This could lead to developers using Zap (for whatever reason) to 
be annoying to themselves and other developers, by coding an entire program on line 1. Instead, this should make it so that if there is any code after a semi colon, it will throw an error, as long as it is not inside a loop and so like a '}' for example. Implementation idea: Simply just check for code after a semi colon token, and check if it is a right curly brace, and if not, error.

--- 

## Better Errors
### [] Completed

At the moment, all errors in Zap are not at all descriptive, Ie. ``Exception: Undefined variable x``. This is somewhat descriptive, but 
line numbers & even just slightly more information will make errors much more developer friendly. Also add in custom error classes
for example, Zap_Parser_Error, etc as well as terminal colors. This will be not only more developer friendly, but much easier for when debugging Zap itself. Implementation idea: Check atleast the character, what word etc, and add in custom errors in place of all the ``raise Exception(<exception>)``

--- 

## Comments
### [] Completed

Comments are basically an essential feature of any good modern programming language. Inline comments may be relatively easy, as we can 
simple implement a comment ``TokenKind`` and check in the program if there is a Comment TokenKind, and simple ignore all tokens until EOL.
(Also meaning must change how parsing/interpreting is done slightly to allow for EOL support) And for full line comments, can just check comment token and skip until EOL token. Implementation will be relatively easy to do for the actual comments, however changing parsing/interpreting to support EOL may prove to be slightly harder to do.