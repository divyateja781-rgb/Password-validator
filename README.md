# Password Validator

A Python Tkinter desktop application that gives live feedback while a user creates a stronger password.

## Validation rules

- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

## Features

- Masked password field with show/hide control
- Live requirement indicators
- Weak, Medium, and Strong status
- Submit and clear actions
- Success and warning dialogs
- Validation engine separated from the GUI and covered by tests

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python app.py
```

Tkinter is included with standard Windows and macOS Python installations. On some Linux distributions, install the system package `python3-tk`.

## Run tests

```bash
pip install -r requirements-dev.txt
pytest -q
```

## Project structure

```text
app.py                    Tkinter user interface
password_service.py       Reusable validation logic
tests/                    Automated tests
```

## Interview explanation

The interface reads the password through a Tkinter `StringVar`. Every change calls the validation service, which returns one result for each rule. The GUI updates the symbols, progress bar and strength label. Keeping validation outside the interface makes the rules easy to test and extend.

