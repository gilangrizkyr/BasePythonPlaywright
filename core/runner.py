"""
Professional Test Runner
========================

Advanced test runner with parallel execution, comprehensive reporting,
CI/CD integration, and enterprise-grade features.
"""

import asyncio
import time
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime
from loguru import logger

import pytest
from playwright.async_api import Browser, BrowserContext, Page
from pydantic import BaseModel, Field

from core.config import config
from core.base import BaseTest, TestResult


class TestSuiteConfig(BaseModel):
    """Test suite configuration"""
    name: str = "Playwright Test Suite"
    description: str = ""
    parallel_workers: int = Field(default_factory=lambda: config.parallel.max_workers)
    browser: str = Field(default_factory=lambda: config.browser.name)
    headless: bool = Field(default_factory=lambda: config.headless)
    retries: int = Field(default_factory=lambda: config.retry.max_attempts)
    timeout: int = Field(default_factory=lambda: config.timeout)
    tags: List[str] = Field(default_factory=list)
    environment: str = Field(default_factory=lambda: config.environment)
    test_data_path: Optional[str] = None
    report_path: str = Field(default_factory=lambda: config.REPORTS_DIR)


@dataclass
class TestExecutionResult:
    """Test execution result"""
    suite_name: str
    total_tests: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    errors: int = 0
    duration: float = 0.0
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    results: List[TestResult] = field(default_factory=list)
    environment_info: Dict[str, Any] = field(default_factory=dict)
    performance_summary: Dict[str, Any] = field(default_factory=dict)


