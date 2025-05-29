setup_pre_commit() {
    if [ "${SKIP_PRE_COMMIT}" = true ]; then
        log "info" "Skipping pre-commit setup as requested"
        return 0
    fi

    section "Setting up pre-commit hooks"

    # Check if pre-commit is installed
    if ! command -v pre-commit &> /dev/null; then
        log "info" "Installing pre-commit..."
        run_command_verbose conda install -y -c conda-forge pre-commit
    fi

    # Install pre-commit hooks
    log "info" "Installing pre-commit hooks..."
    run_command_verbose pre-commit install --install-hooks || \
        log "warning" "Failed to install some pre-commit hooks"

    log "success" "pre-commit hooks installed"
}

return 0 2>/dev/null || true
