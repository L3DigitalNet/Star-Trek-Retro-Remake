# Documentation Standards

**Version:** 0.0.3
**Last Updated:** 10-30-2025
**Status:** Active Policy

---

## Overview

This document defines the documentation standards for the Star Trek Retro Remake project, establishing clear rules for where documentation should be located and what it should contain.

## CRITICAL: Linux Environment Only

- **MANDATORY**: All documentation must reflect **Linux-only compatibility**
- **NO Windows references** - document Linux paths, commands, system requirements only
- **Python 3.14+ REQUIRED**: Document latest language features and requirements
- Use forward slashes for paths, Linux-specific commands, and Linux environment assumptions

---

## General Documentation Guidelines

### File Header Format Compliance

**All Python files must have proper headers following repository standards:**

- Include shebang: `#!/usr/bin/env python3`
- Include encoding: `# -*- coding: utf-8 -*-`
- Complete docstring format with:
  - Description (what the module does and why)
  - Author (full name or team name)
  - Email (contact email)
  - GitHub (repository URL)
  - Date Created (MM-DD-YYYY)
  - Date Changed (MM-DD-YYYY - update when modified)
  - License (license type)
  - Features (key features as bullet list)
  - Requirements (dependencies and environment)
  - Known Issues (current limitations)
  - Planned Features (future enhancements)
  - Classes (brief class descriptions)
  - Functions (brief function descriptions)
- Header content must reflect current code implementation
- Update "Date Changed" to current date when modified

### Docstring Format Compliance

- All docstrings follow the repository's specified format (see copilot-instructions.md)
- **Do not specify types in docstrings** - rely on type hints instead
- Docstring content must reflect current code state
- Use consistent formatting throughout the project

### Inline Documentation Standards

- Inline comments for each significant code block for readability and AI autocompletion context
- Comments at the top of code blocks, briefly explaining purpose (preferably one line)
- Add/update inline comments for:
  - Complex logic
  - Linux-specific implementations
  - Important design decisions
  - Non-obvious behavior

### Minimal .md File Creation Policy

- **IMPORTANT**: Only create/update README.md, PROJECT-DOC.md, CHANGELOG.md as needed
- Exception: auto-generated API docs in library folders (common_lib/docs/)
- Per-file `_doc.md` files required for all `.py` files in `STRR/` directory
- Avoid creating unnecessary documentation files

## Documentation Structure

### Per-File Documentation Rule

**For every `.py` file in the `STRR/` directory, create a matching `.md` documentation file.**

#### Naming Convention

```
Python File:        application.py
Documentation File: application_doc.md
```

The documentation file name is identical to the Python file name with `_doc` appended before the `.md` suffix.

#### Location

The `_doc.md` file must be stored in the **same directory** as its corresponding `.py` file.

**Example:**

```
STRR/src/game/application.py
STRR/src/game/application_doc.md  ← Documentation file here
```

#### Purpose

Each `_doc.md` file contains **all documentation needed to understand and work with that specific Python file**, including:

- File purpose and responsibilities
- Architecture and design patterns used
- Class and function documentation
- Usage examples
- Integration points with other modules
- Configuration requirements
- Common use cases and patterns
- Troubleshooting guidance

### General Documentation

Documentation with **broader scope** than a single file belongs in the **`/docs/` directory** at the repository root.

**Examples of general documentation:**

- `ARCHITECTURE.md` - System-wide architecture
- `DESIGN.md` - Overall design philosophy
- `PYTHON_FILE_REFERENCE.md` - Cross-file reference guide
- `VERSIONING_GUIDELINES.md` - Project versioning policy
- This file (`DOCUMENTATION_STANDARDS.md`)

---

## Per-File Documentation Template

Each `_doc.md` file should follow this structure:

```markdown
# [Module Name] Documentation

**File:** `path/to/file.py`
**Version:** [version]
**Last Updated:** [date]

---

## Purpose

Brief description of what this file does and why it exists.

---

## Architecture

Design patterns, architectural role, and how this fits in the system.

---

## Classes

### ClassName

**Purpose:** What this class does

**Attributes:**
- `attribute_name` (type): Description

**Public Methods:**
- `method_name(args)`: What it does and returns

**Private Methods:**
- `_method_name(args)`: Internal implementation details

---

## Functions

### function_name(args)

**Purpose:** What this function does

**Parameters:**
- `param` (type): Description

**Returns:**
- type: Description

---

## Usage Examples

### Example 1: Common Use Case

```python
# Code example showing typical usage
```

### Example 2: Advanced Pattern

```python
# Code example showing advanced usage
```

---

## Integration Points

### Dependencies

- What this module depends on
- Why each dependency is needed

### Used By

- What other modules use this one
- How they integrate

---

## Configuration

Any configuration requirements, settings, or environment setup needed.

---

## Common Patterns

Frequently used patterns when working with this module.

---

## Troubleshooting

### Issue: [Problem Description]

**Solution:** How to resolve

---

## Notes

Additional information, caveats, or future considerations.

---

## Change History

- **[Date]** - [Change description]

```

