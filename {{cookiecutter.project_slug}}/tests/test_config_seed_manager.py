"""Tests for config settings and seed manager."""

import os

from .conftest import load_project_module

config = load_project_module("config_module", "config", "__init__.py")
seed_mod = load_project_module("seed_manager_module", "utils", "seed_manager.py")


class TestSettings:
    def test_defaults(self):
        """Settings should use default project values."""
        s = config.Settings()
        assert s.PROJECT_NAME == "{{ cookiecutter.project_name }}"
        assert s.API_V1_STR == "/api/v1"

    def test_database_uri_assembly(self, monkeypatch):
        """Database URI should assemble from components when not provided."""
        monkeypatch.setenv("POSTGRES_SERVER", "dbserver")
        monkeypatch.setenv("POSTGRES_USER", "user")
        monkeypatch.setenv("POSTGRES_PASSWORD", "pass")
        monkeypatch.setenv("POSTGRES_DB", "db")
        s = config.Settings()
        assert s.DATABASE_URI == "postgresql://user:pass@dbserver/db"


class TestSeedManager:
    def test_set_get_global_seed(self):
        """Global seed helper functions should update the global manager."""
        seed_mod.set_global_seed(1234)
        assert seed_mod.get_global_seed() == 1234
        manager = seed_mod.get_seed_manager()
        state = manager.get_state()
        assert state["seed"] == 1234
        assert isinstance(manager, seed_mod.SeedManager)
