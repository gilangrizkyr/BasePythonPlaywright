"""
Example Test Cases
==================

Comprehensive test examples demonstrating the professional Playwright framework.
"""

import pytest
import asyncio
from typing import Dict, Any

from core.base import BaseTest
from core.utils import data_generator, web_utils, performance_utils
from decorators import (
    screenshot_on_failure,
    retry_on_failure,
    performance_monitor,
    log_test_execution,
    data_driven,
    step,
)
from pages import LoginPage, DashboardPage, ProductPage, CheckoutPage, SearchPage


class TestLoginFunctionality(BaseTest):
    """Test login functionality"""

    def get_test_data(self) -> Dict[str, Any]:
        """Get test data for login tests"""
        return {
            "valid_user": {
                "username": "testuser@example.com",
                "password": "password123",
                "expected_message": "Welcome back"
            },
            "invalid_user": {
                "username": "invalid@example.com",
                "password": "wrongpassword",
                "expected_error": "Invalid credentials"
            }
        }

    @log_test_execution
    @screenshot_on_failure
    @performance_monitor
    async def run_test(self) -> None:
        """Run login test"""
        # Navigate to login page
        login_page = await self.navigate_to_page(LoginPage)

        # Verify page loaded
        assert await login_page.is_loaded(), "Login page did not load properly"

        # Test data
        test_data = self.get_test_data()["valid_user"]

        # Perform login
        await login_page.login(test_data["username"], test_data["password"])

        # Verify successful login by checking dashboard
        dashboard_page = DashboardPage(self.page)
        await dashboard_page.wait_for_page_load()

        assert await dashboard_page.is_loaded(), "Dashboard did not load after login"

        welcome_message = await dashboard_page.get_welcome_message()
        assert test_data["expected_message"] in welcome_message, f"Expected welcome message not found: {welcome_message}"

        # Add performance metrics
        self.add_performance_metric("login_time", await self.page.evaluate("() => performance.now()"))

        logger.info("Login test completed successfully")


class TestInvalidLogin(BaseTest):
    """Test invalid login scenarios"""

    @data_driven([
        {"username": "invalid@example.com", "password": "wrong", "expected_error": "Invalid credentials"},
        {"username": "", "password": "password123", "expected_error": "Username is required"},
        {"username": "test@example.com", "password": "", "expected_error": "Password is required"},
    ])
    @log_test_execution
    @screenshot_on_failure
    async def run_test(self, test_data: Dict[str, str]) -> None:
        """Run invalid login test"""
        login_page = await self.navigate_to_page(LoginPage)

        # Perform login with invalid credentials
        await login_page.login(test_data["username"], test_data["password"])

        # Check for error message
        error_message = await login_page.get_error_message()
        assert test_data["expected_error"] in error_message, f"Expected error not found: {error_message}"

        logger.info(f"Invalid login test passed for scenario: {test_data}")


class TestDashboardFunctionality(BaseTest):
    """Test dashboard functionality"""

    async def run_test(self) -> None:
        """Run dashboard test"""
        # Login first
        login_page = await self.navigate_to_page(LoginPage)
        test_data = {"username": "testuser@example.com", "password": "password123"}
        await login_page.login(test_data["username"], test_data["password"])

        # Navigate to dashboard
        dashboard_page = await self.navigate_to_page(DashboardPage)

        # Verify dashboard elements
        assert await dashboard_page.is_loaded(), "Dashboard not loaded"

        # Check dashboard cards
        cards_count = await dashboard_page.get_dashboard_cards_count()
        assert cards_count > 0, "No dashboard cards found"

        # Check notifications
        notifications_count = await dashboard_page.get_notifications_count()
        assert notifications_count >= 0, "Invalid notifications count"

        # Take screenshot for verification
        await dashboard_page.take_screenshot("dashboard_loaded.png")

        logger.info("Dashboard functionality test completed")


