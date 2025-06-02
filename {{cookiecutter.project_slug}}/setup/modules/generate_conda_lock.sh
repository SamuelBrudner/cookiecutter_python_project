generate_conda_lock() {
    if [ "${SKIP_LOCK}" = true ]; then
        log "info" "Skipping conda-lock generation as requested"
        return 0
    fi

    local env_file="${1:-${ENV_FILE_TO_USE:-environment.yml}}"

    if [ ! -f "$env_file" ]; then
        log "warning" "Environment file $env_file not found; skipping lock generation"
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

    local temp_env="$SCRIPT_DIR/.temp_env_for_lock.yml"

    log "info" "Creating temporary environment file $temp_env"
    if ! cp "$env_file" "$temp_env"; then
        log "error" "Failed to copy $env_file"
        return 1
    fi

    log "debug" "Removing editable installs from $temp_env"
    if ! sed -i.bak '/^[[:space:]]*-e[[:space:]]/d' "$temp_env" 2>/dev/null; then
        if ! sed -i '' '/^[[:space:]]*-e[[:space:]]/d' "$temp_env" 2>/dev/null; then
            log "warning" "Failed to clean editable installs from $temp_env"
        fi
    fi
    rm -f "${temp_env}.bak" 2>/dev/null || true

    local lock_file="${SCRIPT_DIR}/conda-lock.yml"

    log "info" "Generating lock file for platform: ${platform}"
    run_command_verbose conda-lock -f "$temp_env" -p "$platform" --lockfile "$lock_file" || \
        log "warning" "Failed to generate conda-lock file"

    rm -f "$temp_env"

    log "success" "conda-lock file generated"
}

return 0 2>/dev/null || true
