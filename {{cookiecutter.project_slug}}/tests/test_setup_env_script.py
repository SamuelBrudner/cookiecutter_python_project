import os
import shutil
import subprocess
from pathlib import Path


def make_stub(name: str, directory: Path) -> None:
    path = directory / name
    if name == "conda":
        path.write_text(
            "#!/bin/sh\n"
            "if [ \"$1\" = 'info' ] && [ \"$2\" = '--base' ]; then\n"
            "  echo /tmp\n"
            "  exit 0\n"
            "elif [ \"$1\" = 'info' ] && [ \"$2\" = '--envs' ]; then\n"
            "  echo \"$STUB_ENV_PATH *\"\n"
            "  exit 0\n"
            "fi\n"
            "exit 0\n"
        )
    else:
        path.write_text("#!/bin/sh\nexit 0\n")
    path.chmod(0o755)


def _prepare_scripts(tmp_path: Path) -> Path:
    """Copy setup scripts into a temporary directory and return the path."""
    setup_dir = tmp_path / "setup"
    setup_dir.mkdir()
    project_root = Path(__file__).resolve().parents[2] / "{{cookiecutter.project_slug}}"
    shutil.copy(project_root / "setup" / "setup_env.sh", setup_dir)
    shutil.copy(project_root / "setup" / "setup_utils.sh", setup_dir)
    modules_src = project_root / "setup" / "modules"
    modules_dst = setup_dir / "modules"
    shutil.copytree(modules_src, modules_dst)
    os.chmod(setup_dir / "setup_env.sh", 0o755)
    os.chmod(setup_dir / "setup_utils.sh", 0o755)
    return setup_dir


def _prepare_environment_files(setup_dir: Path) -> None:
    """Create minimal environment files expected by the script."""
    (setup_dir / "environment.yml").write_text("name: base\n")
    (setup_dir / "environment-dev.yml").write_text("name: dev\n")


def _create_stubs(bin_dir: Path) -> None:
    for cmd in ["conda", "pip", "pre-commit", "conda-lock", "pytest"]:
        make_stub(cmd, bin_dir)


def test_dev_flag_selects_dev_env(tmp_path: Path) -> None:
    setup_dir = _prepare_scripts(tmp_path)
    _prepare_environment_files(setup_dir)

    # Create stub commands to satisfy script dependencies
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    _create_stubs(bin_dir)

    # Minimal files expected by the script
    etc_dir = Path("/tmp/etc/profile.d")
    etc_dir.mkdir(parents=True, exist_ok=True)
    (etc_dir / "conda.sh").write_text("")

    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}:{env['PATH']}"
    env["STUB_ENV_PATH"] = str(setup_dir / "dev-env")

    script = setup_dir / "setup_env.sh"
    result = subprocess.run([
        str(script),
        "--dev",
        "--verbose",
        "--force",
    ], cwd=setup_dir, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    print(result.stdout)
    assert result.returncode == 0
    assert "Using development environment file" in result.stdout


def test_source_without_run_setup(tmp_path: Path) -> None:
    """Sourcing the script should not run the setup by default."""
    setup_dir = _prepare_scripts(tmp_path)
    _prepare_environment_files(setup_dir)

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    _create_stubs(bin_dir)

    etc_dir = Path("/tmp/etc/profile.d")
    etc_dir.mkdir(parents=True, exist_ok=True)
    (etc_dir / "conda.sh").write_text("")

    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}:{env['PATH']}"
    env["STUB_ENV_PATH"] = str(setup_dir / "dev-env")

    script = setup_dir / "setup_env.sh"
    result = subprocess.run(
        ["bash", "-c", f"source {script}"],
        cwd=setup_dir,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    print(result.stdout)
    assert result.returncode == 0
    assert "Environment setup completed" not in result.stdout


def test_source_with_run_setup(tmp_path: Path) -> None:
    """Sourcing with --run-setup should execute the setup."""
    setup_dir = _prepare_scripts(tmp_path)
    _prepare_environment_files(setup_dir)

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    _create_stubs(bin_dir)

    etc_dir = Path("/tmp/etc/profile.d")
    etc_dir.mkdir(parents=True, exist_ok=True)
    (etc_dir / "conda.sh").write_text("")

    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}:{env['PATH']}"
    env["STUB_ENV_PATH"] = str(setup_dir / "dev-env")

    script = setup_dir / "setup_env.sh"
    result = subprocess.run(
        ["bash", "-c", f"source {script} --run-setup --verbose"],
        cwd=setup_dir,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    print(result.stdout)
    assert result.returncode == 0
    assert "Environment setup completed" in result.stdout

