"""
Professional Playwright Automation Framework
===========================================

Enterprise-grade automation testing framework with modern architecture.

Features:
- Advanced Page Object Model
- Data-driven testing
- Parallel execution
- API testing integration
- Database testing
- Mobile testing
- Performance monitoring
- Security testing
- Accessibility testing
- Visual regression testing
- CI/CD integration
- Docker & Kubernetes support
- Advanced reporting (Allure)
- Custom decorators & hooks
- Environment management
- Test data management

Author: Professional QA Team
Version: 2.0.0
Date: April 2026
"""

__version__ = "2.0.0"
__author__ = "Professional QA Team"
__description__ = "Enterprise-grade Playwright automation framework"

# Framework metadata
FRAMEWORK_NAME = "Professional Playwright Framework"
FRAMEWORK_VERSION = __version__
FRAMEWORK_AUTHOR = __author__

# Supported platforms
SUPPORTED_PLATFORMS = ["web", "api", "mobile", "database"]
SUPPORTED_BROWSERS = ["chromium", "firefox", "webkit", "edge", "safari"]
SUPPORTED_LANGUAGES = ["python", "javascript", "typescript"]

# Default configurations
DEFAULT_TIMEOUT = 30000
DEFAULT_HEADLESS = True
DEFAULT_BROWSER = "chromium"
DEFAULT_PARALLEL_WORKERS = 4

# Reporting
DEFAULT_REPORT_FORMAT = "allure"
DEFAULT_SCREENSHOT_ON_FAILURE = True
DEFAULT_VIDEO_ON_FAILURE = False

# Performance thresholds
DEFAULT_PAGE_LOAD_TIMEOUT = 5000  # ms
DEFAULT_API_RESPONSE_TIMEOUT = 10000  # ms
DEFAULT_DB_QUERY_TIMEOUT = 5000  # ms

# Security
DEFAULT_SECURITY_SCAN_ENABLED = False
DEFAULT_VULNERABILITY_CHECK_ENABLED = False

# Accessibility
DEFAULT_ACCESSIBILITY_CHECK_ENABLED = False
DEFAULT_WCAG_LEVEL = "AA"

# Visual regression
DEFAULT_VISUAL_COMPARISON_ENABLED = False
DEFAULT_VISUAL_DIFF_THRESHOLD = 0.01

# Mobile
DEFAULT_MOBILE_PLATFORM = "android"
DEFAULT_MOBILE_DEVICE = "Pixel 5"

# API
DEFAULT_API_BASE_URL = "https://api.example.com"
DEFAULT_API_TIMEOUT = 10000

# Database
DEFAULT_DB_TYPE = "postgresql"
DEFAULT_DB_HOST = "localhost"
DEFAULT_DB_PORT = 5432

# CI/CD
DEFAULT_CI_PLATFORM = "github_actions"
DEFAULT_DOCKER_IMAGE = "python:3.12-slim"

# Monitoring
DEFAULT_METRICS_ENABLED = True
DEFAULT_DASHBOARD_ENABLED = False

# Logging
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Test data
DEFAULT_TEST_DATA_FORMAT = "json"
DEFAULT_DATA_PROVIDER = "faker"

# Retry & Recovery
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_DELAY = 1000  # ms
DEFAULT_RECOVERY_ENABLED = True

# Cloud integration
DEFAULT_CLOUD_PROVIDER = "none"
DEFAULT_CLOUD_REGION = "us-east-1"

# Notification
DEFAULT_NOTIFICATION_ENABLED = False
DEFAULT_NOTIFICATION_CHANNELS = ["slack", "email", "teams"]

# Compliance
DEFAULT_COMPLIANCE_ENABLED = False
DEFAULT_COMPLIANCE_STANDARDS = ["GDPR", "HIPAA", "PCI-DSS"]

# Advanced features
DEFAULT_AI_ASSISTED_TESTING = False
DEFAULT_ML_BASED_ANALYSIS = False
DEFAULT_AUTO_HEALING = False
DEFAULT_SMART_WAIT = True

