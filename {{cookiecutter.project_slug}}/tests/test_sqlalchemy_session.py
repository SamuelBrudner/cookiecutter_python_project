from .conftest import load_project_module

# Load required modules with package context so relative imports succeed
load_project_module("pkg.config", "config", "__init__.py")
session_mod = load_project_module("pkg.db.session", "db", "session.py")

def test_sessionlocal_import():
    assert hasattr(session_mod, "SessionLocal")

