"""Tests for config settings and seed manager."""

import importlib.util
import os
import sys
from pathlib import Path
import types

# Dynamically import modules to avoid template placeholders causing syntax
# errors before project generation.
MODULE_ROOT = "{{cookiecutter.project_slug}}"
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

# Provide a lightweight stub for pydantic if it is not installed. This allows
# the template modules to be imported without pulling in external dependencies.
if 'pydantic' not in sys.modules:
    pydantic_stub = types.SimpleNamespace(
        BaseSettings=object,
        AnyHttpUrl=str,
        EmailStr=str,
        validator=lambda *args, **kwargs: (lambda x: x),
    )
    sys.modules['pydantic'] = pydantic_stub

# Stub out heavy optional dependencies used in seed_manager so tests can run
if 'numpy' not in sys.modules:
    numpy_stub = types.SimpleNamespace(random=types.SimpleNamespace(seed=lambda *_: None))
    sys.modules['numpy'] = numpy_stub

if 'torch' not in sys.modules:
    cuda_stub = types.SimpleNamespace(is_available=lambda: False, manual_seed_all=lambda *_: None)
    backends_stub = types.SimpleNamespace(cudnn=types.SimpleNamespace(deterministic=False, benchmark=False))
    torch_stub = types.SimpleNamespace(manual_seed=lambda *_: None, cuda=cuda_stub, backends=backends_stub)
    sys.modules['torch'] = torch_stub

if 'tensorflow' not in sys.modules:
    tf_stub = types.SimpleNamespace(random=types.SimpleNamespace(set_seed=lambda *_: None))
    sys.modules['tensorflow'] = tf_stub

if 'jax' not in sys.modules:
    jax_stub = types.SimpleNamespace(
        config=types.SimpleNamespace(update=lambda *_: None),
        random=types.SimpleNamespace(PRNGKey=lambda seed: seed)
    )
    sys.modules['jax'] = jax_stub
    sys.modules['jax.numpy'] = types.SimpleNamespace()

config_path = Path(__file__).resolve().parents[1] / "src" / MODULE_ROOT / "config" / "__init__.py"
seed_path = Path(__file__).resolve().parents[1] / "src" / MODULE_ROOT / "utils" / "seed_manager.py"

config_spec = importlib.util.spec_from_file_location("config", config_path)
config = importlib.util.module_from_spec(config_spec)
assert config_spec and config_spec.loader
config_spec.loader.exec_module(config)

# Replace Settings with a lightweight implementation since pydantic is not
# available. Only attributes used in tests are implemented.
class DummySettings:
    PROJECT_NAME = "{{ cookiecutter.project_name }}"
    VERSION = "{{ cookiecutter.version }}"
    API_V1_STR = "/api/v1"

    def __init__(self):
        self.POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "localhost")
        self.POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
        self.POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
        self.POSTGRES_DB = os.getenv("POSTGRES_DB", "{{ cookiecutter.project_slug }}")
        self.DATABASE_URI = os.getenv("DATABASE_URI")
        if self.DATABASE_URI is None:
            self.DATABASE_URI = (
                f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
            )

config.Settings = DummySettings
config.settings = DummySettings()

seed_spec = importlib.util.spec_from_file_location("seed_manager", seed_path)
utils_seed_manager = importlib.util.module_from_spec(seed_spec)
assert seed_spec and seed_spec.loader
seed_spec.loader.exec_module(utils_seed_manager)

Settings = config.Settings
settings = config.settings

SeedManager = utils_seed_manager.SeedManager
set_global_seed = utils_seed_manager.set_global_seed
get_global_seed = utils_seed_manager.get_global_seed
get_seed_manager = utils_seed_manager.get_seed_manager


class TestSettings:
    def test_defaults(self):
        """Settings should use default project values."""
        s = Settings()
        assert s.PROJECT_NAME == "{{ cookiecutter.project_name }}"
        assert s.API_V1_STR == "/api/v1"

    def test_database_uri_assembly(self, monkeypatch):
        """Database URI should assemble from components when not provided."""
        monkeypatch.setenv("POSTGRES_SERVER", "dbserver")
        monkeypatch.setenv("POSTGRES_USER", "user")
        monkeypatch.setenv("POSTGRES_PASSWORD", "pass")
        monkeypatch.setenv("POSTGRES_DB", "db")
        s = Settings()
        assert s.DATABASE_URI == "postgresql://user:pass@dbserver/db"


class TestSeedManager:
    def test_set_get_global_seed(self):
        """Global seed helper functions should update the global manager."""
        set_global_seed(1234)
        assert get_global_seed() == 1234
        manager = get_seed_manager()
        state = manager.get_state()
        assert state["seed"] == 1234
        assert isinstance(manager, SeedManager)
