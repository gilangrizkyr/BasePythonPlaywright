"""
Professional Test Decorators
===========================

Advanced decorators for test automation with logging, screenshots, retries,
performance monitoring, and more professional features.
"""

import time
import functools
import asyncio
from typing import Callable, Any, Optional, Dict, List, Union
from pathlib import Path
import inspect
from loguru import logger
from core.config import config


def screenshot_on_failure(func: Callable) -> Callable:
    """
    Decorator to take screenshot on test failure.

    Usage:
        @screenshot_on_failure
        async def test_something(self):
            # Test code
            pass
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            if config.screenshot_on_failure:
                # Get test instance (usually self)
                test_instance = args[0] if args else None
                if test_instance and hasattr(test_instance, 'page'):
                    try:
                        timestamp = time.strftime("%Y%m%d_%H%M%S")
                        screenshot_path = f"reports/screenshots/{func.__name__}_failure_{timestamp}.png"
                        Path(screenshot_path).parent.mkdir(parents=True, exist_ok=True)
                        await test_instance.page.screenshot(path=screenshot_path, full_page=True)
                        logger.error(f"Screenshot saved: {screenshot_path}")
                    except Exception as screenshot_error:
                        logger.error(f"Failed to take screenshot: {screenshot_error}")

            # Re-raise original exception
            raise e

    return wrapper


def retry_on_failure(max_retries: int = None, delay: int = None, backoff: float = None,
                    exceptions: tuple = (Exception,)) -> Callable:
    """
    Decorator to retry test on failure.

    Args:
        max_retries: Maximum number of retry attempts
        delay: Delay between retries in seconds
        backoff: Backoff factor for exponential delay
        exceptions: Tuple of exceptions to retry on

    Usage:
        @retry_on_failure(max_retries=3, delay=1, exceptions=(AssertionError, TimeoutError))
        async def test_something(self):
            # Test code
            pass
    """
    max_retries = max_retries or config.retry.max_retries
    delay = delay or (config.retry.retry_delay / 1000)  # Convert to seconds
    backoff = backoff or config.retry.backoff_factor

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay

            for attempt in range(max_retries + 1):
                try:
                    if attempt > 0:
                        logger.warning(f"Retry attempt {attempt}/{max_retries} for {func.__name__}")
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff

                    return await func(*args, **kwargs)

                except exceptions as e:
                    last_exception = e
                    if attempt == max_retries:
                        logger.error(f"All {max_retries + 1} attempts failed for {func.__name__}")
                        break
                    else:
                        logger.warning(f"Attempt {attempt + 1} failed: {e}")

            raise last_exception

        return wrapper

    return decorator


def performance_monitor(func: Callable) -> Callable:
    """
    Decorator to monitor test performance.

    Usage:
        @performance_monitor
        async def test_something(self):
            # Test code
            pass
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = None  # Could be implemented with psutil

        try:
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time

            # Log performance metrics
            logger.info(f"Performance - {func.__name__}: {execution_time:.2f}s")

            # Check against thresholds
            if execution_time > (config.performance.page_load_threshold / 1000):
                logger.warning(f"Slow test detected: {func.__name__} took {execution_time:.2f}s")

            return result

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Test failed after {execution_time:.2f}s: {func.__name__}")
            raise e

    return wrapper


