# Development & Deployment Strategy

This document outlines how this project is structured and how to run it during development and in production.

---

## 🛠️ Development Setup

To simplify working with individual modules during development, we use the `src/` layout pattern and add it to the `PYTHONPATH`.

### ✅ Setup Instructions

Make sure the root project structure looks like this:

```
project-root/
├── src/
│   ├── app.py
│   ├── utils/
│   └── resources/
├── pyproject.toml
```

### 🧪 Running Individual Files

Set the environment variable `PYTHONPATH=src` so you can run files directly with regular imports:

#### On Linux/macOS:

```bash
export PYTHONPATH=src
python src/resources/updater.py
```

#### On Windows (PowerShell):

```powershell
$env:PYTHONPATH = "src"
python src/resources/updater.py
```

This allows you to write clean, absolute imports like:

```python
from utils import paths
```

---

## 🚀 Production Strategy

In production, only the main application file (`app.py`) is executed.

We **do not rely on PYTHONPATH** in production. Instead, we use Python’s `-m` module execution feature:

```bash
python -m pokeback.app
```

This is supported because:

- `src/` is the base of our source tree.
- `pokeback/` is a proper Python package (`__init__.py` exists).
- We always run from the project root.

---

## ✅ Summary

| Environment   | How to Run                        | PYTHONPATH Required? |
|---------------|------------------------------------|------------------------|
| Development   | `python src/<file>.py`             | ✅ Yes (`src/`)         |
| Production    | `python -m pokeback.app`           | ❌ No                   |

---

## 💡 Optional Tip

You can create a simple `start.sh` or `.ps1` to make development easier.

Example `start.sh`:

```bash
#!/bin/bash
export PYTHONPATH=src
python src/app.py
```

---

## 🔒 Final Notes

- Avoid running submodules directly in production.
- Never modify `sys.path` manually inside source files.
- Stick to one entry point (`app.py`) to keep things predictable and portable.

---

*(Document created with the help of ChatGPT)*