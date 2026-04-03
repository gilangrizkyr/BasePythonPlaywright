"""
Pytest Configuration and Fixtures
=================================

Global pytest configuration, fixtures, and hooks for the professional framework.
"""

import asyncio
import os
import pytest
import pytest_asyncio
from pathlib import Path
from typing import Dict, Any, Optional, Callable

from core.config import config
from core.base import BaseTest


# =============================================================================
# PYTEST CONFIGURATION
# =============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers and settings"""

    # Add custom markers
    config.addinivalue_line("markers", "smoke: Quick smoke tests")
    config.addinivalue_line("markers", "regression: Regression test suite")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "api: API tests")
    config.addinivalue_line("markers", "ui: UI tests")
    config.addinivalue_line("markers", "performance: Performance tests")
    config.addinivalue_line("markers", "accessibility: Accessibility tests")
    config.addinivalue_line("markers", "security: Security tests")
    config.addinivalue_line("markers", "mobile: Mobile tests")
    config.addinivalue_line("markers", "visual: Visual regression tests")
    config.addinivalue_line("markers", "slow: Slow running tests")
    config.addinivalue_line("markers", "flaky: Tests that may be unstable")
    config.addinivalue_line("markers", "skip_ci: Skip in CI environment")
    config.addinivalue_line("markers", "quarantine: Tests under investigation")

    # Set default timeout (removed - not a valid pytest config)


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on configuration"""

    # Skip tests marked with skip_ci in CI environment
    if os.getenv('CI') == 'true':
        skip_ci = pytest.mark.skip(reason="Skipped in CI environment")
        for item in items:
            if "skip_ci" in item.keywords:
                item.add_marker(skip_ci)

    # Add environment marker
    env_marker = pytest.mark.env(config.getoption("--env", default="testing"))
    for item in items:
        item.add_marker(env_marker)


def pytest_addoption(parser):
    """Add custom command line options"""

    # Environment options
    parser.addoption(
        "--env",
        action="store",
        default="testing",
        choices=["development", "staging", "production", "testing"],
        help="Environment to run tests in"
    )

    # Browser options
    parser.addoption(
        "--browser",
        action="store",
        default=config.browser.name,
        choices=["chromium", "firefox", "webkit"],
        help="Browser to use for testing"
    )

    # Execution options
    parser.addoption(
        "--headed",
        action="store_true",
        default=not config.headless,
        help="Run browser in headed mode"
    )

    parser.addoption(
        "--headless",
        action="store_true",
        default=config.headless,
        help="Run browser in headless mode"
    )

    # Feature flags
    parser.addoption(
        "--performance",
        action="store_true",
        default=config.monitoring.enabled,
        help="Enable performance monitoring"
    )

    parser.addoption(
        "--accessibility",
        action="store_true",
        default=config.accessibility.enabled,
        help="Enable accessibility testing"
    )

    parser.addoption(
        "--security",
        action="store_true",
        default=False,
        help="Enable security scanning"
    )

    parser.addoption(
        "--visual",
        action="store_true",
        default=config.visual.enabled,
        help="Enable visual regression testing"
    )


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def page():
    """Page fixture for individual tests"""
    # This is a simplified sync fixture for basic testing
    # In production, you would want proper async setup
    import asyncio
    from playwright.async_api import async_playwright

    async def _get_page():
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_timeout(30000)

        # Store playwright instance for cleanup
        page._playwright = playwright
        page._browser = browser
        page._context = context

        return page

    # Run async setup
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    page = loop.run_until_complete(_get_page())

    yield page

    # Cleanup
    async def _cleanup():
        await page._context.close()
        await page._browser.close()
        await page._playwright.stop()

    loop.run_until_complete(_cleanup())
    loop.close()


@pytest.fixture
async def authenticated_page(page):
    """Authenticated page fixture"""
    # Navigate to login page
    await page.goto(f"{config.base_url}/login")

    # Perform login (customize based on your app)
    await page.fill("#username", "testuser@example.com")
    await page.fill("#password", "password123")
    await page.click("#login-btn")

    # Wait for navigation to dashboard
    await page.wait_for_url("**/dashboard")

    yield page


@pytest.fixture
def test_data():
    """Test data fixture"""
    from core.utils import data_generator

    return {
        "user": data_generator.generate_user(),
        "product": data_generator.generate_product(),
        "credit_card": data_generator.generate_credit_card(),
    }


@pytest.fixture
async def api_client():
    """API client fixture"""
    from core.utils import APIUtilities

    client = APIUtilities(config.api.base_url)
    await client.setup_session()

    try:
        yield client
    finally:
        await client.teardown_session()


@pytest.fixture
async def db_connection():
    """Database connection fixture"""
    from core.utils import DatabaseUtilities

    db = DatabaseUtilities(config.database.connection_string or "")
    await db.connect()

    try:
        yield db
    finally:
        await db.disconnect()


# =============================================================================
# HOOKS
# =============================================================================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results and add custom information"""

    # Execute the test
    outcome = yield
    report = outcome.get_result()

    # Add custom information to report
    if hasattr(item, 'funcargs'):
        # Add browser info
        if 'page' in item.funcargs:
            page = item.funcargs['page']
            report.browser = getattr(page, 'browser', {}).get('name', 'unknown')

        # Add environment info
        report.environment = item.config.getoption("--env")

    # Add performance data if available
    if hasattr(item, 'performance_data'):
        report.performance_data = item.performance_data

    # Handle failures
    if report.when == "call" and report.failed:
        # Take failure screenshot
        if 'page' in item.funcargs:
            page = item.funcargs['page']
            try:
                screenshot_path = f"{config.REPORTS_DIR}/screenshots/failure_{item.name}.png"
                Path(screenshot_path).parent.mkdir(parents=True, exist_ok=True)
                # Schedule screenshot for later execution
                import asyncio
                asyncio.create_task(take_failure_screenshot(page, screenshot_path))
                report.screenshot_path = screenshot_path
            except Exception as e:
                print(f"Failed to take failure screenshot: {e}")


