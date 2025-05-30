try_load_conda_module() {
    if command -v module >/dev/null 2>&1; then
        for mod in miniconda anaconda; do
            if module avail "$mod" 2>&1 | grep -q "$mod"; then
                log "info" "Loading $mod module"
                module load "$mod" && return 0
            fi
        done
    fi
    return 1
}

setup_conda() {
    if [ "${SKIP_CONDA}" = true ]; then
        log "info" "Skipping conda setup as requested"
        return 0
    fi

    # Check if conda is available
    if ! command -v conda &> /dev/null; then
        log "warning" "Conda not found in PATH"

        # Try loading a conda module if available
        try_load_conda_module || true

        if ! command -v conda &> /dev/null; then
            # If we're in a container, try to install miniconda
            if [ -f /.dockerenv ] || grep -q docker /proc/1/cgroup 2>/dev/null; then
                install_conda_in_container
            else
                error "conda is not installed or not in PATH.\nPlease install Miniconda/Anaconda first: https://docs.conda.io/en/latest/miniconda.html"
            fi
        fi
    fi

    # Initialize conda for this shell
    log "info" "Initializing conda..."
    __conda_setup="$($(command -v conda) 'shell.bash' 'hook' 2> /dev/null)"
    if [ $? -eq 0 ]; then
        eval "$__conda_setup"
        log "debug" "Conda shell integration initialized"
    else
        if [ -f "${CONDA_PREFIX:-/dev/null}/etc/profile.d/conda.sh" ]; then
            . "${CONDA_PREFIX}/etc/profile.d/conda.sh"
            log "debug" "Sourced conda.sh from ${CONDA_PREFIX}/etc/profile.d/"
        else
            local found=""
            for prefix in "${HOME}/miniconda3" "/usr/local/miniconda" "/opt/conda"; do
                if [ -f "${prefix}/etc/profile.d/conda.sh" ]; then
                    . "${prefix}/etc/profile.d/conda.sh"
                    log "debug" "Sourced conda.sh from ${prefix}/etc/profile.d/"
                    found=1
                    break
                fi
            done
            if [ -z "$found" ]; then
                export PATH="$(conda info --base)/bin:$PATH"
                log "warning" "Could not find conda.sh, added conda to PATH"
            fi
        fi
    fi
    unset __conda_setup

    # Verify conda is working
    if ! command -v conda &> /dev/null; then
        error "Failed to initialize conda. Please check your installation."
    fi

    log "success" "Conda initialized: $(conda --version 2>/dev/null || echo 'unknown version')"
}

# Install conda in a container environment
install_conda_in_container() {
    section "Installing Miniconda in container..."

    # Install wget if not available
    if ! command -v wget &> /dev/null; then
        log "info" "Installing wget..."
        if command -v apt-get &> /dev/null; then
            run_command_verbose apt-get update
            run_command_verbose apt-get install -y wget
        elif command -v yum &> /dev/null; then
            run_command_verbose yum install -y wget
        elif command -v apk &> /dev/null; then
            run_command_verbose apk add --no-cache wget
        else
            error "Could not install wget: package manager not found"
        fi
    fi

    # Download and install Miniconda
    local miniconda_installer="/tmp/miniconda.sh"
    local conda_prefix="/opt/conda"

    log "info" "Downloading Miniconda installer..."
    run_command_verbose wget -q "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-$(uname -m).sh" -O "$miniconda_installer"

    log "info" "Installing Miniconda to ${conda_prefix}..."
    run_command_verbose bash "$miniconda_installer" -b -p "$conda_prefix"
    run_command_verbose rm -f "$miniconda_installer"

    # Add conda to PATH
    export PATH="${conda_prefix}/bin:$PATH"

    # Verify installation
    if ! command -v conda &> /dev/null; then
        error "Failed to find conda after installation. PATH: $PATH"
    fi

    log "success" "Miniconda installed successfully: $(conda --version 2>/dev/null || echo 'unknown version')"
}

return 0 2>/dev/null || true
