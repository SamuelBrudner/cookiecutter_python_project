#!/usr/bin/env python
"""Post-generation hooks for cookiecutter."""

import os
import shutil
from pathlib import Path

def remove_file(filepath: str) -> None:
    """Remove a file if it exists."""
    if os.path.exists(filepath):
        os.remove(filepath)

def remove_dir(dirpath: str) -> None:
    """Remove a directory if it exists."""
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)

def main():
    """Main function for post-generation hooks."""
    project_slug = '{{ cookiecutter.project_slug }}'
    include_api = '{{ cookiecutter.include_api }}'.lower()
    
    # Get the project directory
    project_dir = Path.cwd() / project_slug
    
    # Handle API inclusion/exclusion
    if include_api != 'y':
        # Remove API-related files and directories
        api_dir = project_dir / 'src' / project_slug / 'api'
        if api_dir.exists():
            shutil.rmtree(api_dir)
        
        # Remove API imports from __init__.py
        init_file = project_dir / 'src' / project_slug / '__init__.py'
        if init_file.exists():
            with open(init_file, 'r') as f:
                content = f.read()
            
            # Remove API import lines
            lines = content.split('\n')
            filtered_lines = [
                line for line in lines 
                if 'from .api import' not in line and '{% if cookiecutter.include_api' not in line
                and '{% endif %}' not in line
            ]
            
            with open(init_file, 'w') as f:
                f.write('\n'.join(filtered_lines))
    
    # Initialize git repository
    os.system('git init')
    os.system('git add .')
    os.system('git commit -m "Initial commit"')

if __name__ == '__main__':
    main()
