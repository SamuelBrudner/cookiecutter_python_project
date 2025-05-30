import json
import os
from pathlib import Path


def run_notebook(nb_path: Path, workdir: Path) -> None:
    """Execute a minimal Jupyter notebook composed of code cells."""
    with nb_path.open() as f:
        nb = json.load(f)
    cwd = os.getcwd()
    os.chdir(workdir)
    try:
        env = {}
        for cell in nb.get("cells", []):
            if cell.get("cell_type") == "code":
                code = "".join(cell.get("source", []))
                exec(code, env)
    finally:
        os.chdir(cwd)


def test_config_notebook_creates_paths(tmp_path: Path):
    notebook = Path(__file__).parents[1] / "notebooks" / "config.ipynb"
    run_notebook(notebook, tmp_path)
    out_file = tmp_path / "configs" / "paths.yaml"
    assert out_file.exists(), "paths.yaml should be created"
    assert "default_dir: data" in out_file.read_text()
