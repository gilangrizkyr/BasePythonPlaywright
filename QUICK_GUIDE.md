"""
Quick guide untuk membuat page object dan test baru
"""

# ============================================
# 1. MEMBUAT PAGE OBJECT BARU
# ============================================

# File: src/pages/dashboard.py

"""
from src.base import BasePage
from src.locators import DashboardLocators

class DashboardPage(BasePage):
    '''Dashboard Page Object'''
    
    async def navigate_to_dashboard(self):
        '''Navigate ke dashboard page'''
        await self.goto(f"{settings.BASE_URL}/dashboard")
    
    async def get_stat_values(self):
        '''Get values dari semua stat cards'''
        cards = await self.page.query_selector_all(DashboardLocators.STAT_CARDS)
        values = []
        for card in cards:
            text = await card.text_content()
            values.append(text)
        return values
    
    async def export_data(self):
        '''Click export button'''
        await self.click(DashboardLocators.EXPORT_BUTTON)
        # Wait untuk file download jika perlu
        async with self.page.expect_download() as download:
            await self.click(DashboardLocators.EXPORT_BUTTON)
        return await download.value
"""

# ============================================
# 2. MENAMBAH LOCATORS BARU
# ============================================

# File: src/locators.py (add this class)

"""
class ProfilePageLocators:
    '''Locators untuk Profile Page'''
    PROFILE_NAME = '#profile-name'
    PROFILE_EMAIL = '#profile-email'
    EDIT_BUTTON = 'button[data-testid="edit-profile"]'
    SAVE_BUTTON = 'button[data-testid="save-profile"]'
    PROFILE_IMAGE = 'img.profile-avatar'
"""

# ============================================
# 3. MEMBUAT TEST FILE BARU
# ============================================

# File: tests/test_dashboard.py

"""
import pytest
from src.base import BaseTest
from src.pages.dashboard import DashboardPage
from config.settings import settings

class TestDashboard(BaseTest):
    '''Test suite untuk Dashboard functionality'''
    
    @pytest.fixture(autouse=True, scope="function")
    async def setup_test(self):
        '''Setup test'''
        self.page = await self.context.new_page()
        self.page.set_default_timeout(settings.TIMEOUT)
        yield
        await self.page.close()
    
    @pytest.mark.asyncio
    async def test_dashboard_loads(self):
        '''Test: Dashboard dapat diload'''
        dashboard = DashboardPage(self.page)
        await dashboard.navigate_to_dashboard()
        
        # Verifikasi dashboard title ada
        assert await dashboard.is_visible("h1:has-text('Dashboard')")
    
    @pytest.mark.asyncio
    async def test_stat_cards_visible(self):
        '''Test: Stat cards visible di dashboard'''
        dashboard = DashboardPage(self.page)
        await dashboard.navigate_to_dashboard()
        
        # Get stat values
        values = await dashboard.get_stat_values()
        assert len(values) > 0
    
    @pytest.mark.asyncio
    async def test_export_data(self):
        '''Test: Export data functionality'''
        dashboard = DashboardPage(self.page)
        await dashboard.navigate_to_dashboard()
        
        # Export data
        download = await dashboard.export_data()
        assert download is not None
"""

# ============================================
# 4. MENGGUNAKAN UTILITIES
# ============================================

"""
from src.utils import WaitUtils, FileUtils, StringUtils

# Wait untuk condition
async def wait_for_text():
    result = await WaitUtils.wait_for_condition(
        lambda: self.page.text_content("h1") == "Expected Text",
        timeout=5000
    )
    assert result, "Text tidak ditemukan dalam timeout"

# Save JSON data
def save_test_data():
    data = {"test": "data", "status": "passed"}
    FileUtils.save_json(data, "reports/test_data.json")

# Normalize text
def check_text():
    text = "  Hello  World  "
    normalized = StringUtils.normalize_text(text)
    assert normalized == "hello world"
"""

# ============================================
# 5. MENJALANKAN TEST
# ============================================

"""
# Terminal commands:

# Run semua tests
pytest

# Run specific file
pytest tests/test_dashboard.py

# Run specific test
pytest tests/test_dashboard.py::TestDashboard::test_dashboard_loads

# Run dengan verbose
pytest -v

# Run dengan markers
pytest -m "slow"

# Generate report
pytest --html=reports/report.html --self-contained-html

# Run dengan screenshot on failure
pytest --screenshot=only-on-failure
"""

# ============================================
# 6. PYTEST MARKERS
# ============================================

"""
# Add ke test untuk organization

@pytest.mark.slow
async def test_something_slow():
    pass

@pytest.mark.smoke
async def test_critical_functionality():
    pass

# Run dengan marker:
pytest -m "smoke"
pytest -m "not slow"
"""

# ============================================
# 7. FIXTURES UNTUK REUSABLE CODE
# ============================================

"""
# File: tests/conftest.py (add this)

@pytest.fixture
async def login_user(page):
    '''Fixture untuk login user'''
    from src.pages.login import LoginPage
    login_page = LoginPage(page)
    await login_page.goto(f"{settings.BASE_URL}/login")
    await login_page.login("testuser", "password123")
    yield page
    # Cleanup if needed

# Usage dalam test:
@pytest.mark.asyncio
async def test_with_logged_in_user(login_user):
    page = login_user
    # Test code here
    pass
"""

print("Lihat dokumentasi lengkap di README.md")
