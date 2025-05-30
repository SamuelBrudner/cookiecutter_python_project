from pathlib import Path


def test_license_files_exist() -> None:
    """Both repository and template root should contain MIT license."""
    template_root = Path(__file__).resolve().parents[1]
    repo_root = template_root.parent

    repo_license = repo_root / "LICENSE"
    template_license = template_root / "LICENSE"

    assert repo_license.exists(), "LICENSE file missing at repository root"
    assert template_license.exists(), "LICENSE file missing in template"

    text = template_license.read_text()
    assert "MIT License" in text