class TestProductSearch(BaseTest):
    """Test product search functionality"""

    @data_driven([
        {"query": "laptop", "expected_min_results": 1},
        {"query": "nonexistentproduct12345", "expected_min_results": 0},
        {"query": "", "expected_min_results": 0},
    ])
    @log_test_execution
    @screenshot_on_failure
    async def run_test(self, test_data: Dict[str, Any]) -> None:
        """Run product search test"""
        search_page = await self.navigate_to_page(SearchPage)

        # Perform search
        await search_page.perform_search(test_data["query"])

        # Wait for results
        await asyncio.sleep(2)  # Allow time for search results to load

        # Check results
        results_count = await search_page.get_search_results_count()

        if test_data["expected_min_results"] == 0:
            # For empty or no results queries
            if results_count == 0:
                assert await search_page.is_no_results_visible(), "No results message should be visible"
            else:
                # Some results found, check if they contain the query
                titles = await search_page.get_result_titles()
                relevant_results = [title for title in titles if test_data["query"].lower() in title.lower()]
                assert len(relevant_results) >= results_count * 0.5, "Too many irrelevant results"
        else:
            assert results_count >= test_data["expected_min_results"], f"Expected at least {test_data['expected_min_results']} results, got {results_count}"

        logger.info(f"Product search test completed for query: '{test_data['query']}'")


class TestE2ECheckout(BaseTest):
    """End-to-end checkout test"""

    async def run_test(self) -> None:
        """Run complete checkout flow"""
        # Generate test data
        user_data = data_generator.generate_user()
        payment_data = data_generator.generate_credit_card()

        # Login
        login_page = await self.navigate_to_page(LoginPage)
        await login_page.login("testuser@example.com", "password123")

        # Search for a product
        search_page = await self.navigate_to_page(SearchPage)
        await search_page.perform_search("laptop")

        # Click on first result
        await search_page.click_result_by_index(0)

        # Add product to cart
        product_page = ProductPage(self.page)
        await product_page.wait_for_page_load()
        assert await product_page.is_loaded(), "Product page not loaded"

        await product_page.add_to_cart(1)

        # Navigate to checkout (assuming cart redirects to checkout)
        await self.page.goto(f"{config.base_url}/checkout")

        # Fill checkout information
        checkout_page = CheckoutPage(self.page)
        await checkout_page.wait_for_page_load()
        assert await checkout_page.is_loaded(), "Checkout page not loaded"

        # Fill billing info
        billing_info = {
            "first_name": user_data["first_name"],
            "last_name": user_data["last_name"],
            "email": user_data["email"],
            "address": user_data["address"]["street"],
            "city": user_data["address"]["city"],
            "zip": user_data["address"]["zip_code"],
        }
        await checkout_page.fill_billing_info(billing_info)

        # Fill payment info
        payment_info = {
            "card_number": payment_data["number"],
            "expiry": payment_data["expiration_date"],
            "cvv": payment_data["cvv"],
        }
        await checkout_page.fill_payment_info(payment_info)

        # Take screenshot before placing order
        await checkout_page.take_screenshot("checkout_filled.png")

        # Note: In real scenario, we wouldn't actually place the order
        # unless using test payment gateway
        # await checkout_page.place_order()

        logger.info("E2E checkout test completed successfully")


class TestPerformanceMonitoring(BaseTest):
    """Test performance monitoring"""

    @performance_monitor
    async def run_test(self) -> None:
        """Run performance test"""
        start_time = time.time()

        # Navigate to page
        await self.page.goto(config.base_url)
        await self.page.wait_for_load_state("networkidle")

        # Measure page load time
        load_time = time.time() - start_time

        # Get performance metrics
        perf_metrics = await web_utils.get_page_performance_metrics(self.page)

        # Add metrics to test result
        self.add_performance_metric("page_load_time", load_time)
        self.add_performance_metric("dom_content_loaded", perf_metrics.get("domContentLoaded", 0) / 1000)
        self.add_performance_metric("resources_loaded", perf_metrics.get("resourcesLoaded", 0))

        # Check performance thresholds
        assert performance_utils.check_performance_threshold(
            load_time, config.performance.page_load_threshold / 1000, "page_load"
        ), f"Page load time {load_time:.2f}s exceeds threshold"

        # Take performance screenshot
        await self.take_screenshot("performance_test.png")

        logger.info(f"Performance test completed. Load time: {load_time:.2f}s")


