"""{{ cookiecutter.project_name }} - {{ cookiecutter.project_short_description }}

This is the main package for {{ cookiecutter.project_name }}.
"""

__version__ = "{{ cookiecutter.version }}"

# Import core functionality
from .core import (
    get_project_root,
    get_version,
    Config,
    config,
)

# Import API if included
{% if cookiecutter.include_api == 'y' %}
from .api import *  # noqa: F403
{% endif %}

# Define public API
__all__ = [
    'get_project_root',
    'get_version',
    'Config',
    'config',
]

# Add API exports if included
{% if cookiecutter.include_api == 'y' %}
__all__.extend([
    # Add API exports here
])
{% endif %}
