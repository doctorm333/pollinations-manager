# Contributing to Pollinations Manager

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the issue, not the person

## How to Contribute

### Reporting Bugs

1. Check if the bug is already reported in [Issues](../../issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Your environment (OS, Python version)

### Suggesting Features

1. Check existing [Issues](../../issues) for similar suggestions
2. Create a new issue with:
   - Clear description of the feature
   - Why it would be useful
   - Possible implementation ideas

### Adding Translations

We welcome new language translations!

1. Fork the repository
2. Open `main.py`
3. Find the `TRANSLATIONS` dictionary
4. Add your language following the existing format:
   ```python
   "xx": {  # ISO 639-1 language code
       "app_title": "...",
       "version": "v2.0",
       # ... copy all keys from "en" and translate values
   }
   ```
5. Add styles to `STYLES_TRANSLATIONS`:
   ```python
   "xx": ["No style", "Cinematic", ...],  # Translate each style
   ```
6. Add to `LANGUAGE_NAMES`:
   ```python
   "xx": "Native Name",
   ```
7. Add restart message in `change_language()` function
8. Submit a pull request

### Submitting Code Changes

1. **Fork** the repository
2. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test** your changes thoroughly
5. **Commit** with a clear message:
   ```bash
   git commit -m "Add: description of what you added"
   ```
6. **Push** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request**

## Commit Message Guidelines

Use clear, descriptive commit messages:

- `Add: new feature description`
- `Fix: bug description`
- `Update: what was updated`
- `Remove: what was removed`
- `Refactor: what was refactored`
- `Docs: documentation changes`

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and small

## Pull Request Process

1. Update README.md if needed
2. Ensure all existing features still work
3. Describe your changes in the PR description
4. Link any related issues
5. Wait for review

## Development Setup

```bash
# Clone your fork
git clone https://github.com/doctorm333/pollinations-manager.git
cd pollinations-manager

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

## Questions?

- Open an issue for questions
- Join our [Telegram](https://t.me/+SSC4B1Dnrlc2ZTky) for discussions

---

Thank you for contributing!
