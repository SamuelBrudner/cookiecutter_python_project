#!/usr/bin/env python
"""Pre-generation hooks for cookiecutter."""

import re
import sys
from pathlib import Path

def validate_project_slug(slug: str) -> bool:
    """Validate project slug format."""
    # Must start with a letter and contain only letters, numbers, and underscores
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', slug):
        print(
            "ERROR: Project slug must start with a letter and "
            "contain only letters, numbers, and underscores."
        )
        return False
    return True

def validate_python_version(version: str) -> bool:
    """Validate Python version format."""
    if not re.match(r'^\d+\.\d+(\.\d+)?$', version):
        print("ERROR: Python version must be in format X.Y or X.Y.Z")
        return False
    return True

def validate_email(email: str) -> bool:
    """Validate email format."""
    if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
        print("ERROR: Invalid email format")
        return False
    return True

def main():
    """Main function for pre-generation hooks."""
    # Get cookiecutter variables
    project_slug = '{{ cookiecutter.project_slug }}'
    python_version = '{{ cookiecutter.python_version }}'
    author_email = '{{ cookiecutter.author_email }}'
    
    # Validate inputs
    if not validate_project_slug(project_slug):
        sys.exit(1)
    
    if not validate_python_version(python_version):
        sys.exit(1)
    
    if not validate_email(author_email):
        sys.exit(1)
    
    # Check if project directory already exists
    project_dir = Path.cwd() / project_slug
    if project_dir.exists():
        print(f"ERROR: Directory {project_slug} already exists")
        sys.exit(1)

if __name__ == '__main__':
    main()
