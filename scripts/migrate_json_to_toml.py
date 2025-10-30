#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Star Trek Retro Remake - JSON to TOML Migration Utility

Description:
    Utility script to migrate JSON configuration files to TOML format.
    Provides batch conversion and validation of configuration files.

Author: Star Trek Retro Remake Development Team
Date Created: 10-29-2025
Date Changed: 10-29-2025
License: Open Source

Usage:
    python migrate_json_to_toml.py --config-dir star_trek_retro_remake/config/
    python migrate_json_to_toml.py --file game_settings.json --output game_settings.toml
"""

import argparse
import json
import sys
import tomllib
from pathlib import Path
from typing import Any, Dict

try:
    import tomli_w
except ImportError:
    print("Error: tomli_w is required for TOML writing")
    print("Install with: pip install tomli_w")
    sys.exit(1)


def convert_json_to_toml(json_data: Dict[str, Any], add_comments: bool = True) -> str:
    """
    Convert JSON data to TOML format with optional comments.

    Args:
        json_data: Dictionary from JSON file
        add_comments: Whether to add descriptive comments

    Returns:
        TOML formatted string
    """
    # Convert to TOML bytes
    toml_bytes = tomli_w.dumps(json_data)

    if not add_comments:
        return toml_bytes

    # Add comments based on common configuration patterns
    lines = toml_bytes.split('\n')
    commented_lines = []

    for line in lines:
        # Add comments for common configuration keys
        if 'window_width' in line:
            line += '     # Default window width in pixels'
        elif 'window_height' in line:
            line += '    # Default window height in pixels'
        elif 'fullscreen' in line and 'false' in line:
            line += '      # Start in windowed mode'
        elif 'vsync' in line and 'true' in line:
            line += '           # Enable vertical sync to prevent screen tearing'
        elif 'fps_limit' in line:
            line += '         # Target framerate (0 = unlimited)'
        elif 'master_volume' in line:
            line += '            # Master audio volume (0.0 - 1.0)'
        elif 'music_volume' in line:
            line += '             # Background music volume'
        elif 'sfx_volume' in line:
            line += '               # Sound effects volume'
        elif 'ui_volume' in line:
            line += '                # UI interaction sounds volume'
        elif 'difficulty' in line:
            line += '           # Game difficulty: easy, normal, hard, expert'
        elif 'auto_save' in line and 'true' in line:
            line += '               # Automatically save game progress'
        elif 'auto_save_interval' in line:
            line += '       # Auto-save interval in seconds'
        elif 'turn_timer' in line:
            line += '                # Turn time limit in seconds (0 = unlimited)'

        commented_lines.append(line)

    return '\n'.join(commented_lines)


def migrate_file(input_path: Path, output_path: Path, add_comments: bool = True) -> bool:
    """
    Migrate single JSON file to TOML.

    Args:
        input_path: Source JSON file
        output_path: Target TOML file
        add_comments: Whether to add descriptive comments

    Returns:
        True if migration successful
    """
    try:
        # Load JSON file
        with open(input_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        # Convert to TOML
        toml_content = convert_json_to_toml(json_data, add_comments)

        # Add file header
        header = f"""# Star Trek Retro Remake - {output_path.stem.replace('_', ' ').title()} Configuration
#
# Migrated from JSON to TOML format for improved readability and maintainability.
# This file contains configuration settings with comments explaining each option.
#
# Author: Star Trek Retro Remake Development Team
# Date Created: 10-29-2025
# License: Open Source

"""

        # Write TOML file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(header + toml_content)

        print(f"✓ Migrated {input_path.name} → {output_path.name}")
        return True

    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON in {input_path.name}: {e}")
        return False
    except Exception as e:
        print(f"✗ Failed to migrate {input_path.name}: {e}")
        return False


def validate_toml_file(toml_path: Path) -> bool:
    """
    Validate TOML file by attempting to load it.

    Args:
        toml_path: Path to TOML file

    Returns:
        True if valid TOML
    """
    try:
        with open(toml_path, 'rb') as f:
            tomllib.load(f)
        print(f"✓ Valid TOML: {toml_path.name}")
        return True
    except tomllib.TOMLDecodeError as e:
        print(f"✗ Invalid TOML in {toml_path.name}: {e}")
        return False
    except Exception as e:
        print(f"✗ Failed to validate {toml_path.name}: {e}")
        return False


def migrate_directory(config_dir: Path, backup: bool = True,
                     add_comments: bool = True) -> int:
    """
    Migrate all JSON files in directory to TOML.

    Args:
        config_dir: Directory containing JSON files
        backup: Whether to backup original JSON files
        add_comments: Whether to add descriptive comments

    Returns:
        Number of files successfully migrated
    """
    if not config_dir.exists():
        print(f"✗ Directory not found: {config_dir}")
        return 0

    json_files = list(config_dir.glob("*.json"))
    if not json_files:
        print(f"No JSON files found in {config_dir}")
        return 0

    # Create backup directory if requested
    if backup:
        backup_dir = config_dir / "json_backup"
        backup_dir.mkdir(exist_ok=True)
        print(f"Backing up JSON files to {backup_dir}")

    migrated_count = 0

    for json_file in json_files:
        toml_file = config_dir / f"{json_file.stem}.toml"

        # Skip if TOML already exists
        if toml_file.exists():
            print(f"⚠ TOML file already exists: {toml_file.name}")
            continue

        # Migrate file
        if migrate_file(json_file, toml_file, add_comments):
            migrated_count += 1

            # Backup original if requested
            if backup:
                backup_path = backup_dir / json_file.name
                json_file.rename(backup_path)
                print(f"  Backed up to {backup_path}")

            # Validate resulting TOML
            validate_toml_file(toml_file)

    return migrated_count


def main():
    """Main script entry point."""
    parser = argparse.ArgumentParser(
        description="Migrate JSON configuration files to TOML format"
    )
    parser.add_argument(
        "--config-dir",
        type=Path,
        help="Directory containing JSON configuration files"
    )
    parser.add_argument(
        "--file",
        type=Path,
        help="Single JSON file to migrate"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output TOML file (used with --file)"
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Don't backup original JSON files"
    )
    parser.add_argument(
        "--no-comments",
        action="store_true",
        help="Don't add descriptive comments"
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate existing TOML files"
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.config_dir and not args.file:
        parser.print_help()
        return 1

    if args.file and not args.output:
        args.output = args.file.with_suffix('.toml')

    # Validate only mode
    if args.validate_only:
        if args.config_dir:
            toml_files = list(args.config_dir.glob("*.toml"))
            valid_count = sum(validate_toml_file(f) for f in toml_files)
            print(f"\nValidated {valid_count}/{len(toml_files)} TOML files")
        elif args.output and args.output.exists():
            validate_toml_file(args.output)
        return 0

    # Single file migration
    if args.file:
        if not args.file.exists():
            print(f"✗ File not found: {args.file}")
            return 1

        success = migrate_file(args.file, args.output, not args.no_comments)
        if success:
            validate_toml_file(args.output)
        return 0 if success else 1

    # Directory migration
    if args.config_dir:
        migrated = migrate_directory(
            args.config_dir,
            backup=not args.no_backup,
            add_comments=not args.no_comments
        )
        print(f"\nMigrated {migrated} configuration files to TOML format")
        return 0 if migrated > 0 else 1


if __name__ == "__main__":
    sys.exit(main())