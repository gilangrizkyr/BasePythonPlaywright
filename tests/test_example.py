"""Example tests with Playwright"""
import pytest
from core.base import BaseTest, BasePage
from core.config import config


class TestNavigation:
    """Test suite untuk Navigation"""

    @pytest.mark.asyncio
    async def test_navigate_to_base_url(self, page):
        """Test: Navigate ke base URL dan verify page loaded"""
        try:
            # Navigate
            await page.goto(config.base_url)

            # Verify page berhasil loaded
            title = await page.title()
            assert title is not None
            assert page.url

            print(f"✅ Successfully navigated to {config.base_url}")
        except Exception as e:
            print(f"❌ Navigation failed: {e}")
            raise
    
    @pytest.mark.asyncio
    async def test_page_object_navigation(self, page):
        """Test: Menggunakan BasePage untuk navigation"""
        try:
            base_page = BasePage(page)
            await base_page.goto(config.base_url)

            # Verify page loaded
            assert page.url == config.base_url

            print("✅ Page Object navigation successful")
        except Exception as e:
            print(f"❌ Page Object navigation failed: {e}")
            raise


class TestBasePage:
    """Test suite untuk BasePage functionality"""

    @pytest.mark.asyncio
    async def test_basepage_methods(self, page):
        """Test: Basic BasePage methods"""
        try:
            base_page = BasePage(page)

            # Navigate dan verify methods exist
            assert hasattr(base_page, 'goto')
            assert hasattr(base_page, 'click')
            assert hasattr(base_page, 'fill')
            assert hasattr(base_page, 'get_text')
            assert hasattr(base_page, 'is_visible')

            print("✅ BasePage has all required methods")
        except Exception as e:
            print(f"❌ BasePage test failed: {e}")
            raise


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


