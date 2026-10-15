# Functions and C interoperability

Ceasy is designed around C rather than trying to hide every detail of it. The current prototype always generates a C `main` function and does not yet support declaring custom Ceasy functions.

## Why C output?

The translation process is:

1. Write a `.ceasy` source file.
2. Run `ceasy.py` to generate `.c` source.
3. Compile the C source with GCC or Clang.
4. Run the resulting executable.

This means the output can be inspected and compiled with standard C tools. At present, the translator supports only the syntax described in the language reference; it is not a general-purpose C preprocessor or full C parser.

## Future direction

Planned features include Ceasy function declarations, explicit type annotations, improved scopes, standard-library wrappers and better error messages. See [FAQ and roadmap](12-faq-roadmap.md) for current priorities.