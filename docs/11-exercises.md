# Practice exercises

Try these in order. Use `python3 ceasy.py your-file.ceasy --check` for the currently supported subset, then compile the generated C.

## Beginner

1. Print your name and a greeting.
2. Declare an integer called `favourite_number` and print it.
3. Declare a decimal value and print it.
4. Calculate `8 * 7` and print the answer.
5. Change the examples and observe the generated C.

## Think about it

6. Why does `let score = 10;` generate an `int`?
7. What is the difference between `=` and `==` in C?
8. Why does Ceasy need a C compiler after translating the source?
9. What can go wrong if a language translator only processes one line at a time?
10. Design a syntax for a function declaration. Write down how it should translate to C before implementing it.

## Challenge project

Plan a tiny quiz program. Write the desired Ceasy code, identify which features are already supported and list what the compiler would need before the whole program could run. Input, robust branching and nested blocks are not fully supported in this prototype, so this is a design exercise rather than a promise that the full quiz compiles today.