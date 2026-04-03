"""
Test Package
============

This package contains all test files and test utilities for the professional
Playwright automation framework.

Modules:
--------
- conftest.py: Pytest configuration, fixtures, and hooks
- test_examples.py: Comprehensive test examples demonstrating framework capabilities
- test_example.py: Simple test example for quick reference

Test Categories:
---------------
- smoke: Quick smoke tests for critical functionality
- regression: Full regression test suite
- e2e: End-to-end user journey tests
- api: API testing scenarios
- ui: User interface tests
- performance: Performance and load testing
- accessibility: Accessibility compliance tests
- security: Security vulnerability tests
- mobile: Mobile application tests
- visual: Visual regression tests

Usage:
------
Run tests with pytest:
    pytest tests/ -v

Run specific test categories:
    pytest tests/ -m smoke
    pytest tests/ -m regression
    pytest tests/ -m e2e

Run with custom options:
    pytest tests/ --browser firefox --headed --performance

For more information, see the README.md file or run:
    python run_tests.py --help
"""

# Test package version
__version__ = "1.0.0"

# Import commonly used test utilities
from .conftest import (
    assert_page_loaded,
    assert_element_visible,
    assert_text_contains,
    assert_api_response,
    get_test_info,
    is_slow_test,
    is_flaky_test,
    should_retry_test,
)

# Export test utilities for easy access
__all__ = [
    # Custom assertions
    'assert_page_loaded',
    'assert_element_visible',
    'assert_text_contains',
    'assert_api_response',

    # Utility functions
    'get_test_info',
    'is_slow_test',
    'is_flaky_test',
    'should_retry_test',
]
