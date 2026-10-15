# FAQ and roadmap

## Is Ceasy a complete language?

No. It is an early prototype intended to establish the syntax, compiler direction and learning materials. Use the reference to see what works.

## Is Ceasy just C?

It is C-inspired. Its `let` declarations and `print` helper are translated into C. The current feature set is intentionally small.

## Do I need a C compiler?

Yes, if you want to compile and run the generated C. Python runs the translator; GCC or Clang compiles its output.

## Does it support Windows?

The translator is Python-based and should run anywhere Python is available. To build executables, install and configure a C compiler too.

## Roadmap

- [x] Initial command-line transpiler
- [x] Basic inferred declarations and output
- [x] Markdown learning guide and examples
- [x] Starter unit tests
- [ ] Tokenizer and parser instead of line-based matching
- [ ] Reliable nested blocks, conditions and loops
- [ ] Input helpers
- [ ] Custom functions and scope rules
- [ ] Stronger type checking and diagnostics
- [ ] CI testing on Linux, macOS and Windows

## How can I help?

Open an issue with a minimal reproducible example, or submit a pull request with tests and documentation. See [CONTRIBUTING.md](../CONTRIBUTING.md).