from pathlib import Path


def test_precommit_includes_jupytext_and_nbstripout() -> None:
    config_path = Path(__file__).resolve().parents[1] / ".pre-commit-config.yaml"
    assert config_path.exists(), ".pre-commit-config.yaml missing"
    text = config_path.read_text()
    assert "jupytext" in text, "pre-commit should include jupytext hook"
    assert "nbstripout" in text, "pre-commit should include nbstripout hook"


def test_jupytext_config_exists() -> None:
    cfg = Path(__file__).resolve().parents[1] / ".jupytext.toml"
    assert cfg.exists(), ".jupytext.toml should exist"


def test_gitattributes_uses_nbdime() -> None:
    path = Path(__file__).resolve().parents[1] / ".gitattributes"
    assert path.exists(), ".gitattributes missing"
    content = path.read_text()
    assert "*.ipynb diff=nbdime" in content, "nbdime diff driver not configured"


def test_ci_checks_notebooks() -> None:
    ci = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "ci.yml"
    assert ci.exists(), "CI workflow missing"
    text = ci.read_text()
    assert "pre-commit run --files notebooks/*.ipynb" in text, "CI should check notebooks"


def test_dev_deps_include_jupyter_tools() -> None:
    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    text = pyproject.read_text()
    assert "jupytext" in text, "jupytext dependency missing"
    assert "nbstripout" in text, "nbstripout dependency missing"
    assert "nbdime" in text, "nbdime dependency missing"

