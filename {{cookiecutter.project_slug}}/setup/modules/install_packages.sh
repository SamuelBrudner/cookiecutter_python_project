install_packages() {
    section "Installing packages"

    # Ensure we're in the right environment
    local env_path=$(conda info --envs | grep -E "^${ENV_PATH}\s" | awk '{print $1}')
    if [ -z "${env_path}" ]; then
        error "Target environment not found. Please create it first."
    fi

    # Activate the environment
    CONDA_BASE=$(conda info --base)
    source "${CONDA_BASE}/etc/profile.d/conda.sh"
    conda activate "${ENV_PATH}" || error "Failed to activate environment"

    # Install development dependencies
    log "info" "Installing development dependencies..."

    # First install pip, setuptools, and wheel
    run_command_verbose conda install -y -c conda-forge pip setuptools wheel

    # Install the package in development mode with all extras
    log "info" "Installing package in development mode..."
    run_command_verbose pip install -e ".[dev]" || \
        error "Failed to install package in development mode"

    log "success" "Package installed in development mode"
}

return 0 2>/dev/null || true