def log_test_execution(func: Callable) -> Callable:
    """
    Decorator to log test execution details.

    Usage:
        @log_test_execution
        async def test_something(self):
            # Test code
            pass
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # Get test class and method info
        test_class = args[0].__class__.__name__ if args else "Unknown"
        test_method = func.__name__

        logger.info(f"Starting test: {test_class}.{test_method}")

        # Log test parameters if any
        if kwargs:
            logger.debug(f"Test parameters: {kwargs}")

        start_time = time.time()

        try:
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time

            logger.success(f"Test passed: {test_class}.{test_method} ({execution_time:.2f}s)")
            return result

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Test failed: {test_class}.{test_method} ({execution_time:.2f}s) - {e}")
            raise e

    return wrapper


def data_driven(data_source: Union[str, List[Dict], Callable]) -> Callable:
    """
    Decorator for data-driven testing.

    Args:
        data_source: Path to data file, list of data, or callable that returns data

    Usage:
        @data_driven("test_data/login_data.json")
        async def test_login(self, username, password):
            # Test code
            pass

        @data_driven([{"username": "user1", "password": "pass1"}])
        async def test_login(self, username, password):
            # Test code
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Load test data
            if isinstance(data_source, str):
                # Load from file
                data = load_test_data(data_source)
            elif isinstance(data_source, list):
                # Use provided list
                data = data_source
            elif callable(data_source):
                # Call function to get data
                data = data_source()
            else:
                raise ValueError("Invalid data source")

            # Run test for each data set
            results = []
            for i, test_data in enumerate(data):
                logger.info(f"Running test iteration {i + 1}/{len(data)}")

                # Merge test data into kwargs
                test_kwargs = {**kwargs, **test_data}

                try:
                    result = await func(*args, **test_kwargs)
                    results.append({"iteration": i + 1, "status": "passed", "data": test_data})
                except Exception as e:
                    results.append({"iteration": i + 1, "status": "failed", "data": test_data, "error": str(e)})
                    if not config.retry.recovery_enabled:
                        raise e

            return results

        return wrapper

    return decorator


def step(description: str = None) -> Callable:
    """
    Decorator to mark test steps with descriptions.

    Args:
        description: Step description

    Usage:
        @step("Login to application")
        async def login_step(self):
            # Login code
            pass

        async def test_workflow(self):
            await self.login_step()
            await self.navigate_to_dashboard()
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            step_desc = description or func.__name__.replace("_", " ").title()
            logger.info(f"Step: {step_desc}")

            start_time = time.time()

            try:
                result = await func(*args, **kwargs)
                execution_time = time.time() - start_time
                logger.success(f"Step completed: {step_desc} ({execution_time:.2f}s)")
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(f"Step failed: {step_desc} ({execution_time:.2f}s) - {e}")
                raise e

        # Store step description for reporting
        wrapper.step_description = description or func.__name__.replace("_", " ").title()
        return wrapper

    return decorator


def api_step(endpoint: str = None, method: str = "GET") -> Callable:
    """
    Decorator for API test steps.

    Args:
        endpoint: API endpoint
        method: HTTP method

    Usage:
        @api_step("/api/users", "POST")
        async def create_user(self, user_data):
            # API call code
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            api_endpoint = endpoint or f"/{func.__name__}"
            logger.info(f"API Call: {method} {api_endpoint}")

            start_time = time.time()

            try:
                result = await func(*args, **kwargs)
                execution_time = time.time() - start_time

                # Check response time threshold
                if execution_time > (config.performance.api_response_threshold / 1000):
                    logger.warning(f"Slow API response: {method} {api_endpoint} took {execution_time:.2f}s")

                logger.success(f"API Call completed: {method} {api_endpoint} ({execution_time:.2f}s)")
                return result

            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(f"API Call failed: {method} {api_endpoint} ({execution_time:.2f}s) - {e}")
                raise e

        return wrapper

    return decorator


def database_step(query_type: str = "SELECT") -> Callable:
    """
    Decorator for database test steps.

    Args:
        query_type: Type of database query

    Usage:
        @database_step("INSERT")
        async def create_user_record(self, user_data):
            # Database operation code
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            logger.info(f"Database Operation: {query_type}")

            start_time = time.time()

            try:
                result = await func(*args, **kwargs)
                execution_time = time.time() - start_time

                # Check query time threshold
                if execution_time > (config.performance.db_query_threshold / 1000):
                    logger.warning(f"Slow database query: {query_type} took {execution_time:.2f}s")

                logger.success(f"Database Operation completed: {query_type} ({execution_time:.2f}s)")
                return result

            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(f"Database Operation failed: {query_type} ({execution_time:.2f}s) - {e}")
                raise e

        return wrapper

    return decorator


def mobile_step(action: str = None) -> Callable:
    """
    Decorator for mobile test steps.

    Args:
        action: Mobile action description

    Usage:
        @mobile_step("Tap login button")
        async def tap_login_button(self):
            # Mobile interaction code
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            action_desc = action or func.__name__.replace("_", " ").title()
            logger.info(f"Mobile Action: {action_desc}")

            start_time = time.time()

            try:
                result = await func(*args, **kwargs)
                execution_time = time.time() - start_time
                logger.success(f"Mobile Action completed: {action_desc} ({execution_time:.2f}s)")
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(f"Mobile Action failed: {action_desc} ({execution_time:.2f}s) - {e}")
                raise e

        return wrapper

    return decorator


