"""
Professional Base Classes
========================

Advanced base classes for Playwright automation with modern features,
type safety, and enterprise-grade capabilities.
"""

import asyncio
import time
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union, Any, Callable, TypeVar, Generic
from pathlib import Path
from dataclasses import dataclass, field
from contextlib import asynccontextmanager
from playwright.async_api import Page, Browser, BrowserContext, Locator, ElementHandle
from loguru import logger

from core.config import config
from decorators import (
    screenshot_on_failure,
    retry_on_failure,
    performance_monitor,
    log_test_execution,
    step,
)


T = TypeVar('T')


@dataclass
class TestResult:
    """Test result data class"""
    test_name: str
    status: str  # "passed", "failed", "skipped", "error"
    duration: float
    error_message: Optional[str] = None
    screenshot_path: Optional[str] = None
    video_path: Optional[str] = None
    performance_metrics: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PageElement:
    """Page element representation"""
    name: str
    locator: str
    description: str = ""
    timeout: Optional[int] = None
    visible_timeout: int = 5000
    retry_attempts: int = 3


@dataclass
class PerformanceMetrics:
    """Performance metrics data class"""
    page_load_time: float = 0.0
    dom_content_loaded: float = 0.0
    first_paint: float = 0.0
    first_contentful_paint: float = 0.0
    largest_contentful_paint: float = 0.0
    cumulative_layout_shift: float = 0.0
    first_input_delay: float = 0.0
    memory_usage: float = 0.0
    cpu_usage: float = 0.0


class BaseElement:
    """Base class for page elements with advanced interactions"""

    def __init__(self, page: Page, locator: str, name: str = "", timeout: Optional[int] = None):
        self.page = page
        self.locator = locator
        self.name = name or locator
        self.timeout = timeout or config.timeout
        self._element: Optional[Locator] = None

    async def get_locator(self) -> Locator:
        """Get Playwright locator"""
        if self._element is None:
            self._element = self.page.locator(self.locator)
        return self._element

    @retry_on_failure(max_retries=3)
    async def click(self, **kwargs) -> None:
        """Click element with retry"""
        locator = await self.get_locator()
        await locator.click(timeout=self.timeout, **kwargs)
        logger.debug(f"Clicked element: {self.name}")

    @retry_on_failure(max_retries=3)
    async def fill(self, text: str, **kwargs) -> None:
        """Fill element with text"""
        locator = await self.get_locator()
        await locator.fill(text, timeout=self.timeout, **kwargs)
        logger.debug(f"Filled element '{self.name}' with text: {text[:50]}...")

    async def type_text(self, text: str, delay: int = 100, **kwargs) -> None:
        """Type text with delay (simulate human typing)"""
        locator = await self.get_locator()
        await locator.type(text, delay=delay, timeout=self.timeout, **kwargs)
        logger.debug(f"Typed text in element '{self.name}': {text[:50]}...")

    async def get_text(self) -> str:
        """Get element text content"""
        locator = await self.get_locator()
        text = await locator.text_content(timeout=self.timeout)
        return text or ""

    async def get_attribute(self, name: str) -> Optional[str]:
        """Get element attribute"""
        locator = await self.get_locator()
        return await locator.get_attribute(name, timeout=self.timeout)

    async def is_visible(self) -> bool:
        """Check if element is visible"""
        try:
            locator = await self.get_locator()
            return await locator.is_visible(timeout=self.timeout)
        except:
            return False

    async def is_hidden(self) -> bool:
        """Check if element is hidden"""
        try:
            locator = await self.get_locator()
            return await locator.is_hidden(timeout=self.timeout)
        except:
            return True

    async def wait_for_visible(self, timeout: Optional[int] = None) -> None:
        """Wait for element to be visible"""
        locator = await self.get_locator()
        await locator.wait_for(state="visible", timeout=timeout or self.timeout)

    async def wait_for_hidden(self, timeout: Optional[int] = None) -> None:
        """Wait for element to be hidden"""
        locator = await self.get_locator()
        await locator.wait_for(state="hidden", timeout=timeout or self.timeout)

    async def hover(self, **kwargs) -> None:
        """Hover over element"""
        locator = await self.get_locator()
        await locator.hover(timeout=self.timeout, **kwargs)
        logger.debug(f"Hovered over element: {self.name}")

    async def focus(self, **kwargs) -> None:
        """Focus element"""
        locator = await self.get_locator()
        await locator.focus(timeout=self.timeout, **kwargs)

    async def scroll_into_view(self, **kwargs) -> None:
        """Scroll element into view"""
        locator = await self.get_locator()
        await locator.scroll_into_view_if_needed(timeout=self.timeout, **kwargs)

    async def take_screenshot(self, name: Optional[str] = None) -> str:
        """Take screenshot of element"""
        locator = await self.get_locator()
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{config.REPORTS_DIR}/screenshots/{name or self.name}_{timestamp}.png"
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        await locator.screenshot(path=filename)
        logger.debug(f"Element screenshot saved: {filename}")
        return filename

    async def get_bounding_box(self) -> Optional[Dict[str, float]]:
        """Get element bounding box"""
        locator = await self.get_locator()
        return await locator.bounding_box()

    async def get_element_handle(self) -> ElementHandle:
        """Get element handle for advanced operations"""
        locator = await self.get_locator()
        return await locator.element_handle()


