"""Core functionality for {{ cookiecutter.project_name }}.

This module provides core utilities and configuration for the package.
"""

import logging
from pathlib import Path
from typing import Any, Dict, Optional

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def get_project_root() -> Path:
    """Get the root directory of the project.
    
    Returns:
        Path to the project root directory.
    """
    return Path(__file__).parent.parent.parent.parent


def get_version() -> str:
    """Get the current version of the package.
    
    Returns:
        Package version as a string.
    """
    from {{ cookiecutter.project_slug }} import __version__
    return __version__


class Config:
    """Simple configuration manager.
    
    Example:
        >>> config = Config({"key": "value"})
        >>> config.get("key")
        'value'
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self._config = dict(config) if config else {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self._config[key] = value


# Default configuration
config = Config({
    "project_name": "{{ cookiecutter.project_name }}",
    "version": "{{ cookiecutter.version }}",
    "python_version": "{{ cookiecutter.python_version }}",
})
