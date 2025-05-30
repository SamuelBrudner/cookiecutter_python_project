# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yourusername/{{ cookiecutter.project_slug }}/HEAD?filepath=notebooks/config.ipynb)

## 🤔 When to Include the API?

When generating your project, you'll be asked whether to include API functionality. Here's guidance to help you decide:

### ✅ Include the API if:
- Your code will be imported and used by other Python projects
- You want to expose specific functions or classes for reuse
- You need a clean interface between different parts of your codebase
- You want to document the public interface of your package

### ❌ Skip the API if:
- You're writing a one-off script
- The code won't be imported by other projects
- You're creating a simple utility for personal use
- You're not sure if you'll need an API

### You can always add it later!
If you're unsure, it's safe to skip the API initially. You can always add it later by:
1. Creating a `api.py` module
2. Moving your public functions/classes there
3. Importing them in `__init__.py`

---

## 🚀 Features

- **Modern Python**: Uses Python {{ cookiecutter.python_version }} with type hints and async/await
- **FastAPI API**: {% if cookiecutter.include_api == 'y' %}Included{% else %}Not included{% endif %} - A modern, fast (high-performance), web framework for building APIs
- **SQLAlchemy**: Provides a powerful ORM layer for database interactions
- **Testing**: Pytest with plugins for better testing
- **Code Quality**: Pre-commit hooks with Black, isort, flake8, and mypy
- **Containerization**: {% if cookiecutter.use_docker == 'y' %}Dockerfile included{% else %}No Docker support{% endif %}
- **CI/CD**: {% if cookiecutter.use_ci != 'none' %}{{ cookiecutter.use_ci|capitalize }} workflow included{% else %}No CI/CD configured{% endif %}

## 🛠️ Installation

### Prerequisites

- Python {{ cookiecutter.python_version }} or higher
- [Poetry](https://python-poetry.org/) (recommended) or pip

### Using Poetry (recommended)

```bash
# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```

### Using pip

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

## 🚦 Usage

{% if cookiecutter.include_api == 'y' %}
### Running the API

```bash
uvicorn {{ cookiecutter.project_slug }}.api:app --reload
```

Then open your browser at http://localhost:8000/api/docs
{% endif %}

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Run linters and type checking
pre-commit run --all-files
```

## 🏗 Project Structure

```
{{ cookiecutter.project_slug }}/
├── .github/                    # GitHub workflows (if CI is enabled)
├── .pre-commit-config.yaml      # Pre-commit hooks configuration
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore file
├── pyproject.toml              # Project dependencies and metadata
├── README.md                   # This file
├── src/
│   └── {{ cookiecutter.project_slug }}/
│       ├── __init__.py         # Package initialization
│       ├── api/                # API endpoints and routes
│       ├── core/               # Core functionality
│       ├── db/                 # Database models and session
│       ├── models/             # Pydantic models
│       ├── schemas/            # Database schemas
│       └── utils/              # Utility functions
└── tests/                      # Test files
```

## 📝 License

This project is licensed under the {{ cookiecutter.open_source_license }} License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
