# Secret values with `.cesecret`

Ceasy looks for a file with the same base name as the program. For `app.ceasy`, create `app.cesecret` beside it:

```json
{
  "API_KEY": "replace-this-with-your-own-key",
  "SERVICE_URL": "https://example.com"
}
```

Use values in your program with `secret("API_KEY")`:

```ceasy
let api_key = secret("API_KEY");
print(api_key); # prints [secret], not the value
```

Ceasy redacts direct secret values when they are printed, including when a secret is included in a string printed with Ceasy's `print(...)`. This is a guard against accidental console output, not a complete security boundary: code can transform or send a value elsewhere. **`.cesecret` files are plain JSON and are not encrypted.** The file owner and any program with permission to read it can read the values. Use file permissions, environment-level secret storage, and your service's own access controls for real credentials. Never commit a real `.cesecret` file to GitHub.

You can ask an AI assistant to draft a `.cesecret` template, but provide placeholders rather than sending it real credentials. Ceasy does not require an AI service to create or run secret files.
