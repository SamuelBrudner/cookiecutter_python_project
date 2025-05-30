generate_conda_lock() {
    if [ "${SKIP_LOCK}" = true ]; then
        log "info" "Skipping conda-lock generation as requested"
        return 0
    fi

    section "Generating conda-lock file"

    # Ensure conda-lock is available
    if ! ensure_conda_lock; then
        log "warning" "conda-lock unavailable; skipping lock generation"
        return 0
    fi

    # Determine platform
    local platform=""
    case "$(uname -s)" in
        Darwin*)
            if [ "$(uname -m)" = "arm64" ]; then
                platform="osx-arm64"
            else
                platform="osx-64"
            fi
            ;;
        Linux*)
            platform="linux-64"
            ;;
        *)
            log "warning" "Unsupported platform for conda-lock: $(uname -s)"
            return 1
            ;;
    esac

    log "info" "Generating lock file for platform: ${platform}"
    run_command_verbose conda-lock -f environment.yml -p "${platform}" --lockfile conda-lock.yml || \
        log "warning" "Failed to generate conda-lock file"

    log "success" "conda-lock file generated"
}

return 0 2>/dev/null || true