# Framework paths
FRAMEWORK_ROOT = "."
CONFIG_DIR = "config"
CORE_DIR = "core"
PAGES_DIR = "pages"
TESTS_DIR = "tests"
TEST_DATA_DIR = "test_data"
REPORTS_DIR = "reports"
LOGS_DIR = "logs"
SCREENSHOTS_DIR = "reports/screenshots"
VIDEOS_DIR = "reports/videos"
ALLURE_RESULTS_DIR = "allure-results"
ALLURE_REPORT_DIR = "allure-report"

# File extensions
PYTHON_EXT = ".py"
JSON_EXT = ".json"
YAML_EXT = ".yaml"
YML_EXT = ".yml"
CSV_EXT = ".csv"
EXCEL_EXT = ".xlsx"
HTML_EXT = ".html"
XML_EXT = ".xml"
PDF_EXT = ".pdf"

# Test markers
MARKERS = {
    "smoke": "Smoke tests - critical functionality",
    "regression": "Regression tests - full test suite",
    "integration": "Integration tests - system interaction",
    "api": "API tests - backend testing",
    "ui": "UI tests - frontend testing",
    "mobile": "Mobile tests - mobile app testing",
    "performance": "Performance tests - load and stress",
    "security": "Security tests - vulnerability scanning",
    "accessibility": "Accessibility tests - WCAG compliance",
    "visual": "Visual regression tests - UI comparison",
    "database": "Database tests - data integrity",
    "slow": "Slow tests - long running tests",
    "flaky": "Flaky tests - unstable tests",
    "wip": "Work in progress - incomplete tests",
    "skip": "Skipped tests - temporarily disabled",
    "critical": "Critical tests - must pass",
    "high": "High priority tests",
    "medium": "Medium priority tests",
    "low": "Low priority tests",
    "manual": "Manual tests - require human intervention",
    "automated": "Automated tests - fully automated",
    "data_driven": "Data-driven tests - parameterized",
    "parallel": "Parallel tests - can run concurrently",
    "serial": "Serial tests - must run sequentially",
}

# Environment types
ENVIRONMENTS = {
    "development": "Development environment",
    "staging": "Staging environment",
    "production": "Production environment",
    "testing": "Testing environment",
    "qa": "Quality Assurance environment",
    "uat": "User Acceptance Testing environment",
    "demo": "Demo environment",
    "sandbox": "Sandbox environment",
}

# Browser configurations
BROWSER_CONFIGS = {
    "chromium": {
        "name": "Chromium",
        "channel": None,
        "args": ["--no-sandbox", "--disable-dev-shm-usage"],
        "downloads_path": "downloads",
    },
    "firefox": {
        "name": "Firefox",
        "channel": None,
        "args": [],
        "downloads_path": "downloads",
    },
    "webkit": {
        "name": "WebKit",
        "channel": None,
        "args": [],
        "downloads_path": "downloads",
    },
    "edge": {
        "name": "Microsoft Edge",
        "channel": "msedge",
        "args": ["--no-sandbox", "--disable-dev-shm-usage"],
        "downloads_path": "downloads",
    },
    "safari": {
        "name": "Safari",
        "channel": None,
        "args": [],
        "downloads_path": "downloads",
    },
}

# Device configurations
DEVICE_CONFIGS = {
    "desktop": {
        "viewport": {"width": 1920, "height": 1080},
        "device_scale_factor": 1,
        "is_mobile": False,
        "has_touch": False,
    },
    "tablet": {
        "viewport": {"width": 768, "height": 1024},
        "device_scale_factor": 2,
        "is_mobile": True,
        "has_touch": True,
    },
    "mobile": {
        "viewport": {"width": 375, "height": 667},
        "device_scale_factor": 2,
        "is_mobile": True,
        "has_touch": True,
    },
}

