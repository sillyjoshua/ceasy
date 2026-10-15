# Start here

Welcome to Ceasy! Ceasy is an experimental language project inspired by C, designed to make the first steps feel less intimidating. It keeps familiar semicolons and braces while adding readable helpers like `print(...)` and inferred `let` declarations.

## The learning route

1. Install Python and a C compiler using [Installation](01-installation.md).
2. Run your first program in [Your first program](02-first-program.md).
3. Learn values and variables in [Variables and types](03-variables-and-types.md).
4. Work through input/output, conditions and loops.
5. Use the [exercises](11-exercises.md) to practise.

## Your first code

```ceasy
print("Hi there!");
let age = 12;
print(age);
```

The Ceasy translator turns this into C source code. A C compiler then turns that C source into an executable. Ceasy is a prototype, so only syntax described in the language reference is supported.