class BasePage(ABC):
    """Advanced base page class with modern features"""

    def __init__(self, page: Page):
        self.page = page
        self.timeout = config.timeout
        self.base_url = config.base_url
        self.elements: Dict[str, BaseElement] = {}
        self.performance_metrics = PerformanceMetrics()

        # Initialize common elements
        self._init_elements()

    def _init_elements(self) -> None:
        """Initialize page elements - override in subclasses"""
        pass

    def add_element(self, name: str, locator: str, description: str = "", **kwargs) -> None:
        """Add element to page"""
        self.elements[name] = BaseElement(self.page, locator, name, **kwargs)

    def get_element(self, name: str) -> BaseElement:
        """Get element by name"""
        if name not in self.elements:
            raise KeyError(f"Element '{name}' not found. Available elements: {list(self.elements.keys())}")
        return self.elements[name]

    @step("Navigate to page")
    async def navigate(self, url: Optional[str] = None, **kwargs) -> None:
        """Navigate to page URL"""
        target_url = url or self.base_url
        start_time = time.time()

        await self.page.goto(target_url, wait_until="networkidle", timeout=self.timeout, **kwargs)

        load_time = time.time() - start_time
        self.performance_metrics.page_load_time = load_time

        if load_time > (config.performance.page_load_threshold / 1000):
            logger.warning(f"Slow page load: {target_url} took {load_time:.2f}s")

        logger.info(f"Navigated to: {target_url} ({load_time:.2f}s)")

    @step("Wait for page load")
    async def wait_for_load(self, state: str = "networkidle") -> None:
        """Wait for page to load"""
        await self.page.wait_for_load_state(state, timeout=self.timeout)

    @step("Take page screenshot")
    async def take_screenshot(self, name: str = "page", full_page: bool = True) -> str:
        """Take page screenshot"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{config.REPORTS_DIR}/screenshots/{name}_{timestamp}.png"
        Path(filename).parent.mkdir(parents=True, exist_ok=True)

        await self.page.screenshot(path=filename, full_page=full_page)
        logger.debug(f"Page screenshot saved: {filename}")
        return filename

    async def get_title(self) -> str:
        """Get page title"""
        return await self.page.title()

    async def get_url(self) -> str:
        """Get current URL"""
        return self.page.url

    async def refresh(self) -> None:
        """Refresh page"""
        await self.page.reload(wait_until="networkidle", timeout=self.timeout)
        logger.debug("Page refreshed")

    async def go_back(self) -> None:
        """Go back in browser history"""
        await self.page.go_back(wait_until="networkidle", timeout=self.timeout)
        logger.debug("Navigated back")

    async def go_forward(self) -> None:
        """Go forward in browser history"""
        await self.page.go_forward(wait_until="networkidle", timeout=self.timeout)
        logger.debug("Navigated forward")

    async def execute_script(self, script: str, *args) -> Any:
        """Execute JavaScript on page"""
        return await self.page.evaluate(script, args)

    async def wait_for_function(self, function: str, **kwargs) -> Any:
        """Wait for JavaScript function to return true"""
        return await self.page.wait_for_function(function, timeout=self.timeout, **kwargs)

    async def get_performance_metrics(self) -> PerformanceMetrics:
        """Get page performance metrics"""
        # Get navigation timing
        timing = await self.page.evaluate("""
            () => {
                const timing = performance.getEntriesByType('navigation')[0];
                return {
                    domContentLoaded: timing.domContentLoadedEventEnd - timing.domContentLoadedEventStart,
                    loadComplete: timing.loadEventEnd - timing.loadEventStart,
                };
            }
        """)

        self.performance_metrics.dom_content_loaded = timing.get('domContentLoaded', 0) / 1000
        self.performance_metrics.page_load_time = timing.get('loadComplete', 0) / 1000

        return self.performance_metrics

    async def check_accessibility(self) -> Dict[str, Any]:
        """Check page accessibility"""
        if not config.accessibility.enabled:
            return {"enabled": False}

        # Run accessibility audit
        results = await self.page.evaluate("""
            () => {
                // Basic accessibility checks
                const issues = [];
                const elements = document.querySelectorAll('*');

                elements.forEach(el => {
                    // Check for alt text on images
                    if (el.tagName === 'IMG' && !el.getAttribute('alt')) {
                        issues.push({
                            type: 'missing_alt',
                            element: el.outerHTML.substring(0, 100),
                            severity: 'error'
                        });
                    }

                    // Check for labels on form elements
                    if (['INPUT', 'SELECT', 'TEXTAREA'].includes(el.tagName) &&
                        el.getAttribute('type') !== 'hidden' &&
                        !el.getAttribute('aria-label') &&
                        !document.querySelector(`label[for="${el.id}"]`)) {
                        issues.push({
                            type: 'missing_label',
                            element: el.outerHTML.substring(0, 100),
                            severity: 'warning'
                        });
                    }
                });

                return {
                    violations: issues.length,
                    issues: issues,
                    score: Math.max(0, 100 - (issues.length * 10))
                };
            }
        """)

        logger.info(f"Accessibility check completed. Score: {results.get('score', 0)}")
        return results

    async def inject_monitoring_script(self) -> None:
        """Inject performance monitoring script"""
        await self.page.add_script_tag(content="""
            window.performanceMetrics = {
                startTime: Date.now(),
                navigationStart: performance.timing.navigationStart,
                events: []
            };

            // Monitor performance
            new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    window.performanceMetrics.events.push({
                        type: entry.entryType,
                        name: entry.name,
                        duration: entry.duration,
                        startTime: entry.startTime
                    });
                }
            }).observe({entryTypes: ['measure', 'paint', 'layout-shift']});
        """)

    @abstractmethod
    async def is_loaded(self) -> bool:
        """Check if page is fully loaded - implement in subclasses"""
        pass

    @abstractmethod
    def get_page_elements(self) -> Dict[str, str]:
        """Get page elements mapping - implement in subclasses"""
        pass


class BaseTest(ABC):
    """Advanced base test class with modern testing features"""

    # Class variables for shared browser instances
    _browser: Optional[Browser] = None
    _context: Optional[BrowserContext] = None
    _playwright = None

    def __init__(self):
        self.page: Optional[Page] = None
        self.current_page: Optional[BasePage] = None
        self.test_result = TestResult("", "pending", 0.0)
        self.start_time = 0.0

    @classmethod
    @asynccontextmanager
    async def browser_context(cls):
        """Context manager for browser setup/cleanup"""
        await cls._setup_browser()
        try:
            yield cls._browser
        finally:
            await cls._cleanup_browser()

    @classmethod
    async def _setup_browser(cls) -> None:
        """Setup browser instance"""
        if cls._browser is not None:
            return

        from playwright.async_api import async_playwright

        cls._playwright = await async_playwright().start()

        # Configure browser launch options
        launch_options = {
            "headless": config.headless,
            "slow_mo": config.browser.slow_mo,
            "args": config.browser.args,
        }

        # Launch browser based on configuration
        if config.browser.name == "firefox":
            cls._browser = await cls._playwright.firefox.launch(**launch_options)
        elif config.browser.name == "webkit":
            cls._browser = await cls._playwright.webkit.launch(**launch_options)
        else:  # chromium
            cls._browser = await cls._playwright.chromium.launch(**launch_options)

        # Create browser context
        context_options = {
            "accept_downloads": True,
            "viewport": config.device.viewport,
            "user_agent": config.device.user_agent,
        }

        if config.video_on_failure:
            context_options["record_video_dir"] = config.VIDEOS_DIR
            context_options["record_video_size"] = config.device.viewport

        cls._context = await cls._browser.new_context(**context_options)

        logger.info(f"Browser setup complete: {config.browser.name}")

    @classmethod
    async def _cleanup_browser(cls) -> None:
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

        logger.info("Browser cleanup complete")

    async def setup_test(self) -> None:
        """Setup test environment"""
        await self._setup_browser()

        # Create new page for test
        self.page = await self._context.new_page()
        self.page.set_default_timeout(config.timeout)

        # Inject monitoring script
        if config.monitoring.enabled:
            await self.page.add_script_tag(content="""
                window.testStartTime = Date.now();
            """)

        self.start_time = time.time()
        logger.debug(f"Test setup complete for {self.__class__.__name__}")

    async def teardown_test(self) -> None:
        """Teardown test environment"""
        if self.page:
            # Take screenshot on failure if configured
            if hasattr(self, '_test_failed') and self._test_failed and config.screenshot_on_failure:
                try:
                    await self.take_screenshot("failure")
                except Exception as e:
                    logger.error(f"Failed to take failure screenshot: {e}")

            await self.page.close()
            self.page = None

        # Calculate test duration
        duration = time.time() - self.start_time
        self.test_result.duration = duration

        logger.debug(f"Test teardown complete. Duration: {duration:.2f}s")

    async def take_screenshot(self, name: str = "screenshot") -> str:
        """Take screenshot"""
        if not self.page:
            raise RuntimeError("Page not initialized")

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{config.REPORTS_DIR}/screenshots/{name}_{timestamp}.png"
        Path(filename).parent.mkdir(parents=True, exist_ok=True)

        await self.page.screenshot(path=filename, full_page=True)
        logger.debug(f"Screenshot saved: {filename}")
        return filename

    async def navigate_to_page(self, page_class: type, **kwargs) -> BasePage:
        """Navigate to a specific page"""
        page_instance = page_class(self.page)
        await page_instance.navigate(**kwargs)
        self.current_page = page_instance
        return page_instance

    async def wait_for_page_load(self, timeout: Optional[int] = None) -> None:
        """Wait for page to load"""
        if self.page:
            await self.page.wait_for_load_state("networkidle", timeout=timeout or config.timeout)

    async def execute_test_step(self, step_func: Callable, *args, **kwargs) -> Any:
        """Execute a test step with error handling"""
        try:
            return await step_func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Test step failed: {step_func.__name__} - {e}")
            raise

    def mark_test_failed(self, error: Exception) -> None:
        """Mark test as failed"""
        self._test_failed = True
        self.test_result.status = "failed"
        self.test_result.error_message = str(error)

    def mark_test_passed(self) -> None:
        """Mark test as passed"""
        self.test_result.status = "passed"

    def add_performance_metric(self, key: str, value: Any) -> None:
        """Add performance metric"""
        self.test_result.performance_metrics[key] = value

    def add_metadata(self, key: str, value: Any) -> None:
        """Add test metadata"""
        self.test_result.metadata[key] = value

    @abstractmethod
    async def run_test(self) -> None:
        """Run the actual test - implement in subclasses"""
        pass

    @abstractmethod
    def get_test_data(self) -> Dict[str, Any]:
        """Get test data - implement in subclasses"""
        return {}


class BaseAPITest(ABC):
    """Base class for API testing"""

    def __init__(self):
        self.base_url = config.api.base_url
        self.session = None
        self.headers = config.api.headers.copy()

    async def setup_session(self) -> None:
        """Setup HTTP session"""
        import aiohttp
        self.session = aiohttp.ClientSession(
            base_url=self.base_url,
            headers=self.headers,
            timeout=aiohttp.ClientTimeout(total=config.api.timeout / 1000)
        )

    async def teardown_session(self) -> None:
        """Teardown HTTP session"""
        if self.session:
            await self.session.close()

    async def make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request"""
        if not self.session:
            await self.setup_session()

        start_time = time.time()

        try:
            async with self.session.request(method, endpoint, **kwargs) as response:
                duration = time.time() - start_time

                result = {
                    "status_code": response.status,
                    "headers": dict(response.headers),
                    "duration": duration,
                    "url": str(response.url),
                }

                # Get response content
                try:
                    result["json"] = await response.json()
                except:
                    result["text"] = await response.text()

                # Check performance threshold
                if duration > (config.performance.api_response_threshold / 1000):
                    logger.warning(f"Slow API response: {method} {endpoint} took {duration:.2f}s")

                return result

        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"API request failed: {method} {endpoint} ({duration:.2f}s) - {e}")
            raise

    @abstractmethod
    async def run_api_test(self) -> None:
        """Run API test - implement in subclasses"""
        pass


class BaseDatabaseTest(ABC):
    """Base class for database testing"""

    def __init__(self):
        self.connection = None
        self.db_config = config.database

    async def setup_connection(self) -> None:
        """Setup database connection"""
        if not self.db_config:
            raise RuntimeError("Database configuration not found")

        # Database connection logic would go here
        # Implementation depends on database type
        pass

    async def teardown_connection(self) -> None:
        """Teardown database connection"""
        if self.connection:
            await self.connection.close()

    async def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict]:
        """Execute database query"""
        start_time = time.time()

        try:
            # Query execution logic would go here
            result = []  # Placeholder

            duration = time.time() - start_time

            # Check performance threshold
            if duration > (config.performance.db_query_threshold / 1000):
                logger.warning(f"Slow database query took {duration:.2f}s: {query[:50]}...")

            return result

        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Database query failed ({duration:.2f}s): {query[:50]}... - {e}")
            raise

    @abstractmethod
    async def run_db_test(self) -> None:
        """Run database test - implement in subclasses"""
        pass


__all__ = [
    "TestResult",
    "PageElement",
    "PerformanceMetrics",
    "BaseElement",
    "BasePage",
    "BaseTest",
    "BaseAPITest",
    "BaseDatabaseTest",
]