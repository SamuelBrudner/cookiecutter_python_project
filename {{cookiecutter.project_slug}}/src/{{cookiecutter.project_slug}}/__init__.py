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

# Import utilities
from .utils import (
    SeedManager,
    seed_manager,
    set_global_seed,
    get_global_seed,
    get_seed_manager,
)

# Import API if included
{% if cookiecutter.include_api == 'y' %}
from .api import *  # noqa: F403
{% endif %}

# Define public API
__all__ = [
    # Core functionality
    'get_project_root',
    'get_version',
    'Config',
    'config',
    
    # Randomness and reproducibility
    'SeedManager',
    'seed_manager',
    'set_global_seed',
    'get_global_seed',
    'get_seed_manager',
]
