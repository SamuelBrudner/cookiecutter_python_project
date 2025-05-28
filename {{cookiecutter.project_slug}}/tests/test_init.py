"""Tests for package __init__ imports."""

from {{ cookiecutter.project_slug }} import (
    __version__,
    get_project_root,
    get_version,
    Config,
    config,
    SeedManager,
    seed_manager,
    set_global_seed,
    get_global_seed,
    get_seed_manager,
)


def test_public_api():
    """Ensure public objects are accessible from package level."""
    assert isinstance(__version__, str)
    assert callable(get_project_root)
    assert callable(get_version)
    assert isinstance(config, Config)
    assert callable(set_global_seed)
    assert callable(get_global_seed)
    assert callable(get_seed_manager)
    assert isinstance(seed_manager, SeedManager)
