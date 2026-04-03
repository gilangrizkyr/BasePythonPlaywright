# Professional Playwright Automation Framework

A comprehensive, enterprise-grade Python Playwright automation framework with modern features, type safety, and production-ready capabilities.

## 🚀 Features

### Core Features
- **Advanced Base Classes**: Professional page object model with type-safe element interactions
- **Parallel Execution**: Run tests concurrently with configurable worker pools
- **Comprehensive Reporting**: HTML, JSON, JUnit XML, and Allure reports
- **CI/CD Integration**: Native support for GitHub Actions, GitLab CI, Jenkins
- **Performance Monitoring**: Built-in performance metrics and thresholds
- **Accessibility Testing**: WCAG compliance checking
- **Visual Regression**: Screenshot comparison and diff detection
- **Security Testing**: Basic security scans and vulnerability checks
- **API Testing**: REST/GraphQL/SOAP API testing capabilities
- **Database Testing**: PostgreSQL, MongoDB, Redis integration
- **Mobile Testing**: Appium integration for mobile automation
- **Cross-browser Support**: Chromium, Firefox, WebKit, Safari
- **Data-driven Testing**: CSV, JSON, Excel test data support
- **Advanced Decorators**: Retry, screenshot, performance, logging decorators

### Enterprise Features
- **Type Safety**: Full Pydantic configuration validation
- **Logging**: Structured logging with multiple levels and formats
- **Error Handling**: Comprehensive error handling and recovery
- **Notifications**: Slack, Teams, Email notifications
- **Cloud Integration**: AWS, Azure, GCP support
- **Docker Support**: Containerized execution
- **Monitoring**: Real-time test execution monitoring
- **Security**: Secure credential management

## 📋 Requirements

- Python 3.12+
- Playwright browsers (auto-installed)
- Dependencies listed in `requirements.txt`

## 🛠️ Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd playwright-framework
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Install Playwright browsers**:
```bash
playwright install
```

5. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## 📁 Project Structure

```
playwright-framework/
├── core/                          # Core framework modules
│   ├── __init__.py               # Framework constants and metadata
│   ├── base.py                   # Base classes (BaseTest, BasePage, BaseElement)
│   ├── config.py                 # Configuration management (Pydantic)
│   ├── runner.py                 # Advanced test runner
│   └── utils.py                  # Utility functions
├── decorators/                   # Test decorators
│   └── __init__.py              # Professional decorators
├── pages/                        # Page object classes
│   └── __init__.py              # Example page classes
├── tests/                        # Test files
│   └── test_examples.py         # Example test cases
├── config/                       # Configuration files
├── data/                         # Test data files
├── reports/                      # Test reports and screenshots
├── logs/                         # Log files
├── scripts/                      # Utility scripts
├── Dockerfile                   # Docker configuration
├── docker-compose.yml          # Docker Compose setup
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## ⚙️ Configuration

### Environment Variables (.env)

```bash
# Application Settings
BASE_URL=https://example.com
ENVIRONMENT=staging
HEADLESS=false

# Browser Configuration
BROWSER_NAME=chromium
BROWSER_SLOW_MO=100
TIMEOUT=30000

# Test Execution
PARALLEL_WORKERS=4
RETRY_MAX_ATTEMPTS=3
SCREENSHOT_ON_FAILURE=true
VIDEO_ON_FAILURE=false

# Reporting
REPORTS_DIR=reports
LOG_LEVEL=INFO

# API Configuration
API_BASE_URL=https://api.example.com
API_TIMEOUT=10000

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=testdb
DB_USER=testuser
DB_PASSWORD=testpass

# Notifications
SLACK_WEBHOOK=https://hooks.slack.com/...
EMAIL_SMTP=smtp.gmail.com
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-password

# Cloud Configuration
AWS_REGION=us-east-1
AZURE_SUBSCRIPTION_ID=your-subscription-id
GCP_PROJECT_ID=your-project-id
```

### Advanced Configuration

The framework uses Pydantic for type-safe configuration. See `core/config.py` for all available options.

## 📝 Writing Tests

### Basic Test Structure

```python
from core.base import BaseTest
from pages import LoginPage, DashboardPage

class TestLogin(BaseTest):
    async def run_test(self):
        # Navigate to login page
        login_page = await self.navigate_to_page(LoginPage)

        # Perform login
        await login_page.login("user@example.com", "password")

        # Verify dashboard
        dashboard_page = DashboardPage(self.page)
        assert await dashboard_page.is_loaded()
```

### Using Decorators

```python
from decorators import screenshot_on_failure, retry_on_failure, performance_monitor

class TestExample(BaseTest):
    @screenshot_on_failure
    @retry_on_failure(max_retries=3)
    @performance_monitor
    async def run_test(self):
        # Your test code here
        pass
```

### Data-driven Tests

```python
from decorators import data_driven

