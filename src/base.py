"""Base class untuk Playwright automation"""
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from config.settings import settings
import asyncio
from typing import Optional
import os
from datetime import datetime


class BasePage:
    """Base class untuk semua page objects"""
    
    def __init__(self, page: Page):
        self.page = page
        self.timeout = settings.TIMEOUT
    
    async def goto(self, url: str):
        """Navigate ke URL"""
        await self.page.goto(url, wait_until="networkidle")
    
    async def click(self, selector: str):
        """Click element dengan selector"""
        await self.page.click(selector)
    
    async def fill(self, selector: str, text: str):
        """Fill input field"""
        await self.page.fill(selector, text)
    
    async def get_text(self, selector: str) -> str:
        """Get text dari element"""
        return await self.page.text_content(selector)
    
    async def is_visible(self, selector: str) -> bool:
        """Check jika element visible"""
        try:
            await self.page.wait_for_selector(selector, timeout=2000, state="visible")
            return True
        except:
            return False
    
    async def wait_for_element(self, selector: str, timeout: Optional[int] = None):
        """Wait untuk element muncul"""
        await self.page.wait_for_selector(selector, timeout=timeout or self.timeout)
    
    async def take_screenshot(self, name: str):
        """Take screenshot"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{settings.SCREENSHOTS_PATH}/{name}_{timestamp}.png"
        os.makedirs(settings.SCREENSHOTS_PATH, exist_ok=True)
        await self.page.screenshot(path=filename)
        return filename


class BaseTest:
    """Base class untuk test automation - gunakan dengan pytest"""
    
    _playwright = None
    _browser: Optional[Browser] = None
    _context: Optional[BrowserContext] = None
    
    @property
    def browser(self) -> Optional[Browser]:
        """Get browser instance"""
        return self.__class__._browser
    
    @property
    def context(self) -> Optional[BrowserContext]:
        """Get context instance"""
        return self.__class__._context
    
    @classmethod
    async def _init_browser(cls):
        """Initialize browser untuk test class"""
        if cls._browser is not None:
            return  # Sudah diinit
        
        settings.create_directories()
        
        # Start playwright
        cls._playwright = await async_playwright().start()
        
        # Launch browser
        if settings.BROWSER_TYPE == "firefox":
            cls._browser = await cls._playwright.firefox.launch(headless=settings.HEADLESS)
        elif settings.BROWSER_TYPE == "webkit":
            cls._browser = await cls._playwright.webkit.launch(headless=settings.HEADLESS)
        else:  # chromium (default)
            cls._browser = await cls._playwright.chromium.launch(headless=settings.HEADLESS)
        
        # Create context
        context_options = {
            "accept_downloads": True,
        }
        
        if settings.RECORD_VIDEO:
            context_options["record_video_dir"] = settings.VIDEOS_PATH
        
        cls._context = await cls._browser.new_context(**context_options)
    
    @classmethod
    async def _cleanup_browser(cls):
        """Cleanup browser resources"""
        if cls._context:
            await cls._context.close()
            cls._context = None
        
        if cls._browser:
            await cls._browser.close()
            cls._browser = None
        
        if cls._playwright:
            await cls._playwright.stop()
            cls._playwright = None


