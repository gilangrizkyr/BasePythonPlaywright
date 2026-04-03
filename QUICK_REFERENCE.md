# 🎯 QUICK REFERENCE - PANDUAN SINGKAT

## 3️⃣ SETUP (3 Menit)

### Opsi Tercepat:
```bash
cd /home/Gilang/DPMPTSP/Playwright
./quick-start.sh run-tests
```

✅ Done! Framework sudah berfungsi


## ⚡ COMMAND PALING SERING DIGUNAKAN

### Jalankan Test
```bash
# Semua tests
pytest tests/ -v

# Test file tertentu  
pytest tests/test_login.py -v

# Test dengan marker
pytest -m smoke           # Run smoke tests only
pytest -m "not slow"      # Skip slow tests
pytest -m regression -v   # Verbose regression tests
```

### Quick Start Commands
```bash
./quick-start.sh run-tests              # Run all tests
./quick-start.sh run-tests-verbose      # With details
./quick-start.sh run-single tests/file  # Single test
./quick-start.sh list-tests             # Show all tests
```

### Makefile Commands
```bash
make install              # Install dependencies
make test                 # Run tests
make test-verbose         # Run with details  
make test-smoke           # Run smoke tests
make quality              # Run quality checks
make help                 # Show all commands
```


## 📝 BUAT TEST BARU (Copy-Paste Template)

### Minimal Test Template:
```python
# tests/test_my_test.py
import pytest
from core.config import config

class TestMyFeature:
    
    @pytest.mark.asyncio
    async def test_simple(self, page):
        """Your test description"""
        # Navigate
        await page.goto(config.base_url)
        
        # Verify
        assert page.url == config.base_url
        print("✅ Test passed")
```

### Run Test:
```bash
pytest tests/test_my_test.py -v
```


## 📄 GUNAKAN PAGE OBJECT (Best Practice)

### 1. Buat Page Object:
```python
# pages/my_page.py
from core.base import BasePage

class MyPage(BasePage):
    
    TITLE = "h1"
    
    async def navigate(self):
        await self.goto("/my-page")
    
    async def get_title(self):
        return await self.get_text(self.TITLE)
```

### 2. Gunakan di Test:
```python
from pages.my_page import MyPage

class TestMyPage:
    
    @pytest.mark.asyncio
    async def test_title(self, page):
        my_page = MyPage(page)
        await my_page.navigate()
        title = await my_page.get_title()
        assert title == "Welcome"
```


## 🔄 AVAILABLE FIXTURES

```python
async def test_example(self,
    page,                    # Playwright page object
    test_data,              # Auto-generated test data
    api_client,             # API testing client
    db_connection,          # Database connection
    test_data_manager,      # Manage test data
):
    pass
```


## 📊 CHECK REPORTS

```bash
# After running tests
open reports/report.html          # View HTML report
open reports/screenshots/         # View screenshots
```


## 🌐 TEST DENGAN BROWSER BERBEDA

```bash
# Chrome
pytest tests/ --browser chromium

# Firefox
pytest tests/ --browser firefox

# Safari
pytest tests/ --browser webkit

# Parallel (4 browsers at once - faster!)
pytest tests/ -n 4
```


## 🎯 MARKERS (Filter Tests By Type)

```python
@pytest.mark.smoke               # Quick tests
@pytest.mark.regression          # Full tests
@pytest.mark.e2e                 # End-to-end
@pytest.mark.api                 # API only
@pytest.mark.ui                  # UI only
@pytest.mark.slow                # Takes long time
@pytest.mark.flaky               # Might fail sometimes
```

Run specific tests:
```bash
pytest -m smoke              # Only smoke tests
pytest -m "not slow"         # Skip slow tests
pytest -m "smoke and not ui" # Smart filtering
```


## 🔧 CONFIGURE APPLICATION

```bash
# Edit environment config
nano .env

# Key settings:
BASE_URL=https://example.com
BROWSER_NAME=chromium
HEADLESS=true
TIMEOUT=30000
```


## 💡 USEFUL BASE PAGE METHODS

```python
# Navigation
await page.goto(url)
await page.back()
await page.forward()

# Interaction
await page.click(selector)
await page.fill(selector, text)
await page.type(selector, text)
await page.press(selector, key)

# Wait
await page.wait_for_selector(selector)
await page.wait_for_load_state("networkidle")

# Get Data
text = await page.get_text(selector)
count = await page.locator(selector).count()
visible = await page.is_visible(selector)

# Screenshot
await page.take_screenshot(path)
```


## ⚙️ HELPFUL OPTIONS

```bash
# Verbose output
pytest tests/ -v --tb=short

# Stop on first failure
pytest tests/ -x

# Show print statements
pytest tests/ -s

# Generate HTML report
pytest tests/ --html=report.html

# Parallel execution (faster!)
pytest tests/ -n auto

# Specific test by keyword
pytest tests/ -k "keyword" 

# Show test duration
pytest tests/ --durations=10
```


## 🆘 COMMON ISSUES

| Issue | Solution |
|-------|----------|
| ModuleNotFoundError | `pip install -r requirements.txt` |
| Import Error | Check `.env` BASE_URL is correct |
| Timeout Error | Increase TIMEOUT in `.env` |
| Element not found | Use `page.wait_for_selector()` |
| Permission denied | `chmod +x quick-start.sh` |


## 📚 FILE LOCATIONS

```
/home/Gilang/DPMPTSP/Playwright/
├── tests/                 # Your test files
│   ├── test_example.py   # Example tests
│   └── conftest.py       # Fixtures & config
├── pages/                # Page objects
│   └── login_page.py
├── core/                 # Framework core
│   ├── config.py         # Configuration
│   ├── base.py          # Base classes
│   └── utils.py         # Utilities
├── reports/             # Test results
│   ├── report.html     # HTML report
│   └── screenshots/    # Failure screenshots
├── .env                # Environment config
├── pytest.ini          # Pytest config
└── README.md           # Full documentation
```


## 🚀 WORKFLOW EXAMPLE

### Step 1: Setup 
```bash
./quick-start.sh run-tests
```

### Step 2: Create Test
```bash
# Create tests/test_login.py
# Copy from template above
```

### Step 3: Run Test
```bash
pytest tests/test_login.py -v
```

### Step 4: Check Results
```bash
open reports/report.html
```

### Step 5: Fix Issues
```bash
# Edit test file
# Re-run: pytest tests/test_login.py -v
```


## 🎯 NEXT STEPS

1. ✅ Run `./quick-start.sh run-tests` 
2. ✅ Create own test file
3. ✅ Update `.env` with your app URL
4. ✅ Run tests regularly
5. ✅ Monitor reports


---

**💡 Pro Tips:**
- Use `pytest -m smoke -v --tb=short` for fast feedback
- Add `@pytest.mark.slow` untuk long-running tests
- Check `reports/` folder after each run
- Use Page Objects untuk maintainability
- Run tests in parallel dengan `-n auto` untuk faster builds

---

**Got Questions?** Check USAGE_GUIDE.md for full documentation!