---

## Documentation Maintenance

### When to Update Documentation

Update the `_doc.md` file whenever:

1. **New classes or functions** are added to the `.py` file
2. **Significant changes** are made to existing code
3. **Usage patterns** change
4. **Integration points** are added or modified
5. **Bugs are fixed** that warrant documentation

### Version Synchronization

The version in `_doc.md` should match the version in the corresponding `.py` file header.

### Date Updates

Update the "Last Updated" field whenever the documentation is modified.

---

## Enforcement

### New Files

When creating a new `.py` file in `STRR/`:
1. Create the corresponding `_doc.md` file immediately
2. Use the template provided above
3. Fill in at minimum: Purpose, Architecture, and Classes/Functions sections

### Existing Files

Gradually add `_doc.md` files for existing `.py` files:
1. Prioritize core/frequently modified files
2. Add documentation as files are worked on
3. Use git commits to track documentation additions

### Code Reviews

Pull requests should include:
- Updated or new `_doc.md` files for modified `.py` files
- General documentation updates in `/docs/` if architectural changes were made

---

## Examples

### Example 1: Core Module Documentation

**File Structure:**
```

STRR/src/game/
├── application.py
├── application_doc.md  ← Per-file documentation
├── model.py
├── model_doc.md        ← Per-file documentation
└── view.py
    └── view_doc.md     ← Per-file documentation

```

### Example 2: General Documentation

**File Structure:**
```

docs/
├── ARCHITECTURE.md       ← General/system-wide
├── DESIGN.md            ← General/system-wide
├── DOCUMENTATION_STANDARDS.md  ← This file
└── PYTHON_FILE_REFERENCE.md   ← Cross-cutting reference

```

---

## Benefits

This documentation structure provides:

1. **Proximity:** Documentation lives next to the code it describes
2. **Discoverability:** Easy to find docs for any given file
3. **Modularity:** Each file's documentation is self-contained
4. **Maintainability:** Changes to code are reflected in adjacent docs
5. **Clarity:** Clear separation between file-specific and general documentation

---

## Tools and Automation

### Future Enhancements

Consider implementing:

1. **Documentation Linter:** Check that every `.py` has a matching `_doc.md`
2. **Template Generator:** Script to create `_doc.md` from `.py` structure
3. **Documentation Coverage Report:** Show which files lack documentation
4. **Automated TOC Generation:** Generate table of contents for documentation

### Pre-commit Hooks

Consider adding a pre-commit hook that:
- Warns if a `.py` file is modified but its `_doc.md` is not
- Checks that new `.py` files have corresponding `_doc.md` files

---

## Questions and Clarifications

**Q: What about `__init__.py` files?**
A: Create `__init___doc.md` only if the `__init__.py` contains significant logic or exports. Empty or simple `__init__.py` files don't need documentation.

**Q: What about test files?**
A: Test files (`test_*.py`) generally don't need `_doc.md` files unless they contain complex test utilities or fixtures that need explanation.

**Q: What if a file is temporary or experimental?**
A: Mark the `_doc.md` as "Experimental" or "Draft" in the header. Still create it for consistency.

**Q: Can I use other formats (RST, AsciiDoc)?**
A: Stick with Markdown (`.md`) for consistency. All project documentation uses Markdown.

---

## Related Documents

- [PYTHON_FILE_REFERENCE.md](PYTHON_FILE_REFERENCE.md) - Guide to Python file purposes
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture overview
- [DESIGN.md](DESIGN.md) - Design philosophy and patterns

---

## Revision History

- **0.0.3** (10-30-2025) - Added comprehensive documentation guidelines:
  - Linux-only environment requirements
  - File header format compliance standards
  - Docstring format compliance (no types in docstrings)
  - Inline documentation standards
  - Minimal .md file creation policy
- **0.0.2** (10-30-2025) - Initial documentation standards established