class TestAccessibility(BaseTest):
    """Test accessibility features"""

    async def run_test(self) -> None:
        """Run accessibility test"""
        # Navigate to page
        await self.page.goto(config.base_url)
        await self.page.wait_for_load_state("networkidle")

        # Run accessibility check
        accessibility_results = await self.page.evaluate("""
            () => {
                const issues = [];
                const elements = document.querySelectorAll('*');

                // Check images for alt text
                const images = document.querySelectorAll('img');
                images.forEach(img => {
                    if (!img.getAttribute('alt')) {
                        issues.push({
                            type: 'missing_alt',
                            element: img.outerHTML.substring(0, 100),
                            severity: 'error'
                        });
                    }
                });

                // Check form elements for labels
                const inputs = document.querySelectorAll('input, select, textarea');
                inputs.forEach(input => {
                    if (input.type !== 'hidden' && input.type !== 'submit') {
                        const label = document.querySelector(`label[for="${input.id}"]`);
                        if (!label && !input.getAttribute('aria-label')) {
                            issues.push({
                                type: 'missing_label',
                                element: input.outerHTML.substring(0, 100),
                                severity: 'warning'
                            });
                        }
                    }
                });

                return {
                    violations: issues.length,
                    issues: issues,
                    score: Math.max(0, 100 - (issues.length * 10))
                };
            }
        """)

        # Add accessibility metrics
        self.add_performance_metric("accessibility_score", accessibility_results.get("score", 0))
        self.add_performance_metric("accessibility_violations", accessibility_results.get("violations", 0))

        # Log issues
        if accessibility_results.get("violations", 0) > 0:
            logger.warning(f"Accessibility issues found: {accessibility_results['violations']}")
            for issue in accessibility_results.get("issues", []):
                logger.warning(f"  {issue['type']}: {issue['severity']}")

        # Accessibility should have reasonable score
        assert accessibility_results.get("score", 0) >= 70, f"Accessibility score too low: {accessibility_results.get('score', 0)}"

        logger.info(f"Accessibility test completed. Score: {accessibility_results.get('score', 0)}")


class TestVisualRegression(BaseTest):
    """Test visual regression"""

    async def run_test(self) -> None:
        """Run visual regression test"""
        # Navigate to page
        await self.page.goto(config.base_url)
        await self.page.wait_for_load_state("networkidle")

        # Take baseline screenshot
        baseline_screenshot = await self.take_screenshot("baseline_homepage.png")

        # Make a visual change (if testing visual diff tools)
        # In real scenario, this would compare against stored baseline

        # For now, just verify screenshot was taken
        assert baseline_screenshot.endswith(".png"), "Screenshot not taken properly"
        assert os.path.exists(baseline_screenshot), "Screenshot file not found"

        # Add visual test metadata
        self.add_metadata("baseline_screenshot", baseline_screenshot)
        self.add_metadata("viewport_size", f"{config.device.viewport['width']}x{config.device.viewport['height']}")

        logger.info("Visual regression test completed")


# Pytest fixtures for setup/teardown
@pytest.fixture(scope="session")
async def browser_context():
    """Browser context fixture"""
    from core.base import BaseTest
    async with BaseTest.browser_context() as context:
        yield context


@pytest.fixture
async def page(browser_context):
    """Page fixture"""
    page = await browser_context.new_page()
    yield page
    await page.close()


# Example of running tests programmatically
async def run_example_tests():
    """Run example tests programmatically"""
    from core.runner import AdvancedTestRunner, TestSuiteConfig

    # Configure test suite
    config = TestSuiteConfig(
        name="Example Test Suite",
        description="Demonstration of professional Playwright framework",
        parallel_workers=2,
        tags=["example", "demo"]
    )

    # Run tests
    runner = AdvancedTestRunner(config)
    results = await runner.run_suite()

    print(f"\nTest Results Summary:")
    print(f"Total: {results.total_tests}")
    print(f"Passed: {results.passed}")
    print(f"Failed: {results.failed}")
    print(f"Duration: {results.duration:.2f}s")

    return results


if __name__ == "__main__":
    # Run example tests
    asyncio.run(run_example_tests())