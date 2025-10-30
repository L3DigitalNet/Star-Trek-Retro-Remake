# Versioning Guidelines & Implementation

## Overview

This document outlines the simplified versioning approach for the Python repository. The new system uses a clean MAJOR.MINOR.PATCH format without development stage extensions and integrates with the `/version-update` prompt command for automated version management.

## Version Format

### Semantic Versioning Standard

- **Format:** `MAJOR.MINOR.PATCH` (e.g., `1.2.3`)
- **NO** development stage extensions (`.dev`, `.a`, `.b`, `.rc`)
- **New projects** start at version `0.0.1`
- **Version 1.0.0** indicates first full release

### Version Significance

- **MAJOR:** Breaking changes or major feature milestones
- **MINOR:** New functionality in backward-compatible manner
- **PATCH:** Bug fixes and small improvements
- **NOTE:** MINOR and PATCH meanings determined by developer discretion

## Command Usage

### Version Update Commands

Triggered via `/version-update` prompt commands:

#### Specific Version Update

```bash
/version-update [filename] [version]
```

Examples:

- `/version-update DFBU 1.2.3`
- `/version-update cust_class.py 0.5.1`

#### Increment Version

```bash
/version-update [filename] increment
```

Examples:

- `/version-update DFBU increment` (increases by 0.0.1)
- `/version-update cust_class.py increment` (increases by 0.0.1)

**Note:** If no filename is specified, updates the currently open file in the editor.

## Automated Process

When a version update is triggered, the following occurs automatically:

1. **Version Update:** Updates `__version__` variable in the specified Python file
2. **Code Analysis:** Compares current implementation with previous version
3. **Changelog Generation:** Creates comprehensive changelog entry
4. **File Updates:** Updates CHANGELOG.md in project's `/docs/` folder
5. **Header Updates:** Updates "Date Changed" in file header to current date

## Implementation Files

### Core Components

#### Version Update Prompt

- **File:** `.github/prompts/version-update.prompt.md`
- **Purpose:** Handles `/version-update` commands and automated changelog generation
- **Features:** Command parsing, version validation, automatic change detection

#### Version Utility

- **File:** `projects/common_lib/version.py`
- **Purpose:** Simplified MAJOR.MINOR.PATCH version management
- **Classes:** `SemanticVersion` with parsing, comparison, and incrementing
- **Functions:** `increment_version_string()`, `is_valid_version()`

#### Updated Templates

- **Location:** `templates/my_project_folder_template/`
- **Changes:** All template files now start with `__version__ = "0.0.1"`
- **Files Updated:** `main.py`, `cli_main.py`, `desktop_main.py`, `game_main.py`, `library_main.py`, `src/__init__.py`

### Updated Projects

All existing projects have been updated to remove development stage extensions:

- **DFBU:** `0.2.1.dev1` → `0.2.1`
- **PIFS:** `0.0.2.dev2` → `0.0.2`
- **HTML to Text GUI:** `0.1.0.dev1` → `0.1.0`
- **ExportScripts:** `0.1.0.dev1` → `0.1.0`
- **HTML to TXT:** `0.1.0.dev1` → `0.1.0`
- **common_lib:** `0.2.0.dev1` → `0.2.0`

## Instructions Integration

### Updated Guidelines

- **Main Instructions:** Updated `.github/copilot-instructions.md` to reflect new versioning rules
- **Project Types:** All instruction files maintain consistency with MAJOR.MINOR.PATCH format
- **Error Handling:** Continues to defer comprehensive error handling until version 1.0.0

### Removed Files

The following superseded files have been removed:

- `version_updater.py` (replaced by prompt-based approach)
- `SEMANTIC_VERSIONING_IMPLEMENTATION.md` (implementation complete)
- `CHANGELOG_COMPARISON_PROMPT.md` (functionality integrated into version-update prompt)

## Benefits

### Simplified Workflow

- **Clean Versioning:** No confusing development stage extensions
- **Command Integration:** Direct integration with VS Code prompt system
- **Automated Documentation:** Automatic changelog generation based on code analysis
- **Consistent Format:** All projects follow identical versioning standards

### Developer Experience

- **Easy Commands:** Simple `/version-update` syntax for all version management
- **Intelligent Analysis:** Automatic detection of code changes for changelog
- **File Targeting:** Can specify files or use currently open file
- **Flexible Incrementing:** Support for both specific versions and automatic incrementing

### Maintenance Benefits

- **Reduced Complexity:** Elimination of development stage tracking
- **Better Integration:** Direct integration with existing prompt system
- **Automated Changelog:** Reduces manual documentation burden
- **Consistent Standards:** Repository-wide version format standardization

## Future Considerations

### Version 1.0.0 Transition

When projects reach version 1.0.0:

- Implement comprehensive error handling (deferred until 1.0.0)
- Establish backward compatibility commitments
- Complete comprehensive testing and documentation
- Solidify API contracts and interfaces

### Enhanced Features (Future)

- Git tag synchronization with version updates
- Release preparation automation
- Version compatibility checking between projects
- Integration with CI/CD pipelines for automated releases

This new versioning approach provides a streamlined, automated solution for version management that integrates seamlessly with the existing development workflow while maintaining consistency across all repository projects.
