import os
import shutil
import subprocess
from pathlib import Path


def _prepare_setup_files(tmp_path: Path) -> Path:
    project_root = Path(__file__).resolve().parents[3] / "{{cookiecutter.project_slug}}"
    setup_dir = tmp_path / "setup"
    setup_dir.mkdir()
    shutil.copy(project_root / "setup" / "modules" / "setup_conda.sh", setup_dir)
    shutil.copy(project_root / "setup" / "setup_utils.sh", setup_dir)
    return setup_dir


def _create_stub_module(bin_dir: Path, log_file: Path) -> None:
    script = bin_dir / "module"
    script.write_text(
        f"#!/bin/sh\n"
        f"echo \"$@\" >> '{log_file}'\n"
        "if [ \"$1\" = 'avail' ]; then\n"
        "  echo miniconda\n"
        "fi\n"
    )
    script.chmod(0o755)


def _create_stub_module_no_avail(bin_dir: Path, log_file: Path) -> None:
    script = bin_dir / "module"
    script.write_text(
        f"#!/bin/sh\n"
        f"echo \"$@\" >> '{log_file}'\n"
        "if [ \"$1\" = 'avail' ]; then\n"
        "  : # no modules available\n"
        "  exit 0\n"
        "fi\n"
    )
    script.chmod(0o755)


def _create_stub_conda(bin_dir: Path, log_file: Path) -> None:
    script = bin_dir / "conda"
    script.write_text(
        f"#!/bin/sh\n"
        f"echo conda \"$@\" >> '{log_file}'\n"
        "if [ \"$1\" = 'shell.bash' ] && [ \"$2\" = 'hook' ]; then\n"
        "  exit 0\n"
        "elif [ \"$1\" = 'info' ] && [ \"$2\" = '--base' ]; then\n"
        "  echo /tmp\n"
        "  exit 0\n"
        "elif [ \"$1\" = '--version' ]; then\n"
        "  echo 'conda 4.0'\n"
        "  exit 0\n"
        "fi\n"
        "exit 0\n"
    )
    script.chmod(0o755)


def _create_stub_conda_fail_hook(bin_dir: Path, log_file: Path) -> None:
    """Create a conda stub that fails for the shell hook."""
    script = bin_dir / "conda"
    script.write_text(
        f"#!/bin/sh\n"
        f"echo conda \"$@\" >> '{log_file}'\n"
        "if [ \"$1\" = 'shell.bash' ] && [ \"$2\" = 'hook' ]; then\n"
        "  exit 1\n"
        "elif [ \"$1\" = 'info' ] && [ \"$2\" = '--base' ]; then\n"
        "  echo /tmp\n"
        "  exit 0\n"
        "elif [ \"$1\" = '--version' ]; then\n"
        "  echo 'conda 4.0'\n"
        "  exit 0\n"
        "fi\n"
        "exit 0\n"
    )
    script.chmod(0o755)


def test_setup_conda_uses_module_when_available(tmp_path: Path) -> None:
    log_file = tmp_path / "calls.log"
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()

    _create_stub_module(bin_dir, log_file)

    setup_dir = _prepare_setup_files(tmp_path)

    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}:{env['PATH']}"

    script = f"""
        STUB_DIR='{bin_dir}'
        source '{setup_dir}/setup_utils.sh'
        source '{setup_dir}/setup_conda.sh'
        log() {{ echo "$@" >> '{log_file}'; }}
        section() {{ :; }}
        install_conda_in_container() {{
            echo install >> '{log_file}';
            cat <<'EOS' > "$STUB_DIR/conda"
#!/bin/sh
echo conda "$@" >> '{log_file}'
if [ "$1" = 'shell.bash' ] && [ "$2" = 'hook' ]; then exit 0; fi
if [ "$1" = 'info' ] && [ "$2" = '--base' ]; then echo /tmp; exit 0; fi
if [ "$1" = '--version' ]; then echo 'conda 4.0'; exit 0; fi
exit 0
EOS
            chmod +x "$STUB_DIR/conda"
        }}
        setup_conda
    """

    result = subprocess.run(["bash", "-c", script], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    print(result.stdout)
    assert result.returncode == 0
    assert "load miniconda" in log_file.read_text()


def test_try_load_conda_module_fails_when_no_modules(tmp_path: Path) -> None:
    log_file = tmp_path / "calls.log"
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()

    _create_stub_module_no_avail(bin_dir, log_file)

    setup_dir = _prepare_setup_files(tmp_path)

    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}:{env['PATH']}"

    status_file = tmp_path / "status.txt"

    script = f"""
        source '{setup_dir}/setup_utils.sh'
        source '{setup_dir}/setup_conda.sh'
        log() {{ echo "$@" >> '{log_file}'; }}
        try_load_conda_module
        echo $? > '{status_file}'
    """

    result = subprocess.run([
        "bash",
        "-c",
        script,
    ], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    print(result.stdout)
    assert result.returncode == 0
    assert status_file.read_text().strip() != "0"
    assert "load" not in log_file.read_text()


def test_sources_known_prefix_when_hook_fails(tmp_path: Path) -> None:
    """setup_conda should source conda.sh from common locations."""
    log_file = tmp_path / "calls.log"
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()

    _create_stub_conda_fail_hook(bin_dir, log_file)

    setup_dir = _prepare_setup_files(tmp_path)

    home_dir = tmp_path / "home"
    conda_sh = home_dir / "miniconda3" / "etc" / "profile.d" / "conda.sh"
    conda_sh.parent.mkdir(parents=True)
    conda_sh.write_text("echo sourced")

    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}:{env['PATH']}"
    env["HOME"] = str(home_dir)

    script = f"""
        source '{setup_dir}/setup_utils.sh'
        source '{setup_dir}/setup_conda.sh'
        log() {{ echo "$@" >> '{log_file}'; }}
        section() {{ :; }}
        setup_conda
    """

    result = subprocess.run([
        "bash",
        "-c",
        script,
    ], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    print(result.stdout)
    assert result.returncode == 0
    assert str(conda_sh.parent) in log_file.read_text()
