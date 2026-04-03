# Contributing to Professional Playwright Automation Framework

Thank you for your interest in contributing to the Professional Playwright Automation Framework! We welcome contributions from the community and are grateful for your help in making this framework better.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Development Guidelines](#development-guidelines)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Community](#community)

## Code of Conduct

This project adheres to a code of conduct to ensure a welcoming environment for all contributors. By participating, you agree to:

- Be respectful and inclusive
- Focus on constructive feedback
- Accept responsibility for mistakes
- Show empathy towards other contributors
- Help create a positive community

## Getting Started

### Prerequisites

Before you begin, ensure you have:

- Python 3.8 or higher
- Git
- Virtual environment tool (venv, virtualenv, conda, etc.)
- Node.js (for some development tools)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/playwright-automation-framework.git
   cd playwright-automation-framework
   ```

3. Set up the upstream remote:
   ```bash
   git remote add upstream https://github.com/company/playwright-automation-framework.git
   ```

## Development Setup

### Automated Setup

Use the provided setup script:

```bash
# Linux/Mac
./quick-start.sh

# Windows
python setup.py
```

### Manual Setup

1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .[dev]  # Install with development dependencies
   ```

3. Install Playwright browsers:
   ```bash
   playwright install
   ```

4. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

5. Copy environment configuration:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **Bug fixes**: Fix issues in the codebase
- **Features**: Add new functionality
- **Documentation**: Improve documentation and examples
- **Tests**: Add or improve test coverage
- **Code review**: Review pull requests
- **Issue triage**: Help manage and organize issues

### Finding Issues

- Check the [issue tracker](https://github.com/company/playwright-automation-framework/issues) for open issues
- Look for issues labeled `good first issue` or `help wanted`
- Comment on issues to indicate you're working on them

### Development Workflow

1. **Choose an issue**: Find or create an issue to work on
2. **Create a branch**: Use a descriptive branch name
   ```bash
   git checkout -b feature/add-new-decorator
   # or
   git checkout -b fix/browser-initialization-bug
   # or
   git checkout -b docs/improve-api-documentation
   ```

3. **Make changes**: Implement your changes following the guidelines below
4. **Test your changes**: Run tests and ensure everything works
5. **Update documentation**: Update docs if needed
6. **Commit changes**: Write clear, concise commit messages
7. **Push and create PR**: Push your branch and create a pull request

## Development Guidelines

### Code Style

This project uses several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **Flake8**: Linting
- **MyPy**: Type checking

Run all quality checks:

```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .

# Type check
mypy .

# Run all checks
make quality
```

### Commit Messages

Follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Testing
- `chore`: Maintenance

Examples:
```
feat(decorators): add retry_on_failure decorator
fix(config): resolve browser initialization timeout
docs(readme): update installation instructions
```

### Naming Conventions

- **Classes**: PascalCase (e.g., `BaseTest`, `LoginPage`)
- **Functions/Methods**: snake_case (e.g., `setup_browser`, `take_screenshot`)
- **Constants**: UPPER_CASE (e.g., `DEFAULT_TIMEOUT`, `BROWSER_CONFIG`)
- **Variables**: snake_case (e.g., `page_title`, `user_credentials`)

### Async/Await Guidelines

- Use async/await for all Playwright operations
- Name async functions with `_async` suffix when needed for clarity
- Use `asyncio.gather()` for concurrent operations
- Handle exceptions properly in async contexts

### Error Handling

- Use specific exception types
- Provide meaningful error messages
- Log errors appropriately
- Don't expose sensitive information in error messages

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_examples.py

# Run with coverage
pytest --cov=core --cov-report=html

# Run specific test markers
pytest -m smoke
pytest -m "not slow"

# Run in parallel
pytest -n auto

# Run with different browser
pytest --browser firefox
```

### Writing Tests

- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)
- Use fixtures for setup/teardown
- Mock external dependencies
- Test both positive and negative scenarios
- Add appropriate markers

Example:
```python
@pytest.mark.asyncio
@pytest.mark.ui
async def test_login_successful(page, test_data):
    """Test successful user login"""
    # Arrange
    login_page = LoginPage(page)
    user = test_data["user"]

    # Act
    await login_page.navigate()
    await login_page.login(user["email"], user["password"])

    # Assert
    await expect(page).to_have_url("**/dashboard")
    await expect(page.locator(".welcome-message")).to_contain_text(user["name"])
```

### Test Coverage

Maintain high test coverage:

- Aim for >80% overall coverage
- Cover all critical paths
- Test error conditions
- Include integration tests

## Documentation

### Types of Documentation

- **Code comments**: Explain complex logic
- **Docstrings**: Document all public functions/classes
- **README**: Project overview and setup
- **Examples**: Usage examples and tutorials
- **API docs**: Generated from docstrings

### Documentation Standards

Use Google-style docstrings:

```python
def login(self, email: str, password: str) -> None:
    """Log in a user with email and password.

    Args:
        email: User's email address
        password: User's password

    Raises:
        LoginError: If login fails
        TimeoutError: If login takes too long

    Example:
        >>> page = LoginPage(browser_page)
        >>> await page.login("user@example.com", "password123")
    """
```

### Updating Documentation

- Update README for new features
- Add examples for new functionality
- Keep API documentation current
- Update changelog for changes

## Pull Request Process

### Before Submitting

1. **Update your branch**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run all checks**:
   ```bash
   make quality
   make test
   ```

3. **Update CHANGELOG.md** if needed

4. **Write tests** for new functionality

### Creating a Pull Request

1. **Push your branch**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create PR on GitHub**:
   - Use descriptive title
   - Fill out PR template
   - Reference related issues
   - Add screenshots/videos if UI changes

3. **PR Template**:
   - Description of changes
   - Type of change (bug fix, feature, etc.)
   - Testing done
   - Breaking changes (if any)
   - Screenshots (if applicable)

### After Submitting

- Respond to reviewer comments promptly
- Make requested changes
- Keep PR updated with main branch
- Close related issues when merged

## Community

### Getting Help

- **Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Discord/Slack**: For real-time chat (if available)

### Recognition

Contributors are recognized in:
- CHANGELOG.md for significant contributions
- GitHub contributors list
- Release notes

### Code Review Guidelines

When reviewing PRs:

- Be constructive and respectful
- Focus on code quality and functionality
- Suggest improvements, don't demand changes
- Test the changes when possible
- Approve when requirements are met

## Additional Resources

- [Framework Documentation](https://playwright-framework.readthedocs.io/)
- [Playwright Documentation](https://playwright.dev/python/docs/intro)
- [Pytest Documentation](https://docs.pytest.org/)
- [Python Best Practices](https://python-best-practices.readthedocs.io/)

Thank you for contributing to the Professional Playwright Automation Framework! 🚀