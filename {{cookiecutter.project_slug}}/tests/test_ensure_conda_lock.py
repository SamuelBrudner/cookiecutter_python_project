import os
import shutil
import subprocess
from pathlib import Path


def _prepare_module(tmp_path: Path) -> Path:
    project_root = Path(__file__).resolve().parents[2] / "{{cookiecutter.project_slug}}"
    setup_dir = tmp_path / "setup"
    setup_dir.mkdir()
    shutil.copy(project_root / "setup" / "setup_utils.sh", setup_dir)
    modules_src = project_root / "setup" / "modules"
    modules_dst = setup_dir / "modules"
    shutil.copytree(modules_src, modules_dst)
    return setup_dir


def _make_stub(name: str, content: str, directory: Path) -> None:
    path = directory / name
    path.write_text(content)
    path.chmod(0o755)


def test_pip_user_fallback(tmp_path: Path) -> None:
    setup_dir = _prepare_module(tmp_path)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    user_bin = tmp_path / ".local" / "bin"
    user_bin.mkdir(parents=True)

    _make_stub("conda", "#!/bin/sh\nexit 1\n", bin_dir)
    pip_content = f"""#!/bin/sh
for arg in "$@"; do
  if [ "$arg" = '--user' ]; then
    mkdir -p '{user_bin}'
    echo '#!/bin/sh\nexit 0' > '{user_bin}/conda-lock'
    chmod +x '{user_bin}/conda-lock'
    exit 0
  fi
done
exit 1
"""
    _make_stub("pip", pip_content, bin_dir)
    _make_stub("python", "#!/bin/sh\nexit 1\n", bin_dir)
    mktemp_stub = f"#!/bin/sh\nmkdir -p {tmp_path}/unused\necho {tmp_path}/unused\n"
    _make_stub("mktemp", mktemp_stub, bin_dir)

    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}:{env['PATH']}"
    env["HOME"] = str(tmp_path)

    result = subprocess.run(
        ["bash", "-c", f"source {setup_dir}/setup_utils.sh; source {setup_dir}/modules/ensure_conda_lock.sh; ensure_conda_lock"],
        env=env,
        cwd=setup_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    assert result.returncode == 0
    assert (user_bin / "conda-lock").exists()


def test_virtualenv_fallback(tmp_path: Path) -> None:
    setup_dir = _prepare_module(tmp_path)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    venv_dir = tmp_path / "venv"
    venv_dir.mkdir()

    _make_stub("conda", "#!/bin/sh\nexit 1\n", bin_dir)
    pip_stub = f"""#!/bin/sh
if [ "$0" = '{venv_dir}/bin/pip' ]; then
  mkdir -p '{venv_dir}/bin'
  echo '#!/bin/sh\nexit 0' > '{venv_dir}/bin/conda-lock'
  chmod +x '{venv_dir}/bin/conda-lock'
  exit 0
fi
exit 1
"""
    _make_stub("pip", pip_stub, bin_dir)
    python_stub = f"""#!/bin/sh
if [ "$1" = '-m' ] && [ "$2" = 'venv' ]; then
  mkdir -p '{venv_dir}/bin'
  cp '{bin_dir}/pip' '{venv_dir}/bin/pip'
  exit 0
fi
exit 1
"""
    _make_stub("python", python_stub, bin_dir)
    mktemp_stub = f"#!/bin/sh\necho {venv_dir}\n"
    _make_stub("mktemp", mktemp_stub, bin_dir)

    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}:{env['PATH']}"

    result = subprocess.run(
        ["bash", "-c", f"source {setup_dir}/setup_utils.sh; source {setup_dir}/modules/ensure_conda_lock.sh; ensure_conda_lock"],
        env=env,
        cwd=setup_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    assert result.returncode == 0
    assert (venv_dir / "bin" / "conda-lock").exists()
