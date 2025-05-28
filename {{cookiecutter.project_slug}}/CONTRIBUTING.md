# Contributing to {{ cookiecutter.project_name }}

Thank you for your interest in contributing to {{ cookiecutter.project_name }}! We welcome contributions from the community.

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally
3. **Install** the development dependencies:
   ```bash
   make install
   ```
4. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

1. **Run tests** to ensure everything is working:
   ```bash
   make test
   ```

2. **Make your changes** and ensure tests pass

3. **Format your code** before committing:
   ```bash
   make format
   ```

4. **Run linters** to catch any issues:
   ```bash
   make lint
   ```

5. **Commit your changes** with a descriptive message:
   ```bash
   git commit -m "Add feature: your feature description"
   ```

6. **Push** to your fork and open a pull request

## Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints for all function signatures
- Include docstrings for all public functions and classes
- Keep functions small and focused on a single responsibility
- Write tests for new functionality

## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a build.
2. Update the README.md with details of changes to the interface, including new environment variables, exposed ports, useful file locations, and container parameters.
3. Increase the version numbers in any examples files and the README.md to the new version that this Pull Request would represent.
4. Your pull request will be reviewed by the maintainers, who may request changes.

## Reporting Issues

When reporting issues, please include:

- A clear description of the issue
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Any relevant error messages
- Your environment (OS, Python version, etc.)