class TestDataDriven(BaseTest):
    @data_driven([
        {"input": "value1", "expected": "result1"},
        {"input": "value2", "expected": "result2"},
    ])
    async def run_test(self, test_data):
        # Test code using test_data
        pass
```

### Page Object Model

```python
from core.base import BasePage

class LoginPage(BasePage):
    def _init_elements(self):
        self.add_element("username", "#username")
        self.add_element("password", "#password")
        self.add_element("login_btn", "#login")

    async def login(self, username, password):
        await self.get_element("username").fill(username)
        await self.get_element("password").fill(password)
        await self.get_element("login_btn").click()
```

## 🚀 Running Tests

### Run All Tests

```bash
# Sequential execution
python -m pytest tests/

# Parallel execution
python -m pytest tests/ -n 4

# Using the advanced runner
python core/runner.py
```

### Run Specific Test

```bash
python -m pytest tests/test_login.py -v
```

### Run with Tags

```bash
python -m pytest tests/ -m "smoke"
```

### Run with Custom Configuration

```bash
python core/runner.py --config config/test_config.json
```

### Generate Reports

```bash
# HTML Report
python -m pytest tests/ --html=reports/html-report/index.html

# JUnit XML for CI/CD
python -m pytest tests/ --junitxml=reports/junit-xml/results.xml

# Allure Report
python -m pytest tests/ --alluredir=reports/allure-results
allure serve reports/allure-results
```

## 🔧 Advanced Features

### Parallel Execution

```python
from core.runner import TestSuiteConfig, AdvancedTestRunner

config = TestSuiteConfig(
    name="Parallel Test Suite",
    parallel_workers=4,
    browser="chromium"
)

runner = AdvancedTestRunner(config)
results = await runner.run_suite()
```

### Performance Monitoring

```python
from core.utils import performance_utils

@performance_utils.measure_execution_time
async def my_test_function():
    # Your test code
    pass

# Check thresholds
performance_utils.check_performance_threshold(
    actual_time, threshold, "page_load"
)
```

### API Testing

```python
from core.utils import APIUtilities

api = APIUtilities("https://api.example.com")

# Make requests
response = await api.get("/users/1")
assert response["status_code"] == 200

# POST request
data = {"name": "John", "email": "john@example.com"}
response = await api.post("/users", data)
```

### Database Testing

```python
from core.utils import DatabaseUtilities

db = DatabaseUtilities("postgresql://user:pass@localhost/db")

# Execute queries
users = await db.execute_query("SELECT * FROM users")
assert len(users) > 0
```

### Data Generation

```python
from core.utils import data_generator

# Generate test data
user = data_generator.generate_user()
product = data_generator.generate_product()
credit_card = data_generator.generate_credit_card()
```

## 📊 Reporting

### HTML Reports
- Interactive test results with screenshots
- Performance metrics visualization
- Timeline view of test execution
- Detailed error information

### JSON Reports
- Machine-readable test results
- Performance data export
- CI/CD integration data

### JUnit XML
- Standard CI/CD format
- Test management tool integration
- Historical trend analysis

### Allure Reports
- Beautiful, detailed reports
- Test step visualization
- Historical trends
- Attachment support

## 🔒 Security

### Credential Management
- Environment variables for sensitive data
- Secure credential storage
- No hardcoded secrets

### Security Testing
```python
from decorators import security_scan

class TestSecurity(BaseTest):
    @security_scan
    async def run_test(self):
        # Security test code
        pass
```

## 📱 Mobile Testing

```python
from core.config import config

# Configure for mobile
config.device.viewport = {"width": 375, "height": 667}
config.device.user_agent = "iPhone Safari"

# Use Appium for native mobile apps
# (Requires Appium server setup)
```

## ☁️ Cloud Integration

### AWS Device Farm
```python
# Configure AWS credentials
config.cloud.aws.region = "us-east-1"
config.cloud.aws.device_farm_project = "your-project"
```

### BrowserStack
```python
config.browser.remote_url = "https://hub-cloud.browserstack.com/wd/hub"
config.browser.capabilities = {
    "browserstack.user": "your-user",
    "browserstack.key": "your-key",
}
```

## 🐳 Docker Support

### Build Docker Image
```bash
docker build -t playwright-framework .
```

### Run Tests in Docker
```bash
docker run --rm -v $(pwd)/reports:/app/reports playwright-framework
```

### Docker Compose
```bash
docker-compose up test-runner
```

## 🔄 CI/CD Integration

### GitHub Actions
```yaml
name: Playwright Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: playwright install
      - run: python -m pytest tests/ --junitxml=reports/results.xml
      - uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: reports/
```

### GitLab CI
```yaml
stages:
  - test

playwright_tests:
  stage: test
  image: python:3.12
  before_script:
    - pip install -r requirements.txt
    - playwright install
  script:
    - python -m pytest tests/ --junitxml=reports/results.xml
  artifacts:
    reports:
      junit: reports/results.xml
    paths:
      - reports/
