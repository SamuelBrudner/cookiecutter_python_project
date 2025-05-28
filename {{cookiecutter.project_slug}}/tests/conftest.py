"""Pytest configuration and common test utilities."""

from __future__ import annotations

import importlib.util
import os
import re
import sys
import types
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """Return the path to the test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture(autouse=True)
def setup_logging():
    """Configure logging for tests."""
    import logging

    logging.basicConfig(level=logging.INFO)
    # Disable logging for test runs
    logging.disable(logging.CRITICAL)
    yield
    # Re-enable logging after tests complete
    logging.disable(logging.NOTSET)


def _create_stub_modules() -> None:
    """Install lightweight stubs for optional dependencies."""

    if "pydantic" not in sys.modules:
        pydantic = types.ModuleType("pydantic")

        class BaseSettings:
            def __init__(self, **values: object) -> None:
                for name, default in self.__class__.__dict__.items():
                    if name.isupper():
                        setattr(self, name, values.get(name, os.getenv(name, default)))
                import inspect
                for attr in dir(self.__class__):
                    method = getattr(self.__class__, attr)
                    if hasattr(method, "_validator_field"):
                        field = method._validator_field
                        val = getattr(self, field, None)
                        params = inspect.signature(method).parameters
                        if len(params) == 3:
                            new_val = method(cls=self.__class__, v=val, values=self.__dict__)
                        else:
                            new_val = method(cls=self.__class__, v=val)
                        setattr(self, field, new_val)

        def validator(field: str, pre: bool = False):
            def decorator(func):
                func._validator_field = field
                return func

            return decorator

        class EmailStr(str):
            pass

        class AnyHttpUrl(str):
            pass

        pydantic.BaseSettings = BaseSettings
        pydantic.validator = validator
        pydantic.EmailStr = EmailStr
        pydantic.AnyHttpUrl = AnyHttpUrl
        sys.modules["pydantic"] = pydantic

    if "numpy" not in sys.modules:
        numpy = types.ModuleType("numpy")
        numpy.random = types.SimpleNamespace(seed=lambda seed: None)
        sys.modules["numpy"] = numpy

    if "torch" not in sys.modules:
        torch = types.ModuleType("torch")
        torch.manual_seed = lambda seed: None
        torch.cuda = types.SimpleNamespace(is_available=lambda: False, manual_seed_all=lambda seed: None)
        torch.backends = types.SimpleNamespace(cudnn=types.SimpleNamespace(deterministic=False, benchmark=False))
        sys.modules["torch"] = torch

    if "tensorflow" not in sys.modules:
        tf = types.ModuleType("tensorflow")
        tf.random = types.SimpleNamespace(set_seed=lambda seed: None)
        sys.modules["tensorflow"] = tf

    if "jax" not in sys.modules:
        jax = types.ModuleType("jax")
        jax.config = types.SimpleNamespace(update=lambda *args, **kwargs: None)
        jax.random = types.SimpleNamespace(PRNGKey=lambda seed: seed)
        sys.modules["jax"] = jax
        sys.modules["jax.numpy"] = types.ModuleType("jax.numpy")


@pytest.fixture(scope="session", autouse=True)
def stub_dependencies() -> None:
    """Ensure optional dependencies are available during tests."""

    _create_stub_modules()


def load_module_from_path(name: str, path: Path):
    """Load a module from a file, ignoring Jinja template syntax."""

    with open(path, "r", encoding="utf-8") as handle:
        source = handle.read()
    source = re.sub(r"{%.+?%}", "", source, flags=re.DOTALL)
    source = re.sub(r"from\s+{{.*?}}\s+import\s+__version__", "__version__ = '0.0.0'", source)
    spec = importlib.util.spec_from_loader(name, loader=None)
    module = importlib.util.module_from_spec(spec)
    module.__file__ = str(path)
    exec(compile(source, str(path), "exec"), module.__dict__)
    sys.modules[name] = module
    return module


def load_project_module(name: str, *parts: str):
    """Helper to load a module from the project source tree."""

    _create_stub_modules()
    base = Path(__file__).resolve().parents[2] / "{{cookiecutter.project_slug}}" / "src" / "{{cookiecutter.project_slug}}"
    return load_module_from_path(name, base.joinpath(*parts))