class AdvancedTestRunner:
    """Advanced test runner with enterprise features"""

    def __init__(self, suite_config: TestSuiteConfig):
        self.config = suite_config
        self.execution_result = TestExecutionResult(suite_config.name)
        self._browsers: List[Browser] = []
        self._contexts: List[BrowserContext] = []
        self._executor = ThreadPoolExecutor(max_workers=suite_config.parallel_workers)

        # Setup logging
        self._setup_logging()

        # Setup reporting
        self._setup_reporting()

    def _setup_logging(self) -> None:
        """Setup advanced logging"""
        log_file = f"{self.config.report_path}/logs/test_execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        # Remove default handler
        logger.remove()

        # Add console handler
        logger.add(
            lambda msg: print(msg, end=""),
            level=config.logging.level,
            format=config.logging.format,
            colorize=True
        )

        # Add file handler
        logger.add(
            log_file,
            level="DEBUG",
            format=config.logging.file_format,
            rotation="10 MB",
            retention="7 days"
        )

        logger.info(f"Test execution logging initialized: {log_file}")

    def _setup_reporting(self) -> None:
        """Setup reporting directories"""
        directories = [
            f"{self.config.report_path}/screenshots",
            f"{self.config.report_path}/videos",
            f"{self.config.report_path}/logs",
            f"{self.config.report_path}/allure-results",
            f"{self.config.report_path}/html-report",
            f"{self.config.report_path}/junit-xml",
            f"{self.config.report_path}/performance",
        ]

        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)

        logger.info("Reporting directories created")

    async def _setup_browsers(self) -> None:
        """Setup browser instances for parallel execution"""
        from playwright.async_api import async_playwright

        playwright = await async_playwright().start()

        try:
            for i in range(self.config.parallel_workers):
                # Launch browser
                launch_options = {
                    "headless": self.config.headless,
                    "slow_mo": config.browser.slow_mo,
                    "args": config.browser.args,
                }

                if self.config.browser == "firefox":
                    browser = await playwright.firefox.launch(**launch_options)
                elif self.config.browser == "webkit":
                    browser = await playwright.webkit.launch(**launch_options)
                else:  # chromium
                    browser = await playwright.chromium.launch(**launch_options)

                self._browsers.append(browser)

                # Create context
                context_options = {
                    "accept_downloads": True,
                    "viewport": config.device.viewport,
                    "user_agent": config.device.user_agent,
                }

                if config.video_on_failure:
                    context_options["record_video_dir"] = f"{self.config.report_path}/videos"
                    context_options["record_video_size"] = config.device.viewport

                context = await browser.new_context(**context_options)
                self._contexts.append(context)

                logger.debug(f"Browser {i+1}/{self.config.parallel_workers} initialized")

        except Exception as e:
            logger.error(f"Failed to setup browsers: {e}")
            await self._cleanup_browsers()
            raise

    async def _cleanup_browsers(self) -> None:
        """Cleanup browser resources"""
        for context in self._contexts:
            try:
                await context.close()
            except Exception as e:
                logger.error(f"Error closing context: {e}")

        self._contexts.clear()

        for browser in self._browsers:
            try:
                await browser.close()
            except Exception as e:
                logger.error(f"Error closing browser: {e}")

        self._browsers.clear()

        logger.info("Browser cleanup completed")

    async def _collect_tests(self) -> List[type]:
        """Collect test classes"""
        test_classes = []

        # Import test modules dynamically
        test_dir = Path("tests")
        if test_dir.exists():
            for file_path in test_dir.rglob("test_*.py"):
                try:
                    module_name = str(file_path.relative_to(test_dir)).replace("/", ".").replace("\\", ".").replace(".py", "")
                    module = __import__(f"tests.{module_name}", fromlist=[module_name])

                    # Find test classes
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (isinstance(attr, type) and
                            issubclass(attr, BaseTest) and
                            attr != BaseTest):
                            test_classes.append(attr)

                except Exception as e:
                    logger.error(f"Failed to import test module {file_path}: {e}")

        logger.info(f"Collected {len(test_classes)} test classes")
        return test_classes

    async def _run_test_parallel(self, test_class: type, worker_id: int) -> TestResult:
        """Run a single test in parallel"""
        test_instance = test_class()
        test_result = TestResult(test_class.__name__, "running", 0.0)

        try:
            # Setup test
            await test_instance.setup_test()

            # Assign browser context
            if worker_id < len(self._contexts):
                # Create new page from context
                page = await self._contexts[worker_id].new_page()
                test_instance.page = page

            # Run test
            start_time = time.time()
            await test_instance.run_test()
            duration = time.time() - start_time

            # Mark as passed
            test_instance.mark_test_passed()
            test_result.status = "passed"
            test_result.duration = duration

            logger.info(f"✓ {test_class.__name__} passed ({duration:.2f}s)")

        except Exception as e:
            duration = time.time() - (start_time if 'start_time' in locals() else time.time())
            test_result.duration = duration
            test_result.status = "failed"
            test_result.error_message = str(e)

            test_instance.mark_test_failed(e)
            logger.error(f"✗ {test_class.__name__} failed ({duration:.2f}s): {e}")

        finally:
            # Teardown test
            try:
                await test_instance.teardown_test()
            except Exception as e:
                logger.error(f"Error during test teardown for {test_class.__name__}: {e}")

        return test_result

    async def run_tests_parallel(self, test_classes: List[type]) -> None:
        """Run tests in parallel"""
        logger.info(f"Starting parallel test execution with {self.config.parallel_workers} workers")

        # Create tasks for parallel execution
        tasks = []
        for i, test_class in enumerate(test_classes):
            worker_id = i % self.config.parallel_workers
            task = asyncio.create_task(self._run_test_parallel(test_class, worker_id))
            tasks.append(task)

        # Wait for all tests to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Test execution error: {result}")
                self.execution_result.errors += 1
            else:
                self.execution_result.results.append(result)
                self.execution_result.total_tests += 1

                if result.status == "passed":
                    self.execution_result.passed += 1
                elif result.status == "failed":
                    self.execution_result.failed += 1
                elif result.status == "skipped":
                    self.execution_result.skipped += 1

    async def run_tests_sequential(self, test_classes: List[type]) -> None:
        """Run tests sequentially"""
        logger.info("Starting sequential test execution")

        for test_class in test_classes:
            result = await self._run_test_parallel(test_class, 0)
            self.execution_result.results.append(result)
            self.execution_result.total_tests += 1

            if result.status == "passed":
                self.execution_result.passed += 1
            elif result.status == "failed":
                self.execution_result.failed += 1
            elif result.status == "skipped":
                self.execution_result.skipped += 1

    async def _generate_reports(self) -> None:
        """Generate comprehensive test reports"""
        self.execution_result.end_time = datetime.now()
        self.execution_result.duration = (
            self.execution_result.end_time - self.execution_result.start_time
        ).total_seconds()

        # Generate JSON report
        json_report = self._generate_json_report()
        json_path = f"{self.config.report_path}/test_results.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_report, f, indent=2, default=str)
        logger.info(f"JSON report generated: {json_path}")

        # Generate HTML report
        html_report = self._generate_html_report()
        html_path = f"{self.config.report_path}/html-report/index.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_report)
        logger.info(f"HTML report generated: {html_path}")

        # Generate JUnit XML for CI/CD
        junit_report = self._generate_junit_report()
        junit_path = f"{self.config.report_path}/junit-xml/results.xml"
        with open(junit_path, 'w', encoding='utf-8') as f:
            f.write(junit_report)
        logger.info(f"JUnit XML report generated: {junit_path}")

        # Generate performance summary
        self._generate_performance_summary()

        # Send notifications if configured
        await self._send_notifications()

    def _generate_json_report(self) -> Dict[str, Any]:
        """Generate JSON test report"""
        return {
            "suite": {
                "name": self.config.name,
                "description": self.config.description,
                "environment": self.config.environment,
                "browser": self.config.browser,
                "parallel_workers": self.config.parallel_workers,
                "start_time": self.execution_result.start_time.isoformat(),
                "end_time": self.execution_result.end_time.isoformat() if self.execution_result.end_time else None,
                "duration": self.execution_result.duration,
            },
            "summary": {
                "total": self.execution_result.total_tests,
                "passed": self.execution_result.passed,
                "failed": self.execution_result.failed,
                "skipped": self.execution_result.skipped,
                "errors": self.execution_result.errors,
                "pass_rate": (self.execution_result.passed / self.execution_result.total_tests * 100) if self.execution_result.total_tests > 0 else 0,
            },
            "results": [
                {
                    "test_name": result.test_name,
                    "status": result.status,
                    "duration": result.duration,
                    "error_message": result.error_message,
                    "screenshot_path": result.screenshot_path,
                    "video_path": result.video_path,
                    "performance_metrics": result.performance_metrics,
                    "metadata": result.metadata,
                }
                for result in self.execution_result.results
            ],
            "environment_info": self.execution_result.environment_info,
            "performance_summary": self.execution_result.performance_summary,
        }

    def _generate_html_report(self) -> str:
        """Generate HTML test report"""
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.config.name} - Test Results</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .summary {{ background: #f5f5f5; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
        .passed {{ color: #28a745; }}
        .failed {{ color: #dc3545; }}
        .skipped {{ color: #ffc107; }}
        .test-result {{ margin-bottom: 10px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }}
        .test-passed {{ border-left: 5px solid #28a745; }}
        .test-failed {{ border-left: 5px solid #dc3545; }}
        .test-skipped {{ border-left: 5px solid #ffc107; }}
        .performance {{ background: #e9ecef; padding: 10px; margin-top: 10px; border-radius: 3px; }}
    </style>
</head>
<body>
    <h1>{self.config.name}</h1>
    <p>{self.config.description}</p>

    <div class="summary">
        <h2>Test Summary</h2>
        <p><strong>Total Tests:</strong> {self.execution_result.total_tests}</p>
        <p><strong>Passed:</strong> <span class="passed">{self.execution_result.passed}</span></p>
        <p><strong>Failed:</strong> <span class="failed">{self.execution_result.failed}</span></p>
        <p><strong>Skipped:</strong> <span class="skipped">{self.execution_result.skipped}</span></p>
        <p><strong>Duration:</strong> {self.execution_result.duration:.2f}s</p>
        <p><strong>Pass Rate:</strong> {(self.execution_result.passed / self.execution_result.total_tests * 100):.1f}%</p>
    </div>

    <h2>Test Results</h2>
"""

        for result in self.execution_result.results:
            status_class = f"test-{result.status}"
            html_template += f"""
    <div class="test-result {status_class}">
        <h3>{result.test_name}</h3>
        <p><strong>Status:</strong> {result.status.upper()}</p>
        <p><strong>Duration:</strong> {result.duration:.2f}s</p>
"""

            if result.error_message:
                html_template += f"<p><strong>Error:</strong> {result.error_message}</p>"

            if result.performance_metrics:
                html_template += f"""
        <div class="performance">
            <strong>Performance Metrics:</strong>
            <ul>
"""
                for key, value in result.performance_metrics.items():
                    html_template += f"<li>{key}: {value}</li>"
                html_template += "</ul></div>"

            html_template += "</div>"

        html_template += """
</body>
</html>
"""

        return html_template

    def _generate_junit_report(self) -> str:
        """Generate JUnit XML report for CI/CD"""
        xml_template = f"""<?xml version="1.0" encoding="UTF-8"?>
<testsuites name="{self.config.name}" tests="{self.execution_result.total_tests}" failures="{self.execution_result.failed}" errors="{self.execution_result.errors}" skipped="{self.execution_result.skipped}" time="{self.execution_result.duration}">
"""

        for result in self.execution_result.results:
            xml_template += f"""    <testsuite name="{result.test_name}" tests="1" failures="{'1' if result.status == 'failed' else '0'}" errors="{'1' if result.status == 'error' else '0'}" skipped="{'1' if result.status == 'skipped' else '0'}" time="{result.duration}">
        <testcase name="{result.test_name}" time="{result.duration}">
"""

            if result.status == "failed" and result.error_message:
                xml_template += f"""            <failure message="{result.error_message}">{result.error_message}</failure>
"""
            elif result.status == "error" and result.error_message:
                xml_template += f"""            <error message="{result.error_message}">{result.error_message}</error>
"""
            elif result.status == "skipped":
                xml_template += "<skipped />"

            xml_template += """        </testcase>
    </testsuite>
"""

        xml_template += "</testsuites>"
        return xml_template

    def _generate_performance_summary(self) -> None:
        """Generate performance summary"""
        if not self.execution_result.results:
            return

        total_duration = sum(result.duration for result in self.execution_result.results)
        avg_duration = total_duration / len(self.execution_result.results)

        # Collect all performance metrics
        all_metrics = {}
        for result in self.execution_result.results:
            for key, value in result.performance_metrics.items():
                if key not in all_metrics:
                    all_metrics[key] = []
                if isinstance(value, (int, float)):
                    all_metrics[key].append(value)

        # Calculate averages
        avg_metrics = {}
        for key, values in all_metrics.items():
            if values:
                avg_metrics[f"avg_{key}"] = sum(values) / len(values)
                avg_metrics[f"max_{key}"] = max(values)
                avg_metrics[f"min_{key}"] = min(values)

        self.execution_result.performance_summary = {
            "total_execution_time": total_duration,
            "average_test_duration": avg_duration,
            "slowest_test": max((r.duration for r in self.execution_result.results), default=0),
            "fastest_test": min((r.duration for r in self.execution_result.results), default=0),
            **avg_metrics,
        }

        # Save performance report
        perf_path = f"{self.config.report_path}/performance/summary.json"
        with open(perf_path, 'w', encoding='utf-8') as f:
            json.dump(self.execution_result.performance_summary, f, indent=2)
        logger.info(f"Performance summary saved: {perf_path}")

    async def _send_notifications(self) -> None:
        """Send test completion notifications"""
        if not config.notifications.enabled:
            return

        try:
            # Slack notification
            if config.notifications.slack_webhook:
                await self._send_slack_notification()

            # Email notification
            if config.notifications.email_smtp:
                await self._send_email_notification()

            # Teams notification
            if config.notifications.teams_webhook:
                await self._send_teams_notification()

        except Exception as e:
            logger.error(f"Failed to send notifications: {e}")

    async def _send_slack_notification(self) -> None:
        """Send Slack notification"""
        import aiohttp

        message = {
            "text": f"Test Suite Complete: {self.config.name}",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"🧪 {self.config.name} Results"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Total:* {self.execution_result.total_tests}"},
                        {"type": "mrkdwn", "text": f"*Passed:* ✅ {self.execution_result.passed}"},
                        {"type": "mrkdwn", "text": f"*Failed:* ❌ {self.execution_result.failed}"},
                        {"type": "mrkdwn", "text": f"*Duration:* ⏱️ {self.execution_result.duration:.1f}s"},
                    ]
                }
            ]
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(config.notifications.slack_webhook, json=message) as response:
                if response.status == 200:
                    logger.info("Slack notification sent successfully")
                else:
                    logger.error(f"Failed to send Slack notification: {response.status}")

    async def _send_email_notification(self) -> None:
        """Send email notification"""
        # Email implementation would go here
        logger.info("Email notification not implemented yet")

    async def _send_teams_notification(self) -> None:
        """Send Microsoft Teams notification"""
        # Teams implementation would go here
        logger.info("Teams notification not implemented yet")

    async def run_suite(self) -> TestExecutionResult:
        """Run the complete test suite"""
        logger.info(f"Starting test suite: {self.config.name}")
        self.execution_result.start_time = datetime.now()

        try:
            # Collect tests
            test_classes = await self._collect_tests()

            if not test_classes:
                logger.warning("No test classes found")
                return self.execution_result

            # Setup browsers
            await self._setup_browsers()

            # Run tests
            if self.config.parallel_workers > 1:
                await self.run_tests_parallel(test_classes)
            else:
                await self.run_tests_sequential(test_classes)

            # Generate reports
            await self._generate_reports()

            # Log summary
            logger.info(f"Test suite completed: {self.execution_result.passed}/{self.execution_result.total_tests} passed")

        except Exception as e:
            logger.error(f"Test suite execution failed: {e}")
            self.execution_result.errors += 1

        finally:
            # Cleanup
            await self._cleanup_browsers()

        return self.execution_result


async def run_test_suite(config_path: Optional[str] = None) -> TestExecutionResult:
    """Run test suite from configuration"""
    if config_path and Path(config_path).exists():
        # Load config from file
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        suite_config = TestSuiteConfig(**config_data)
    else:
        # Use default config
        suite_config = TestSuiteConfig()

    runner = AdvancedTestRunner(suite_config)
    return await runner.run_suite()


if __name__ == "__main__":
    # Run test suite
    asyncio.run(run_test_suite())