```

## 📈 Monitoring & Analytics

### Real-time Monitoring
- Test execution progress
- Performance metrics dashboard
- Failure rate tracking
- Resource usage monitoring

### Notifications
```python
# Slack notifications
config.notifications.slack_webhook = "https://hooks.slack.com/..."

# Email notifications
config.notifications.email_smtp = "smtp.gmail.com"
config.notifications.email_user = "your-email@gmail.com"
```

## 🛠️ Development

### Adding New Features
1. Create feature branch
2. Implement changes
3. Add tests
4. Update documentation
5. Create pull request

### Code Quality
```bash
# Run linting
flake8 core/ tests/

# Run type checking
mypy core/ tests/

# Run tests with coverage
pytest --cov=core --cov-report=html
```

### Contributing
1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## 📚 Examples

See `tests/test_examples.py` for comprehensive test examples including:
- Login functionality tests
- E2E checkout flow
- Performance monitoring
- Accessibility testing
- Visual regression
- API testing patterns

## 🐛 Troubleshooting

### Common Issues

1. **Browser not found**: Run `playwright install`
2. **Import errors**: Check virtual environment activation
3. **Timeout errors**: Increase timeout in configuration
4. **Screenshot failures**: Check write permissions on reports directory

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with verbose output
python -m pytest tests/ -v -s
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review example tests
- Join our community discussions

## 🎯 Roadmap

### Upcoming Features
- [ ] Advanced visual regression with pixel-perfect comparison
- [ ] Machine learning-based test failure prediction
- [ ] Integration with test management tools (TestRail, Zephyr)
- [ ] Advanced API testing with GraphQL support
- [ ] Mobile native app testing enhancements
- [ ] Performance profiling and optimization tools
- [ ] AI-powered test generation
- [ ] Advanced security testing modules

---

**Happy Testing! 🚀**

## Usage

### Membuat Test Baru

1. **Buat Page Object** (dalam `src/pages/` jika Anda membuat folder baru):
```python
from src.base import BasePage
from src.locators import LoginPageLocators

class LoginPage(BasePage):
    async def login(self, username: str, password: str):
        await self.fill(LoginPageLocators.USERNAME_INPUT, username)
        await self.fill(LoginPageLocators.PASSWORD_INPUT, password)
        await self.click(LoginPageLocators.LOGIN_BUTTON)
```

2. **Buat Test Case**:
```python
import pytest
from src.base import BaseTest

class TestLogin(BaseTest):
    @pytest.mark.asyncio
    async def test_login_success(self):
        # Your test code here
        pass
```

### Menjalankan Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_example.py

# Run dengan verbose
pytest -v

# Run dengan markers
pytest -m "slow"

# Generate HTML report
pytest --html=reports/report.html --self-contained-html
```

## Features

✅ **Async Support** - Menggunakan async/await untuk performa test yang lebih baik
✅ **Page Object Model** - Struktur yang clean dan maintainable
✅ **Base Classes** - BaseTest dan BasePage untuk kurangi code duplication
✅ **Configuration Management** - Settings management dengan .env
✅ **Screenshots & Videos** - Automatic screenshot dan video recording
✅ **Multiple Browsers** - Support Chromium, Firefox, WebKit
✅ **Pytest Integration** - Full pytest support dengan markers dan fixtures

## Configuration

Ubah settings di `.env` file:

- `HEADLESS` - Run browser dalam headless mode (true/false)
- `BROWSER_TYPE` - Pilih browser: chromium, firefox, webkit
- `TIMEOUT` - Default timeout dalam milliseconds
- `BASE_URL` - Base URL untuk aplikasi Anda
- `SCREENSHOT_ON_FAILURE` - Auto screenshot saat test gagal
- `RECORD_VIDEO` - Record video untuk setiap test

## Locators Management

Manage semua locators dalam file `src/locators.py`:

```python
class LoginPageLocators:
    USERNAME_INPUT = 'input[name="username"]'
    PASSWORD_INPUT = 'input[name="password"]'
    LOGIN_BUTTON = 'button:has-text("Login")'
```

## Tips & Best Practices

1. **Selalu gunakan async/await** dalam test methods
2. **Organize locators** dalam class terpisah
3. **Use Page Objects** untuk better maintainability
4. **Add waits** untuk handle timing issues
5. **Use fixtures** untuk setup dan cleanup
6. **Document your tests** dengan docstrings

## Troubleshooting

### Playwright Browser Install Error
```bash
playwright install --with-deps
```

### Timeout Issues
Increase `TIMEOUT` di `.env` file

### Import Errors
Pastikan Anda sudah activate virtual environment dan install requirements

## Resources

- [Playwright Python Documentation](https://playwright.dev/python/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Async/Await Python](https://docs.python.org/3/library/asyncio.html)

## License

MIT
# BasePythonPlaywright