# API configurations
API_CONFIGS = {
    "rest": {
        "base_url": DEFAULT_API_BASE_URL,
        "timeout": DEFAULT_API_TIMEOUT,
        "headers": {
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        "auth": None,
    },
    "graphql": {
        "base_url": DEFAULT_API_BASE_URL,
        "timeout": DEFAULT_API_TIMEOUT,
        "headers": {
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        "auth": None,
    },
    "soap": {
        "base_url": DEFAULT_API_BASE_URL,
        "timeout": DEFAULT_API_TIMEOUT,
        "headers": {
            "Content-Type": "text/xml",
            "Accept": "text/xml",
        },
        "auth": None,
    },
}

# Database configurations
DB_CONFIGS = {
    "postgresql": {
        "driver": "postgresql",
        "port": 5432,
        "charset": "utf8",
    },
    "mysql": {
        "driver": "mysql",
        "port": 3306,
        "charset": "utf8mb4",
    },
    "mongodb": {
        "driver": "mongodb",
        "port": 27017,
        "charset": None,
    },
    "redis": {
        "driver": "redis",
        "port": 6379,
        "charset": None,
    },
    "oracle": {
        "driver": "oracle",
        "port": 1521,
        "charset": "utf8",
    },
    "sqlserver": {
        "driver": "sqlserver",
        "port": 1433,
        "charset": "utf8",
    },
}

# Cloud provider configurations
CLOUD_CONFIGS = {
    "none": {
        "region": "local",
        "service": "local",
        "runtime": "python3.12",
    },
    "aws": {
        "region": "us-east-1",
        "service": "lambda",
        "runtime": "python3.12",
    },
    "azure": {
        "region": "eastus",
        "service": "functions",
        "runtime": "python",
    },
    "gcp": {
        "region": "us-central1",
        "service": "functions",
        "runtime": "python312",
    },
    "vercel": {
        "region": "iad1",
        "service": "functions",
        "runtime": "python3.12",
    },
    "netlify": {
        "region": "us-east-1",
        "service": "functions",
        "runtime": "python3.12",
    },
}

# CI/CD configurations
CI_CD_CONFIGS = {
    "github_actions": {
        "workflow_file": ".github/workflows/ci.yml",
        "trigger": ["push", "pull_request"],
        "python_versions": ["3.9", "3.10", "3.11", "3.12"],
        "os": ["ubuntu-latest", "windows-latest", "macos-latest"],
    },
    "gitlab_ci": {
        "config_file": ".gitlab-ci.yml",
        "stages": ["test", "build", "deploy"],
        "image": "python:3.12-slim",
    },
    "jenkins": {
        "config_file": "Jenkinsfile",
        "agent": "docker",
        "image": "python:3.12-slim",
    },
    "circle_ci": {
        "config_file": ".circleci/config.yml",
        "executor": "python",
        "image": "cimg/python:3.12",
    },
    "travis_ci": {
        "config_file": ".travis.yml",
        "language": "python",
        "python": ["3.9", "3.10", "3.11", "3.12"],
    },
    "azure_pipelines": {
        "config_file": "azure-pipelines.yml",
        "vm_image": "ubuntu-latest",
        "python_version": "3.12",
    },
}

# Docker configurations
DOCKER_CONFIGS = {
    "base_image": "python:3.12-slim",
    "workdir": "/app",
    "user": "playwright",
    "ports": ["8080"],
    "volumes": ["/app/reports", "/app/logs"],
    "environment": {
        "PYTHONPATH": "/app",
        "DISPLAY": ":99",
    },
}

# Kubernetes configurations
KUBERNETES_CONFIGS = {
    "namespace": "playwright",
    "replicas": 1,
    "image": "playwright-framework:latest",
    "resources": {
        "requests": {"memory": "512Mi", "cpu": "500m"},
        "limits": {"memory": "1Gi", "cpu": "1000m"},
    },
    "env": [
        {"name": "PYTHONPATH", "value": "/app"},
        {"name": "DISPLAY", "value": ":99"},
    ],
}

# Monitoring configurations
MONITORING_CONFIGS = {
    "prometheus": {
        "enabled": True,
        "port": 9090,
        "metrics_path": "/metrics",
    },
    "grafana": {
        "enabled": False,
        "port": 3000,
        "dashboard_path": "/dashboards",
    },
    "datadog": {
        "enabled": False,
        "api_key": None,
        "app_key": None,
    },
    "new_relic": {
        "enabled": False,
        "license_key": None,
        "app_name": FRAMEWORK_NAME,
    },
}

# Notification configurations
NOTIFICATION_CONFIGS = {
    "slack": {
        "webhook_url": None,
        "channel": "#automation",
        "username": "Playwright Bot",
    },
    "teams": {
        "webhook_url": None,
        "channel": "Automation",
    },
    "discord": {
        "webhook_url": None,
        "channel": "automation",
        "username": "Playwright Bot",
    },
    "email": {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "username": None,
        "password": None,
        "recipients": [],
    },
    "telegram": {
        "bot_token": None,
        "chat_id": None,
    },
}

# Security configurations
SECURITY_CONFIGS = {
    "ssl_verification": True,
    "certificate_validation": True,
    "vulnerability_scanning": False,
    "sql_injection_check": False,
    "xss_check": False,
    "csrf_check": False,
    "headers_check": True,
    "cookies_check": True,
}

# Performance configurations
PERFORMANCE_CONFIGS = {
    "page_load_threshold": 3000,  # ms
    "api_response_threshold": 1000,  # ms
    "db_query_threshold": 500,  # ms
    "memory_threshold": 512,  # MB
    "cpu_threshold": 80,  # %
    "network_threshold": 1000,  # KB/s
}

# Accessibility configurations
ACCESSIBILITY_CONFIGS = {
    "wcag_level": "AA",
    "rules": [
        "color-contrast",
        "keyboard-navigation",
        "screen-reader",
        "focus-management",
        "alt-text",
        "semantic-html",
    ],
    "ignore_rules": [],
    "custom_rules": [],
}

# Visual regression configurations
VISUAL_CONFIGS = {
    "threshold": 0.01,
    "diff_color": [255, 0, 0],  # Red
    "baseline_dir": "test_data/baselines",
    "diff_dir": "reports/visual_diffs",
    "formats": ["png", "jpg", "webp"],
}

# Mobile configurations
MOBILE_CONFIGS = {
    "android": {
        "platform_version": "12.0",
        "device_name": "emulator-5554",
        "app_package": None,
        "app_activity": None,
        "automation_name": "UiAutomator2",
    },
    "ios": {
        "platform_version": "15.0",
        "device_name": "iPhone 13",
        "bundle_id": None,
        "automation_name": "XCUITest",
    },
}

# Framework status
FRAMEWORK_STATUS = "active"
FRAMEWORK_MAINTAINER = "Professional QA Team"
FRAMEWORK_LICENSE = "MIT"
FRAMEWORK_DOCUMENTATION = "https://framework-docs.example.com"
FRAMEWORK_REPOSITORY = "https://github.com/professional-qa/playwright-framework"
FRAMEWORK_ISSUES = "https://github.com/professional-qa/playwright-framework/issues"
FRAMEWORK_DISCUSSIONS = "https://github.com/professional-qa/playwright-framework/discussions"

# Export all constants
__all__ = [
    # Framework info
    "FRAMEWORK_NAME",
    "FRAMEWORK_VERSION",
    "FRAMEWORK_AUTHOR",
    "FRAMEWORK_STATUS",

    # Supported platforms
    "SUPPORTED_PLATFORMS",
    "SUPPORTED_BROWSERS",
    "SUPPORTED_LANGUAGES",

    # Default configurations
    "DEFAULT_TIMEOUT",
    "DEFAULT_HEADLESS",
    "DEFAULT_BROWSER",
    "DEFAULT_PARALLEL_WORKERS",

    # Reporting
    "DEFAULT_REPORT_FORMAT",
    "DEFAULT_SCREENSHOT_ON_FAILURE",
    "DEFAULT_VIDEO_ON_FAILURE",

    # Performance
    "DEFAULT_PAGE_LOAD_TIMEOUT",
    "DEFAULT_API_RESPONSE_TIMEOUT",
    "DEFAULT_DB_QUERY_TIMEOUT",

    # Security
    "DEFAULT_SECURITY_SCAN_ENABLED",
    "DEFAULT_VULNERABILITY_CHECK_ENABLED",

    # Accessibility
    "DEFAULT_ACCESSIBILITY_CHECK_ENABLED",
    "DEFAULT_WCAG_LEVEL",

    # Visual
    "DEFAULT_VISUAL_COMPARISON_ENABLED",
    "DEFAULT_VISUAL_DIFF_THRESHOLD",

    # Mobile
    "DEFAULT_MOBILE_PLATFORM",
    "DEFAULT_MOBILE_DEVICE",

    # API
    "DEFAULT_API_BASE_URL",
    "DEFAULT_API_TIMEOUT",

    # Database
    "DEFAULT_DB_TYPE",
    "DEFAULT_DB_HOST",
    "DEFAULT_DB_PORT",

    # CI/CD
    "DEFAULT_CI_PLATFORM",
    "DEFAULT_DOCKER_IMAGE",

    # Monitoring
    "DEFAULT_METRICS_ENABLED",
    "DEFAULT_DASHBOARD_ENABLED",

    # Logging
    "DEFAULT_LOG_LEVEL",
    "DEFAULT_LOG_FORMAT",

    # Test data
    "DEFAULT_TEST_DATA_FORMAT",
    "DEFAULT_DATA_PROVIDER",

    # Retry
    "DEFAULT_MAX_RETRIES",
    "DEFAULT_RETRY_DELAY",
    "DEFAULT_RECOVERY_ENABLED",

    # Cloud
    "DEFAULT_CLOUD_PROVIDER",
    "DEFAULT_CLOUD_REGION",

    # Notification
    "DEFAULT_NOTIFICATION_ENABLED",
    "DEFAULT_NOTIFICATION_CHANNELS",

    # Compliance
    "DEFAULT_COMPLIANCE_ENABLED",
    "DEFAULT_COMPLIANCE_STANDARDS",

    # Advanced
    "DEFAULT_AI_ASSISTED_TESTING",
    "DEFAULT_ML_BASED_ANALYSIS",
    "DEFAULT_AUTO_HEALING",
    "DEFAULT_SMART_WAIT",

    # Paths
    "FRAMEWORK_ROOT",
    "CONFIG_DIR",
    "CORE_DIR",
    "PAGES_DIR",
    "TESTS_DIR",
    "TEST_DATA_DIR",
    "REPORTS_DIR",
    "LOGS_DIR",
    "SCREENSHOTS_DIR",
    "VIDEOS_DIR",
    "ALLURE_RESULTS_DIR",
    "ALLURE_REPORT_DIR",

    # Extensions
    "PYTHON_EXT",
    "JSON_EXT",
    "YAML_EXT",
    "YML_EXT",
    "CSV_EXT",
    "EXCEL_EXT",
    "HTML_EXT",
    "XML_EXT",
    "PDF_EXT",

    # Collections
    "MARKERS",
    "ENVIRONMENTS",
    "BROWSER_CONFIGS",
    "DEVICE_CONFIGS",
    "API_CONFIGS",
    "DB_CONFIGS",
    "CLOUD_CONFIGS",
    "CI_CD_CONFIGS",
    "DOCKER_CONFIGS",
    "KUBERNETES_CONFIGS",
    "MONITORING_CONFIGS",
    "NOTIFICATION_CONFIGS",
    "SECURITY_CONFIGS",
    "PERFORMANCE_CONFIGS",
    "ACCESSIBILITY_CONFIGS",
    "VISUAL_CONFIGS",
    "MOBILE_CONFIGS",
]