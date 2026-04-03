# 🚀 CARA MENGGUNAKAN FRAMEWORK PLAYWRIGHT

Panduan lengkap untuk menggunakan Professional Playwright Automation Framework.

## 📋 DAFTAR ISI

1. [Quick Start (3 Menit)](#quick-start)
2. [Setup Framework](#setup-framework)
3. [Menjalankan Tests](#menjalankan-tests)
4. [Membuat Test Baru](#membuat-test-baru)
5. [Menggunakan Page Objects](#menggunakan-page-objects)
6. [Advanced Features](#advanced-features)
7. [Troubleshooting](#troubleshooting)

---

## ⚡ QUICK START (3 Menit)

### Langkah 1: Setup Otomatis
```bash
cd /home/Gilang/DPMPTSP/Playwright

# Jalankan quick-start script
./quick-start.sh run-tests

# Atau gunakan Makefile
make setup
```

### Langkah 2: Verifikasi Framework Berfungsi
```bash
python -c "from core.config import config; print('✅ Framework Working!')"
```

### Langkah 3: Jalankan Contoh Test
```bash
# Run semua tests
./quick-start.sh run-tests-verbose

# Atau
python run_tests.py --help
pytest tests/test_example.py -v
```

---

## 🔧 SETUP FRAMEWORK

### Opsi 1: Quick Start Script (REKOMENDASI)
```bash
./quick-start.sh
```

Pilihan:
- `run-tests` - Jalankan semua test
- `run-tests-verbose` - Jalankan dengan output detail
- `run-single tests/file.py` - Jalankan test tertentu
- `generate-report` - Buat HTML report
- `list-tests` - Lihat semua tests

### Opsi 2: Menggunakan Makefile
```bash
# Install dependencies
make install

# Setup lengkap
make setup

# Jalankan tests
make test

# Lihat semua commands
make help
```

### Opsi 3: Manual Setup
```bash
# 1. Buat virtual environment
python3 -m venv venv

# 2. Activate environment
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Playwright browsers
playwright install

# 5. Setup environment variables
cp .env.example .env
# Edit .env dengan settings Anda
```

---

## 🧪 MENJALANKAN TESTS

### 1. Jalankan Semua Tests
```bash
# Dengan default settings
pytest tests/

# Dengan verbose output
pytest tests/ -v

# Dengan HTML report
pytest tests/ --html=reports/report.html

# Parallel execution
pytest tests/ -n auto
```

### 2. Jalankan Test Spesifik
```bash
# Test file tertentu
pytest tests/test_example.py

# Test class tertentu
pytest tests/test_example.py::TestNavigation

# Test method tertentu
pytest tests/test_example.py::TestNavigation::test_navigate_to_base_url
```

### 3. Jalankan Dengan Markers (Tags)
```bash
# Smoke tests (cepat)
pytest -m smoke

# Regression tests
pytest -m regression

# End-to-end tests
pytest -m e2e

# API tests
pytest -m api

# UI tests
pytest -m ui
```

### 4. Menggunakan CLI Runner
```bash
# Jalankan dengan custom options
python run_tests.py --browser firefox --headed --performance

# Lihat semua options
python run_tests.py --help

# Generate reports
python run_tests.py --generate-reports

# Run tests in parallel
python run_tests.py --parallel 4
```

### 5. With Different Browsers
```bash
# Chrome/Chromium
pytest tests/ --browser chromium

# Firefox
pytest tests/ --browser firefox

# Safari
pytest tests/ --browser webkit
```

### 6. Enable Features
```bash
# Enable performance monitoring
pytest tests/ --performance

# Enable accessibility testing
pytest tests/ --accessibility

# Enable security scanning
pytest tests/ --security

# Enable visual regression
pytest tests/ --visual
```

---

## 🎯 MEMBUAT TEST BARU

### Template Test Dasar
```python
# tests/test_login.py
import pytest
from pages.login_page import LoginPage
from core.config import config

class TestLogin:
    """Test suite untuk login functionality"""
    
    @pytest.mark.asyncio
    async def test_successful_login(self, page):
        """Test: Successful user login"""
        # Arrange - Setup
        login_page = LoginPage(page)
        
        # Act - Execute
        await login_page.navigate()
        await login_page.login("user@example.com", "password123")
        
        # Assert - Verify
        assert page.url == f"{config.base_url}/dashboard"
        print("✅ Login test passed")
    
    @pytest.mark.asyncio
    async def test_invalid_login(self, page):
        """Test: Invalid credentials"""
        login_page = LoginPage(page)
        
        await login_page.navigate()
        await login_page.login("user@example.com", "wrong_password")
        
        error_message = await login_page.get_error_message()
        assert "Invalid credentials" in error_message
```

### Template Dengan Markers
```python
import pytest
from pages.login_page import LoginPage

class TestLogin:
    
    @pytest.mark.smoke    # Smoke test
    @pytest.mark.asyncio
    async def test_login_smoke(self, page):
        """Quick smoke test"""
        pass
    
    @pytest.mark.regression  # Regression test
    @pytest.mark.asyncio
    async def test_login_regression(self, page):
        """Full regression test"""
        pass
    
    @pytest.mark.e2e  # End-to-end test
    @pytest.mark.asyncio
    async def test_login_e2e(self, page):
        """Full user journey"""
        pass
    
    @pytest.mark.slow  # Slow test
    @pytest.mark.asyncio
    async def test_login_slow(self, page):
        """Takes longer time"""
        pass
```

### Dengan Decorators
```python
from decorators import retry_on_failure, screenshot_on_failure, step

class TestLogin:
    
    @retry_on_failure(max_retries=3)  # Retry 3 times if fails
    @screenshot_on_failure  # Screenshot on failure
    @pytest.mark.asyncio
    async def test_login_with_retry(self, page):
        """Test dengan retry dan screenshot on failure"""
        pass
    
    @step("Navigate to login page")  # Step logging
    @pytest.mark.asyncio
    async def test_with_steps(self, page):
        await page.goto("https://example.com/login")
```

---

## 📄 MENGGUNAKAN PAGE OBJECTS

### 1. Buat Page Object Class
```python
# pages/login_page.py
from core.base import BasePage

class LoginPage(BasePage):
    """Page Object untuk Login Page"""
    
    # Locators
    EMAIL_INPUT = "#email"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button:has-text('Login')"
    ERROR_MESSAGE = ".error-message"
    
    async def navigate(self):
        """Navigate to login page"""
        await self.goto("/login")
    
    async def login(self, email: str, password: str):
        """Perform login action"""
        await self.fill(self.EMAIL_INPUT, email)
        await self.fill(self.PASSWORD_INPUT, password)
        await self.click(self.LOGIN_BUTTON)
        await self.page.wait_for_load_state("networkidle")
    
    async def get_error_message(self) -> str:
        """Get error message"""
        return await self.get_text(self.ERROR_MESSAGE)
    
    async def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        return await self.is_visible(".dashboard")
```

### 2. Gunakan Page Object di Test
```python
# tests/test_login.py
from pages.login_page import LoginPage

class TestLogin:
    
    @pytest.mark.asyncio
    async def test_login(self, page):
        # Create page object
        login_page = LoginPage(page)
        
        # Use page object methods
        await login_page.navigate()
        await login_page.login("user@example.com", "password123")
        
        # Verify result
        is_logged_in = await login_page.is_logged_in()
        assert is_logged_in
```

### 3. Base Page Methods (Built-in)
```python
# Available methods in BasePage:
await page.goto(url)              # Navigate to URL
await page.click(selector)        # Click element
await page.fill(selector, text)   # Fill input
await page.get_text(selector)     # Get element text
await page.is_visible(selector)   # Check visibility
await page.is_enabled(selector)   # Check if enabled
await page.wait_for(selector)     # Wait for element
await page.take_screenshot(path)  # Take screenshot
await page.hover(selector)        # Hover element
await page.double_click(selector) # Double click
```

---

## 🎪 ADVANCED FEATURES

### 1. Test Data Generation
```python
from core.utils import data_generator

class TestRegistration:
    
    @pytest.mark.asyncio
    async def test_register_new_user(self, page):
        # Generate random test data
        user = data_generator.generate_user()
        
        # Use generated data
        register_page = RegisterPage(page)
        await register_page.navigate()
        await register_page.fill_form(
            email=user['email'],
            password=user['password'],
            name=user['name']
        )
        await register_page.submit()
```

### 2. API Testing
```python
from core.utils import APIUtilities

class TestAPI:
    
    @pytest.mark.asyncio
    async def test_api_request(self, api_client):
        # Make API request
        response = await api_client.get("/api/users/123")
        
        # Verify response
        assert response['status_code'] == 200
        assert response['data']['id'] == 123
```

### 3. Database Testing
```python
from core.utils import DatabaseUtilities

class TestDatabase:
    
    @pytest.mark.asyncio
    async def test_database_operations(self, db_connection):
        # Execute query
        result = await db_connection.query("SELECT * FROM users WHERE id = ?", [123])
        
        # Verify result
        assert len(result) > 0
```

### 4. Performance Monitoring
```python
from decorators import performance_monitor

class TestPerformance:
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_page_load_time(self, page):
        """Test page load performance"""
        start_time = time.time()
        await page.goto("https://example.com")
        load_time = time.time() - start_time
        
        # Assert load time < 3 seconds
        assert load_time < 3.0
        print(f"Page loaded in {load_time:.2f}s")
```

### 5. Multi-Browser Testing
```python
@pytest.mark.parametrize("browser", ["chromium", "firefox", "webkit"])
@pytest.mark.asyncio
async def test_cross_browser(page, browser):
    """Test same scenario on different browsers"""
    await page.goto("https://example.com")
    
    # Verify layout/functionality same on all browsers
    assert await page.is_visible("h1")
```

---

## 🔍 CONFIGURATION

### Edit Environment Variables
```bash
# Copy example file
cp .env.example .env

# Edit untuk project Anda
nano .env
# atau
code .env
```

### Key Configuration Options
```ini
# Browser settings
BROWSER_NAME=chromium
HEADLESS=true
SCREEN_WIDTH=1920
SCREEN_HEIGHT=1080

# Application settings
BASE_URL=https://example.com
TIMEOUT=30000

# Test settings
PARALLEL=4
RETRY_COUNT=3
HEADLESS_MODE=true

# Reporting
REPORT_FORMAT=html
SCREENSHOT_ON_FAILURE=true

# API settings
API_BASE_URL=https://api.example.com
API_TIMEOUT=10000

# Database settings
DB_HOST=localhost
DB_PORT=5432
DB_NAME=testdb
DB_USER=postgres
DB_PASSWORD=password
```

---

## 📊 VIEWING TEST REPORTS

### HTML Report
```bash
# Open HTML report
open reports/report.html  # Mac
xdg-open reports/report.html  # Linux
start reports/report.html  # Windows
```

### JSON Report
```bash
pytest tests/ --json=reports/report.json
```

### JUnit Report
```bash
pytest tests/ --junit-xml=reports/junit.xml
```

### Allure Report
```bash
pytest tests/ --allure-dir=allure-results
allure serve allure-results
```

---

## 🐳 DOCKER USAGE

### Build Docker Image
```bash
docker build -t playwright-framework .
```

### Run Tests in Docker
```bash
docker run -v $(pwd)/reports:/app/reports playwright-framework pytest tests/
```

### Using Docker Compose
```bash
# Start services
docker-compose up -d

# Run tests
docker-compose exec playwright pytest tests/

# Stop services
docker-compose down
```

---

## 🛠️ TROUBLESHOOTING

### Issue: "ModuleNotFoundError"
```bash
# Solution: Install missing dependencies
pip install -r requirements.txt
playwright install
```

### Issue: "Timeout error"
```bash
# Increase timeout in .env
TIMEOUT=60000  # 60 seconds instead of 30

# Or in code
page.set_default_timeout(60000)
```

### Issue: "Element not found"
```python
# Wait for element
await page.wait_for_selector("#element-id", timeout=5000)

# Or use implicit wait
await page.wait_for_load_state("networkidle")
```

### Issue: Browser won't launch
```bash
# Install browser dependencies
playwright install-deps

# Or run with sudo
sudo playwright install-deps
```

### Issue: Permission denied on Linux
```bash
# Make script executable
chmod +x quick-start.sh
chmod +x setup.py
```

---

## 💡 BEST PRACTICES

### 1. Use Page Objects
✅ DO:
```python
login_page = LoginPage(page)
await login_page.login("user@example.com", "password")
```

❌ DON'T:
```python
await page.fill("#email", "user@example.com")
await page.fill("#password", "password")
await page.click("button")
```

### 2. Use Test Markers
✅ DO:
```python
@pytest.mark.smoke
@pytest.mark.asyncio
async def test_basic_flow(self, page):
    pass
```

### 3. Use Fixtures
✅ DO:
```python
@pytest.mark.asyncio
async def test_with_fixture(self, page, test_data):
    await login_page.login(test_data['user']['email'])
```

### 4. Add Assertions with Messages
✅ DO:
```python
assert user_name == "John", f"Expected 'John', got '{user_name}'"
```

❌ DON'T:
```python
assert user_name == "John"
```

### 5. Handle Waits Properly
✅ DO:
```python
await page.wait_for_selector("#submit-button")
await page.click("#submit-button")
```

❌ DON'T:
```python
import time
time.sleep(5)  # Hard wait
```

---

## 📚 ADDITIONAL RESOURCES

- [Official Readme](README.md)
- [Installation Guide](INSTALLATION_SUMMARY.md)
- [Setup Complete Info](SETUP_COMPLETE.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)

---

## 🎓 NEXT STEPS

1. **Create Your First Test**
   - Copy template dari section "Membuat Test Baru"
   - Run dengan `pytest tests/test_my_test.py -v`

2. **Customize Configuration**
   - Edit `.env` untuk your application
   - Update `BASE_URL` dan credentials

3. **Learn Page Objects**
   - Create page objects untuk setiap page di aplikasi Anda
   - Reuse methods di multiple tests

4. **Setup CI/CD**
   - Copy GitHub Actions workflow dari `.github/workflows/`
   - Customize untuk project Anda

5. **Run Tests Regularly**
   - Run smoke tests setiap deploy
   - Run full regression seminggu
   - Monitor metrics dan trends

---

## 🆘 NEED HELP?

- Check Troubleshooting section
- Read CONTRIBUTING.md untuk contribution guidelines
- Create issue di GitHub dengan error details
- Check logs di `reports/` directory

---

**Happy Testing! 🎉**