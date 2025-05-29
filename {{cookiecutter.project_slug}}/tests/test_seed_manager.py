from .conftest import load_project_module

seed_mod = load_project_module("seed_manager_module", "utils", "seed_manager.py")


def test_set_and_get_global_seed():
    seed_mod.set_global_seed(4321)
    assert seed_mod.get_global_seed() == 4321
    manager = seed_mod.get_seed_manager()
    assert manager.get_state()["seed"] == 4321


def test_seed_manager_seed_everything():
    manager = seed_mod.SeedManager(1111)
    results = manager.seed_everything()
    expected_keys = {"python", "numpy", "pytorch", "tensorflow", "jax"}
    assert set(results.keys()) == expected_keys
    assert all(results.values())
    state = manager.get_state()
    assert set(state["libraries"].keys()) == expected_keys
    assert all(state["libraries"].values())
