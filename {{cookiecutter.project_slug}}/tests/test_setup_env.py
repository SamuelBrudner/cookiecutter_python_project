import subprocess
from pathlib import Path
import pytest

SCRIPT = Path(__file__).parents[1] / "setup" / "setup_env.sh"

@pytest.mark.parametrize("flag", [
    "--no-tests",
    "--skip-conda",
    "--skip-pre-commit",
    "--skip-lock",
    "--clean-install",
    "--force",
    "-v",
    "--verbose",
])
def test_flags_parse_with_help(flag):
    result = subprocess.run(["bash", str(SCRIPT), flag, "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert result.returncode == 0
    output = result.stdout.decode() + result.stderr.decode()
    assert "Usage" in output

def test_help_and_short_help():
    for flag in ("--help", "-h"):
        result = subprocess.run(["bash", str(SCRIPT), flag], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        assert result.returncode == 0
        output = result.stdout.decode() + result.stderr.decode()
        assert "Usage" in output

def test_unknown_parameter():
    result = subprocess.run(["bash", str(SCRIPT), "--unknown"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert result.returncode != 0
