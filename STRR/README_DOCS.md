# STRR Module Documentation

This directory contains the source code for the Star Trek Retro Remake game.

## Documentation Standard

**Every `.py` file in this directory has a corresponding `_doc.md` documentation file.**

### Naming Convention

- **Python file:** `application.py`
- **Documentation file:** `application_doc.md`

The documentation file is located in the **same directory** as its Python file.

### Example

```
STRR/src/game/
├── application.py
├── application_doc.md  ← Comprehensive documentation for application.py
├── model.py
├── model_doc.md        ← Comprehensive documentation for model.py
└── view.py
    └── view_doc.md     ← Comprehensive documentation for view.py
```

### What's in the _doc.md Files?

Each `_doc.md` file contains:

- **Purpose:** What the module does and why it exists
- **Architecture:** Design patterns and architectural role
- **Classes & Functions:** Detailed documentation of all code elements
- **Usage Examples:** Practical code examples
- **Integration Points:** Dependencies and relationships with other modules
- **Configuration:** Any setup or configuration requirements
- **Common Patterns:** Frequently used patterns when working with the module
- **Troubleshooting:** Common issues and solutions

### Benefits

1. **Proximity:** Documentation lives next to the code it describes
2. **Completeness:** Each module has comprehensive documentation
3. **Discoverability:** Easy to find docs for any file
4. **Maintainability:** Docs are updated alongside code changes

## General Documentation

For documentation that spans multiple files or covers broader topics, see the `/docs/` directory at the repository root:

- [DOCUMENTATION_STANDARDS.md](../docs/DOCUMENTATION_STANDARDS.md) - Full documentation policy
- [PYTHON_FILE_REFERENCE.md](../docs/PYTHON_FILE_REFERENCE.md) - Quick reference guide
- [ARCHITECTURE.md](../docs/ARCHITECTURE.md) - System architecture
- [DESIGN.md](../docs/DESIGN.md) - Design philosophy

## Contributing

When adding or modifying a `.py` file:

1. **Create or update** the corresponding `_doc.md` file
2. **Use the template** from `DOCUMENTATION_STANDARDS.md`
3. **Keep it current** - update docs when code changes
4. **Be thorough** - future you (and others) will thank you!

---

For more information, see [DOCUMENTATION_STANDARDS.md](../docs/DOCUMENTATION_STANDARDS.md)