async def take_failure_screenshot(page, screenshot_path: str):
    """Take failure screenshot asynchronously"""
    try:
        await page.screenshot(path=screenshot_path, full_page=True)
    except Exception as e:
        print(f"Failed to take failure screenshot: {e}")


@pytest.hookimpl(trylast=True)
def pytest_sessionstart(session):
    """Configure test session with additional metadata"""
    session.config.test_environment = {
        'browser': session.config.getoption("--browser", "chromium"),
        'environment': session.config.getoption("--env", "testing"),
        'headless': session.config.getoption("--headless", False),
        'performance': session.config.getoption("--performance", False),
        'accessibility': session.config.getoption("--accessibility", False),
        'security': session.config.getoption("--security", False),
    }


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_test_info(item) -> Dict[str, Any]:
    """Get test information from pytest item"""
    return {
        'name': item.name,
        'nodeid': item.nodeid,
        'function': item.function.__name__,
        'module': item.module.__name__ if item.module else None,
        'cls': item.cls.__name__ if item.cls else None,
        'markers': [marker.name for marker in item.iter_markers()],
        'keywords': list(item.keywords.keys()),
    }


def is_slow_test(item) -> bool:
    """Check if test is marked as slow"""
    return 'slow' in [marker.name for marker in item.iter_markers()]


def is_flaky_test(item) -> bool:
    """Check if test is marked as flaky"""
    return 'flaky' in [marker.name for marker in item.iter_markers()]


def should_retry_test(item) -> bool:
    """Determine if test should be retried"""
    return is_flaky_test(item) or 'retry' in [marker.name for marker in item.iter_markers()]


# =============================================================================
# CUSTOM ASSERTIONS
# =============================================================================

def assert_page_loaded(page, expected_url: Optional[str] = None):
    """Assert that page is loaded"""
    if expected_url:
        assert page.url == expected_url, f"Expected URL {expected_url}, got {page.url}"
    assert "loading" not in page.url.lower(), "Page appears to still be loading"


def assert_element_visible(page, selector: str, timeout: int = 5000):
    """Assert that element is visible"""
    from playwright.async_api import expect
    expect(page.locator(selector)).to_be_visible(timeout=timeout)


def assert_text_contains(page, selector: str, expected_text: str, timeout: int = 5000):
    """Assert that element contains expected text"""
    from playwright.async_api import expect
    expect(page.locator(selector)).to_contain_text(expected_text, timeout=timeout)


def assert_api_response(response: Dict[str, Any], expected_status: int = 200):
    """Assert API response"""
    assert response['status_code'] == expected_status, f"Expected status {expected_status}, got {response['status_code']}"


# =============================================================================
# PERFORMANCE MONITORING
# =============================================================================

@pytest.fixture(autouse=True)
def performance_monitor(request):
    """Performance monitoring fixture"""
    if not request.config.getoption("--performance"):
        yield
        return

    start_time = asyncio.get_event_loop().time()

    def finalize():
        duration = asyncio.get_event_loop().time() - start_time
        request.node.performance_data = {
            'duration': duration,
            'start_time': start_time,
            'end_time': start_time + duration,
        }

    request.addfinalizer(finalize)
    yield


# =============================================================================
# ENVIRONMENT SETUP
# =============================================================================

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment(request):
    """Setup test environment"""
    # Set environment variables from pytest options
    os.environ['BROWSER_NAME'] = request.config.getoption("--browser")
    os.environ['HEADLESS'] = str(request.config.getoption("--headless")).lower()
    os.environ['ENVIRONMENT'] = request.config.getoption("--env")

    # Enable features based on options
    if request.config.getoption("--performance"):
        os.environ['PERFORMANCE_MONITORING'] = 'true'

    if request.config.getoption("--accessibility"):
        os.environ['ACCESSIBILITY_CHECKING'] = 'true'

    if request.config.getoption("--security"):
        os.environ['SECURITY_SCANNING'] = 'true'

    if request.config.getoption("--visual"):
        os.environ['VISUAL_REGRESSION_ENABLED'] = 'true'

    yield

    # Cleanup environment variables
    env_vars = [
        'BROWSER_NAME', 'HEADLESS', 'ENVIRONMENT',
        'PERFORMANCE_MONITORING', 'ACCESSIBILITY_CHECKING',
        'SECURITY_SCANNING', 'VISUAL_REGRESSION_ENABLED'
    ]

    for var in env_vars:
        os.environ.pop(var, None)


# =============================================================================
# TEST DATA MANAGEMENT
# =============================================================================

@pytest.fixture(scope="session")
def test_data_manager():
    """Test data manager fixture"""
    from core.utils import data_generator

    class TestDataManager:
        def __init__(self):
            self.data = {}

        def get_user(self, key: str = "default"):
            if key not in self.data:
                self.data[key] = data_generator.generate_user()
            return self.data[key]

        def get_product(self, key: str = "default"):
            if key not in self.data:
                self.data[key] = data_generator.generate_product()
            return self.data[key]

        def cleanup(self):
            self.data.clear()

    manager = TestDataManager()
    yield manager
    manager.cleanup()

