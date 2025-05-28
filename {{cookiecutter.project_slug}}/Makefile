.PHONY: help install test lint format clean docs

# Default target
help:
	@echo "\n\033[1m{{ cookiecutter.project_name }}\033[0m - Development Tools\n"
	@echo "\033[1mInstallation:\033[0m"
	@echo "  install           Install development dependencies"
	@echo "  install-precommit Install pre-commit hooks\n"
	@echo "\033[1mDevelopment:\033[0m"
	@echo "  test              Run tests with coverage"
	@echo "  test-fast         Run tests without coverage"
	@echo "  test-cov          Generate coverage report\n"
	@echo "\033[1mCode Quality:\033[0m"
	@echo "  lint              Run all linters"
	@echo "  format            Format code\n"
	@echo "\033[1mDocumentation:\033[0m"
	@echo "  docs              Generate documentation\n"
	@echo "\033[1mMaintenance:\033[0m"
	@echo "  clean             Remove build artifacts"
	@echo "  dist              Build distribution"

# ===== Installation =====

# Install development dependencies
install:
	@echo "\n\033[1mInstalling dependencies...\033[0m"
	pip install -e .[dev]

# Install pre-commit hooks
install-precommit:
	@echo "\n\033[1mInstalling pre-commit hooks...\033[0m"
	pre-commit install

# ===== Testing =====

# Run tests with coverage
test:
	@echo "\n\033[1mRunning tests...\033[0m"
	pytest -v --cov={{ cookiecutter.project_slug }} --cov-report=term-missing

# Run tests without coverage
test-fast:
	@echo "\n\033[1mRunning tests...\033[0m"
	pytest -v

# Generate coverage report
test-cov:
	@echo "\n\033[1mGenerating coverage report...\033[0m"
	pytest --cov={{ cookiecutter.project_slug }} --cov-report=html

# ===== Code Quality =====

# Run all linters
lint:
	@echo "\n\033[1mRunning linters...\033[0m"
	@echo "\n\033[1mBlack:\033[0m"
	black --check {{ cookiecutter.project_slug }} tests || (echo "\nRun 'make format' to fix formatting issues" && exit 1)
	@echo "\n\033[1misort:\033[0m"
	isort --check-only {{ cookiecutter.project_slug }} tests || (echo "\nRun 'make format' to fix import ordering" && exit 1)
	@echo "\n\033[1mFlake8:\033[0m"
	flake8 {{ cookiecutter.project_slug }} tests
	@echo "\n\033[1mMypy:\033[0m"
	mypy {{ cookiecutter.project_slug }}

# Format code
format:
	@echo "\n\033[1mFormatting code...\033[0m"
	black {{ cookiecutter.project_slug }} tests
	isort {{ cookiecutter.project_slug }} tests

# ===== Documentation =====

docs:
	@echo "\n\033[1mBuilding documentation...\033[0m"
	$(MAKE) -C docs html

# ===== Maintenance =====

# Clean up build artifacts
clean:
	@echo "\n\033[1mCleaning up...\033[0m"
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage htmlcov/ .mypy_cache/
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type f -name '*.py[co]' -delete

# Build distribution
dist: clean
	@echo "\n\033[1mBuilding distribution...\033[0m"
	python -m build

# ===== API Specific =====

{% if cookiecutter.include_api == 'y' %}
# Run the development server
run:
	@echo "\n\033[1mStarting development server...\033[0m"
	uvicorn {{ cookiecutter.project_slug }}.api:app --reload

# Run database migrations
migrate:
	@echo "\n\033[1mRunning database migrations...\033[0m"
	alembic upgrade head

# Create a new migration
migration:
	if [ -z "${MESSAGE}" ]; then \
		echo "Error: MESSAGE variable not set. Usage: make migration MESSAGE='your message'" >&2; \
		exit 1; \
	fi
	@echo "\n\033[1mCreating new migration...\033[0m"
	alembic revision --autogenerate -m "${MESSAGE}"
{% endif %}
