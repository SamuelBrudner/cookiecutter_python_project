ensure_conda_lock() {
    if command -v conda-lock >/dev/null 2>&1; then
        return 0
    fi

    if [ -n "${ENV_PATH:-}" ] && command -v conda >/dev/null 2>&1; then
        if conda run --prefix "${ENV_PATH}" pip install conda-lock >/dev/null 2>&1; then
            export PATH="${ENV_PATH}/bin:$PATH"
            command -v conda-lock >/dev/null 2>&1 && return 0
        fi
    fi

    if command -v pip >/dev/null 2>&1; then
        if pip install --user conda-lock >/dev/null 2>&1; then
            export PATH="$HOME/.local/bin:$PATH"
            command -v conda-lock >/dev/null 2>&1 && return 0
        fi
    fi

    if command -v python >/dev/null 2>&1; then
        local _tmp_venv
        _tmp_venv="$(mktemp -d)"
        if python -m venv "${_tmp_venv}" >/dev/null 2>&1 && \
           "${_tmp_venv}/bin/pip" install conda-lock >/dev/null 2>&1; then
            export PATH="${_tmp_venv}/bin:$PATH"
            command -v conda-lock >/dev/null 2>&1 && return 0
        fi
    fi

    return 1
}

return 0 2>/dev/null || true
