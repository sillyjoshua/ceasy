# Addons with `.cedev`

A `.cedev` file is a tiny JSON project file. Double-click it after installing the Ceasy Windows file association, or run it with `ceasy.exe my-project.cedev`. Ceasy installs the listed Python packages with `pip`.

Create `my-project.cedev`:

```json
{
  "name": "my-first-project",
  "addons": ["requests", "rich"]
}
```

Double-click the file to install the addons. You need Python 3 and pip installed for package installation. Only install packages you trust: Python packages can execute code on your computer.

Then import packages in a `.ceasy` program using familiar Python syntax:

```ceasy
import random;
from math import sqrt;
let roll = random.randint(1, 6);
print(roll);
print(sqrt(81));
```

The same Python packages are available to the packaged Windows runtime when the matching system Python is installed. This feature is part of the double-click runtime; it is not yet supported by the C transpiler (`ceasy.py`).
