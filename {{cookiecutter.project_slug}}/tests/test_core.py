"""Tests for core module functionality."""

from pathlib import Path

from .conftest import load_project_module

# Load the core module directly from the source tree
core = load_project_module("core_module", "core", "__init__.py")


def test_get_project_root():
    """get_project_root should point to the repository root."""
    root = core.get_project_root()
    assert root.is_dir()
    assert (root / "pyproject.toml").exists()


def test_get_version():
    """get_version should return a non-empty string."""
    version = core.get_version()
    assert isinstance(version, str)
    assert version.strip() != ""


class TestConfig:
    """Tests for the Config class."""

    def test_get_set(self):
        cfg = core.Config()
        assert cfg.get("nonexistent") is None
        assert cfg.get("nonexistent", "default") == "default"

        cfg.set("test_key", "test_value")
        assert cfg.get("test_key") == "test_value"

    def test_initial_values(self):
        cfg = core.Config({"key1": "value1", "key2": 42})
        assert cfg.get("key1") == "value1"
        assert cfg.get("key2") == 42


def test_global_config():
    """Ensure the global config instance has the expected defaults."""
    assert isinstance(core.config, core.Config)
    assert core.config.get("project_name") == "{{ cookiecutter.project_name }}"
    assert core.config.get("version") == "{{ cookiecutter.version }}"
