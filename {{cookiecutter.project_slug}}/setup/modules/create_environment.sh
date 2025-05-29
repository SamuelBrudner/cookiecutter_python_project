create_environment() {
    if [ "${SKIP_CONDA}" = true ]; then
        log "info" "Skipping environment creation as requested"
        return 0
    fi

    # Check if environment already exists
    if [ -d "${ENV_PATH}" ]; then
        if [ "${FORCE}" = true ]; then
            log "warning" "Removing existing environment at ${ENV_PATH} (--force)"
            rm -rf "${ENV_PATH}"
        else
            log "info" "Using existing environment at ${ENV_PATH}"
            return 0
        fi
    fi

    # Create conda environment
    section "Creating conda environment"
    log "info" "Creating environment with Python ${PYTHON_VERSION}"

    run_command_verbose conda create -y -p "${ENV_PATH}" python="${PYTHON_VERSION}" || \
        error "Failed to create conda environment"

    # Initialize the new environment
    log "info" "Initializing new environment..."
    CONDA_BASE=$(conda info --base)
    source "${CONDA_BASE}/etc/profile.d/conda.sh"
    conda activate "${ENV_PATH}" || error "Failed to activate new environment"

    log "success" "Environment created at ${ENV_PATH}"
}

return 0 2>/dev/null || true