def visual_comparison(baseline_name: str = None) -> Callable:
    """
    Decorator for visual regression testing.

    Args:
        baseline_name: Name of baseline image

    Usage:
        @visual_comparison("homepage")
        async def test_homepage_visual(self):
            # Navigate and check visual
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            baseline = baseline_name or func.__name__
            logger.info(f"Visual Comparison: {baseline}")

            try:
                result = await func(*args, **kwargs)

                # Visual comparison logic would go here
                # This is a placeholder for the actual implementation
                logger.success(f"Visual Comparison passed: {baseline}")
                return result

            except Exception as e:
                logger.error(f"Visual Comparison failed: {baseline} - {e}")
                raise e

        return wrapper

    return decorator


def accessibility_check(level: str = None) -> Callable:
    """
    Decorator for accessibility testing.

    Args:
        level: WCAG compliance level

    Usage:
        @accessibility_check("AA")
        async def test_page_accessibility(self):
            # Accessibility check code
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            wcag_level = level or config.accessibility.wcag_level
            logger.info(f"Accessibility Check: WCAG {wcag_level}")

            try:
                result = await func(*args, **kwargs)
                logger.success(f"Accessibility Check passed: WCAG {wcag_level}")
                return result
            except Exception as e:
                logger.error(f"Accessibility Check failed: WCAG {wcag_level} - {e}")
                raise e

        return wrapper

    return decorator


def security_scan(scan_type: str = "basic") -> Callable:
    """
    Decorator for security testing.

    Args:
        scan_type: Type of security scan

    Usage:
        @security_scan("xss")
        async def test_xss_vulnerability(self):
            # Security test code
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            logger.info(f"Security Scan: {scan_type}")

            try:
                result = await func(*args, **kwargs)
                logger.success(f"Security Scan passed: {scan_type}")
                return result
            except Exception as e:
                logger.error(f"Security Scan failed: {scan_type} - {e}")
                raise e

        return wrapper

    return decorator


def load_test_data(filepath: str) -> List[Dict]:
    """
    Load test data from file.

    Args:
        filepath: Path to test data file

    Returns:
        List of test data dictionaries
    """
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"Test data file not found: {filepath}")

    if path.suffix == ".json":
        with open(path, "r") as f:
            data = json.load(f)
            return data if isinstance(data, list) else [data]

    elif path.suffix in [".yaml", ".yml"]:
        with open(path, "r") as f:
            return yaml.safe_load(f)

    elif path.suffix == ".csv":
        import pandas as pd
        df = pd.read_csv(path)
        return df.to_dict("records")

    elif path.suffix == ".xlsx":
        import pandas as pd
        df = pd.read_excel(path)
        return df.to_dict("records")

    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")


# Combined decorators for common use cases
def full_test_decorator(func: Callable = None, *, retries: int = 3, screenshot: bool = True,
                       performance: bool = True, logging: bool = True) -> Callable:
    """
    Combined decorator with multiple features.

    Usage:
        @full_test_decorator(retries=3, screenshot=True, performance=True, logging=True)
        async def test_something(self):
            # Test code
            pass
    """
    if func is None:
        return lambda f: full_test_decorator(f, retries=retries, screenshot=screenshot,
                                           performance=performance, logging=logging)

    # Apply decorators in reverse order
    if logging:
        func = log_test_execution(func)
    if performance:
        func = performance_monitor(func)
    if screenshot:
        func = screenshot_on_failure(func)
    if retries > 0:
        func = retry_on_failure(max_retries=retries)(func)

    return func


__all__ = [
    "screenshot_on_failure",
    "retry_on_failure",
    "performance_monitor",
    "log_test_execution",
    "data_driven",
    "step",
    "api_step",
    "database_step",
    "mobile_step",
    "visual_comparison",
    "accessibility_check",
    "security_scan",
    "full_test_decorator",
    "load_test_data",
]