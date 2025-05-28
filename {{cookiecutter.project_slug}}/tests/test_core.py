"""Tests for core module functionality."""

import pytest
from pathlib import Path
from {{ cookiecutter.project_slug }}.core import (
    get_project_root,
    get_version,
    Config,
    config as global_config
)


def test_get_project_root():
    """Test that get_project_root returns a valid directory."""
    root = get_project_root()
    assert root.is_dir()
    assert (root / "pyproject.toml").exists()


def test_get_version():
    """Test that get_version returns a non-empty string."""
    version = get_version()
    assert isinstance(version, str)
    assert version.strip() != ""


class TestConfig:
    """Tests for the Config class."""

    def test_get_set(self):
        """Test getting and setting config values."""
        cfg = Config()
        assert cfg.get("nonexistent") is None
        assert cfg.get("nonexistent", "default") == "default"
        
        cfg.set("test_key", "test_value")
        assert cfg.get("test_key") == "test_value"

    def test_initial_values(self):
        """Test initializing with values."""
        cfg = Config({"key1": "value1", "key2": 42})
        assert cfg.get("key1") == "value1"
        assert cfg.get("key2") == 42


def test_global_config():
    """Test the global config instance."""
    assert isinstance(global_config, Config)
    assert global_config.get("project_name") == "{{ cookiecutter.project_name }}"
    assert global_config.get("version") == "{{ cookiecutter.version }}"
