from pathlib import Path


def test_citation_file_exists():
    project_root = Path(__file__).resolve().parents[1]
    citation = project_root / "CITATION.cff"
    assert citation.is_file(), "CITATION.cff should exist at project root"
    content = citation.read_text()
    assert "{{ cookiecutter.project_name }}" in content
    assert "{{ cookiecutter.version }}" in content
    assert "{{ cookiecutter.author_name }}" in content
