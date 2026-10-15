# Contributing to Ceasy

Thanks for helping improve Ceasy!

## Before changing syntax

1. Open an issue or describe the proposed syntax in your pull request.
2. Include a short `.ceasy` example and the C output you expect.
3. Update the language reference and relevant tutorial pages.
4. Add tests for successful translation and error cases.
5. Keep claims in the README aligned with features that actually work.

## Development

Ceasy currently requires Python 3.10+ and uses only the Python standard library.

```bash
python3 -m unittest discover -s tests -v
python3 ceasy.py examples/hello.ceasy --check
```

## Style

- Prefer readable code over clever regex tricks.
- Keep compiler errors actionable and include the source line where possible.
- Do not add dependencies without explaining why they are needed.
- Never commit credentials, personal data or generated binaries.

By submitting a contribution, you agree that it may be distributed under the repository's MIT license.