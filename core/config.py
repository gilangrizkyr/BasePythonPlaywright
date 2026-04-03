"""
Advanced Configuration Management
================================

Professional configuration system using Pydantic for type safety and validation.
Supports multiple environments, secrets management, and dynamic configuration.
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Literal
from pydantic import BaseModel, Field, validator, model_validator
from pydantic_settings import BaseSettings
from loguru import logger

from core import (
    DEFAULT_TIMEOUT,
    DEFAULT_HEADLESS,
    DEFAULT_BROWSER,
    DEFAULT_PARALLEL_WORKERS,
    DEFAULT_REPORT_FORMAT,
    DEFAULT_SCREENSHOT_ON_FAILURE,
    DEFAULT_VIDEO_ON_FAILURE,
    DEFAULT_PAGE_LOAD_TIMEOUT,
    DEFAULT_API_RESPONSE_TIMEOUT,
    DEFAULT_API_TIMEOUT,
    DEFAULT_DB_QUERY_TIMEOUT,
    DEFAULT_SECURITY_SCAN_ENABLED,
    DEFAULT_ACCESSIBILITY_CHECK_ENABLED,
    DEFAULT_WCAG_LEVEL,
    DEFAULT_VISUAL_COMPARISON_ENABLED,
    DEFAULT_MOBILE_PLATFORM,
    DEFAULT_API_BASE_URL,
    DEFAULT_DB_TYPE,
    DEFAULT_CI_PLATFORM,
    DEFAULT_METRICS_ENABLED,
    DEFAULT_LOG_LEVEL,
    DEFAULT_MAX_RETRIES,
    DEFAULT_RETRY_DELAY,
    DEFAULT_CLOUD_PROVIDER,
    DEFAULT_NOTIFICATION_ENABLED,
    DEFAULT_AI_ASSISTED_TESTING,
    DEFAULT_AUTO_HEALING,
    DEFAULT_SMART_WAIT,
    ENVIRONMENTS,
    BROWSER_CONFIGS,
    DEVICE_CONFIGS,
    API_CONFIGS,
    DB_CONFIGS,
    CLOUD_CONFIGS,
    CI_CD_CONFIGS,
    MONITORING_CONFIGS,
    NOTIFICATION_CONFIGS,
    SECURITY_CONFIGS,
    PERFORMANCE_CONFIGS,
    ACCESSIBILITY_CONFIGS,
    VISUAL_CONFIGS,
    MOBILE_CONFIGS,
)


class BrowserConfig(BaseModel):
    """Browser configuration model"""
    name: str = Field(..., description="Browser name")
    channel: Optional[str] = Field(None, description="Browser channel")
    args: List[str] = Field(default_factory=list, description="Browser arguments")
    downloads_path: str = Field("downloads", description="Downloads directory")
    headless: bool = Field(DEFAULT_HEADLESS, description="Run in headless mode")
    slow_mo: int = Field(0, description="Slow motion delay in milliseconds")
    viewport: Optional[Dict[str, int]] = Field(None, description="Viewport size")


class DeviceConfig(BaseModel):
    """Device configuration model"""
    viewport: Dict[str, int] = Field(..., description="Viewport dimensions")
    device_scale_factor: float = Field(1.0, description="Device scale factor")
    is_mobile: bool = Field(False, description="Is mobile device")
    has_touch: bool = Field(False, description="Has touch capability")
    user_agent: Optional[str] = Field(None, description="Custom user agent")


class APIConfig(BaseModel):
    """API configuration model"""
    base_url: str = Field(DEFAULT_API_BASE_URL, description="API base URL")
    timeout: int = Field(DEFAULT_API_TIMEOUT, description="API timeout in ms")
    headers: Dict[str, str] = Field(default_factory=dict, description="Default headers")
    auth: Optional[Dict[str, Any]] = Field(None, description="Authentication config")
    retries: int = Field(3, description="Number of retries")
    verify_ssl: bool = Field(True, description="Verify SSL certificates")


class DatabaseConfig(BaseModel):
    """Database configuration model"""
    type: str = Field(DEFAULT_DB_TYPE, description="Database type")
    host: str = Field("localhost", description="Database host")
    port: int = Field(5432, description="Database port")
    name: str = Field(..., description="Database name")
    username: str = Field(..., description="Database username")
    password: str = Field(..., description="Database password")
    charset: Optional[str] = Field("utf8", description="Database charset")
    pool_size: int = Field(10, description="Connection pool size")
    max_overflow: int = Field(20, description="Max overflow connections")
    timeout: int = Field(DEFAULT_DB_QUERY_TIMEOUT, description="Query timeout")


class CloudConfig(BaseModel):
    """Cloud configuration model"""
    provider: str = Field(DEFAULT_CLOUD_PROVIDER, description="Cloud provider")
    region: str = Field("us-east-1", description="Cloud region")
    access_key: Optional[str] = Field(None, description="Access key")
    secret_key: Optional[str] = Field(None, description="Secret key")
    session_token: Optional[str] = Field(None, description="Session token")
    profile: Optional[str] = Field(None, description="AWS profile")


class CICDConfig(BaseModel):
    """CI/CD configuration model"""
    platform: str = Field(DEFAULT_CI_PLATFORM, description="CI/CD platform")
    enabled: bool = Field(True, description="CI/CD enabled")
    parallel: bool = Field(True, description="Run tests in parallel")
    workers: int = Field(DEFAULT_PARALLEL_WORKERS, description="Number of workers")
    timeout: int = Field(3600, description="CI/CD timeout in seconds")
    artifacts: List[str] = Field(default_factory=lambda: ["reports", "logs"], description="Artifacts to upload")


class MonitoringConfig(BaseModel):
    """Monitoring configuration model"""
    enabled: bool = Field(DEFAULT_METRICS_ENABLED, description="Monitoring enabled")
    prometheus_port: int = Field(9090, description="Prometheus port")
    grafana_port: int = Field(3000, description="Grafana port")
    datadog_api_key: Optional[str] = Field(None, description="Datadog API key")
    new_relic_license_key: Optional[str] = Field(None, description="New Relic license key")
    metrics_interval: int = Field(60, description="Metrics collection interval")


class NotificationConfig(BaseModel):
    """Notification configuration model"""
    enabled: bool = Field(DEFAULT_NOTIFICATION_ENABLED, description="Notifications enabled")
    channels: List[str] = Field(default_factory=list, description="Notification channels")
    slack_webhook: Optional[str] = Field(None, description="Slack webhook URL")
    teams_webhook: Optional[str] = Field(None, description="Teams webhook URL")
    discord_webhook: Optional[str] = Field(None, description="Discord webhook URL")
    email_smtp: Optional[str] = Field(None, description="SMTP server")
    email_port: int = Field(587, description="SMTP port")
    email_username: Optional[str] = Field(None, description="Email username")
    email_password: Optional[str] = Field(None, description="Email password")
    email_recipients: List[str] = Field(default_factory=list, description="Email recipients")
    telegram_bot_token: Optional[str] = Field(None, description="Telegram bot token")
    telegram_chat_id: Optional[str] = Field(None, description="Telegram chat ID")


class SecurityConfig(BaseModel):
    """Security configuration model"""
    ssl_verification: bool = Field(True, description="SSL verification")
    certificate_validation: bool = Field(True, description="Certificate validation")
    vulnerability_scanning: bool = Field(DEFAULT_SECURITY_SCAN_ENABLED, description="Vulnerability scanning")
    sql_injection_check: bool = Field(False, description="SQL injection checks")
    xss_check: bool = Field(False, description="XSS checks")
    csrf_check: bool = Field(False, description="CSRF checks")
    headers_check: bool = Field(True, description="Security headers check")
    cookies_check: bool = Field(True, description="Cookie security check")


class PerformanceConfig(BaseModel):
    """Performance configuration model"""
    page_load_threshold: int = Field(DEFAULT_PAGE_LOAD_TIMEOUT, description="Page load threshold (ms)")
    api_response_threshold: int = Field(DEFAULT_API_RESPONSE_TIMEOUT, description="API response threshold (ms)")
    db_query_threshold: int = Field(DEFAULT_DB_QUERY_TIMEOUT, description="DB query threshold (ms)")
    memory_threshold: int = Field(512, description="Memory threshold (MB)")
    cpu_threshold: int = Field(80, description="CPU threshold (%)")
    network_threshold: int = Field(1000, description="Network threshold (KB/s)")
    lighthouse_enabled: bool = Field(False, description="Lighthouse performance audit")


class AccessibilityConfig(BaseModel):
    """Accessibility configuration model"""
    enabled: bool = Field(DEFAULT_ACCESSIBILITY_CHECK_ENABLED, description="Accessibility checks enabled")
    wcag_level: str = Field(DEFAULT_WCAG_LEVEL, description="WCAG compliance level")
    rules: List[str] = Field(default_factory=lambda: ["color-contrast", "keyboard-navigation"], description="Accessibility rules")
    ignore_rules: List[str] = Field(default_factory=list, description="Rules to ignore")
    custom_rules: List[Dict[str, Any]] = Field(default_factory=list, description="Custom accessibility rules")


class VisualConfig(BaseModel):
    """Visual regression configuration model"""
    enabled: bool = Field(DEFAULT_VISUAL_COMPARISON_ENABLED, description="Visual comparison enabled")
    threshold: float = Field(0.01, description="Visual diff threshold")
    diff_color: List[int] = Field(default_factory=lambda: [255, 0, 0], description="Diff highlight color")
    baseline_dir: str = Field("test_data/baselines", description="Baseline images directory")
    diff_dir: str = Field("reports/visual_diffs", description="Diff images directory")
    formats: List[str] = Field(default_factory=lambda: ["png"], description="Supported image formats")


class MobileConfig(BaseModel):
    """Mobile testing configuration model"""
    platform: str = Field(DEFAULT_MOBILE_PLATFORM, description="Mobile platform")
    device_name: str = Field("emulator-5554", description="Device name")
    platform_version: str = Field("12.0", description="Platform version")
    app_package: Optional[str] = Field(None, description="Android app package")
    app_activity: Optional[str] = Field(None, description="Android app activity")
    bundle_id: Optional[str] = Field(None, description="iOS bundle ID")
    automation_name: str = Field("UiAutomator2", description="Automation engine")
    app_path: Optional[str] = Field(None, description="App file path")
    no_reset: bool = Field(False, description="Don't reset app state")
    full_reset: bool = Field(False, description="Full app reset")


class LoggingConfig(BaseModel):
    """Logging configuration model"""
    level: str = Field(DEFAULT_LOG_LEVEL, description="Log level")
    format: str = Field("%(asctime)s - %(name)s - %(levelname)s - %(message)s", description="Log format")
    file_path: Optional[str] = Field(None, description="Log file path")
    max_file_size: str = Field("10 MB", description="Max log file size")
    retention: str = Field("30 days", description="Log retention period")
    console: bool = Field(True, description="Console logging enabled")
    file: bool = Field(True, description="File logging enabled")


class TestDataConfig(BaseModel):
    """Test data configuration model"""
    format: str = Field("json", description="Test data format")
    provider: str = Field("faker", description="Data provider")
    locale: str = Field("en_US", description="Data locale")
    seed: Optional[int] = Field(None, description="Random seed for reproducible data")
    cache_enabled: bool = Field(True, description="Data caching enabled")
    cache_dir: str = Field("test_data/cache", description="Data cache directory")


class RetryConfig(BaseModel):
    """Retry configuration model"""
    max_retries: int = Field(DEFAULT_MAX_RETRIES, description="Maximum retry attempts")
    retry_delay: int = Field(DEFAULT_RETRY_DELAY, description="Delay between retries (ms)")
    backoff_factor: float = Field(2.0, description="Backoff factor for exponential delay")
    retry_on: List[str] = Field(default_factory=lambda: ["AssertionError", "TimeoutError"], description="Exceptions to retry on")
    recovery_enabled: bool = Field(True, description="Auto recovery enabled")


class AdvancedConfig(BaseModel):
    """Advanced features configuration model"""
    ai_assisted_testing: bool = Field(DEFAULT_AI_ASSISTED_TESTING, description="AI-assisted testing enabled")
    ml_based_analysis: bool = Field(False, description="ML-based test analysis")
    auto_healing: bool = Field(DEFAULT_AUTO_HEALING, description="Auto-healing enabled")
    smart_wait: bool = Field(DEFAULT_SMART_WAIT, description="Smart wait enabled")
    predictive_testing: bool = Field(False, description="Predictive test failure detection")
    anomaly_detection: bool = Field(False, description="Anomaly detection enabled")


class FrameworkConfig(BaseSettings):
    """Main framework configuration model"""

    # Environment
    environment: str = Field("development", description="Current environment")
    debug: bool = Field(False, description="Debug mode")

    # Browser
    browser: BrowserConfig = Field(default_factory=lambda: BrowserConfig(**BROWSER_CONFIGS["chromium"]), description="Browser configuration")
    device: DeviceConfig = Field(default_factory=lambda: DeviceConfig(**DEVICE_CONFIGS["desktop"]), description="Device configuration")

    # URLs & Timeouts
    base_url: str = Field("https://example.com", description="Application base URL")
    timeout: int = Field(DEFAULT_TIMEOUT, description="Default timeout in milliseconds")

    # Reporting
    report_format: str = Field(DEFAULT_REPORT_FORMAT, description="Report format")
    screenshot_on_failure: bool = Field(DEFAULT_SCREENSHOT_ON_FAILURE, description="Take screenshot on failure")
    video_on_failure: bool = Field(DEFAULT_VIDEO_ON_FAILURE, description="Record video on failure")

    # Test Execution
    parallel: bool = Field(True, description="Run tests in parallel")
    workers: int = Field(DEFAULT_PARALLEL_WORKERS, description="Number of parallel workers")
    headless: bool = Field(DEFAULT_HEADLESS, description="Run browser in headless mode")

    # API Testing
    api: APIConfig = Field(default_factory=APIConfig, description="API configuration")

    # Database Testing
    database: Optional[DatabaseConfig] = Field(None, description="Database configuration")

    # Cloud Integration
    cloud: CloudConfig = Field(default_factory=CloudConfig, description="Cloud configuration")

    # CI/CD
    cicd: CICDConfig = Field(default_factory=CICDConfig, description="CI/CD configuration")

    # Monitoring
    monitoring: MonitoringConfig = Field(default_factory=MonitoringConfig, description="Monitoring configuration")

    # Notifications
    notifications: NotificationConfig = Field(default_factory=NotificationConfig, description="Notification configuration")

    # Security
    security: SecurityConfig = Field(default_factory=SecurityConfig, description="Security configuration")

    # Performance
    performance: PerformanceConfig = Field(default_factory=PerformanceConfig, description="Performance configuration")

    # Accessibility
    accessibility: AccessibilityConfig = Field(default_factory=AccessibilityConfig, description="Accessibility configuration")

    # Visual Regression
    visual: VisualConfig = Field(default_factory=VisualConfig, description="Visual regression configuration")

    # Mobile Testing
    mobile: MobileConfig = Field(default_factory=MobileConfig, description="Mobile testing configuration")

    # Logging
    logging: LoggingConfig = Field(default_factory=LoggingConfig, description="Logging configuration")

    # Test Data
    test_data: TestDataConfig = Field(default_factory=TestDataConfig, description="Test data configuration")

    # Retry & Recovery
    retry: RetryConfig = Field(default_factory=RetryConfig, description="Retry configuration")

    # Advanced Features
    advanced: AdvancedConfig = Field(default_factory=AdvancedConfig, description="Advanced features configuration")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "allow",  # Allow extra fields from environment
    }

    @validator("environment")
    @classmethod
    def validate_environment(cls, v):
        """Validate environment value"""
        if v not in ENVIRONMENTS:
            raise ValueError(f"Invalid environment: {v}. Must be one of {list(ENVIRONMENTS.keys())}")
        return v

    @validator("browser")
    @classmethod
    def validate_browser(cls, v):
        """Validate browser configuration"""
        if v.name.lower() not in BROWSER_CONFIGS:
            raise ValueError(f"Invalid browser: {v.name}. Must be one of {list(BROWSER_CONFIGS.keys())}")
        return v

    @validator("report_format")
    @classmethod
    def validate_report_format(cls, v):
        """Validate report format"""
        valid_formats = ["html", "json", "xml", "allure", "junit"]
        if v not in valid_formats:
            raise ValueError(f"Invalid report format: {v}. Must be one of {valid_formats}")
        return v

    @model_validator(mode='after')
    def validate_config(self):
        """Validate overall configuration"""
        # Validate mobile configuration if mobile testing is enabled
        if self.mobile and self.mobile.platform not in MOBILE_CONFIGS:
            raise ValueError(f"Invalid mobile platform: {self.mobile.platform}")

        # Validate cloud configuration
        if self.cloud and self.cloud.provider not in CLOUD_CONFIGS:
            raise ValueError(f"Invalid cloud provider: {self.cloud.provider}")

        return self

    def save_to_file(self, filepath: str, format: str = "json"):
        """Save configuration to file"""
        data = self.dict()
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        if format == "json":
            with open(filepath, "w") as f:
                json.dump(data, f, indent=2, default=str)
        elif format in ["yaml", "yml"]:
            with open(filepath, "w") as f:
                yaml.dump(data, f, default_flow_style=False)
        else:
            raise ValueError(f"Unsupported format: {format}")

    @classmethod
    def load_from_file(cls, filepath: str) -> "FrameworkConfig":
        """Load configuration from file"""
        if not Path(filepath).exists():
            raise FileNotFoundError(f"Configuration file not found: {filepath}")

        with open(filepath, "r") as f:
            if filepath.endswith(".json"):
                data = json.load(f)
            elif filepath.endswith((".yaml", ".yml")):
                data = yaml.safe_load(f)
            else:
                raise ValueError(f"Unsupported file format: {filepath}")

        return cls(**data)

    def get_env_config(self) -> Dict[str, Any]:
        """Get environment-specific configuration"""
        env_config_file = f"environments/{self.environment}.json"
        if Path(env_config_file).exists():
            with open(env_config_file, "r") as f:
                return json.load(f)
        return {}

    def merge_env_config(self):
        """Merge environment-specific configuration"""
        env_config = self.get_env_config()
        for key, value in env_config.items():
            if hasattr(self, key):
                setattr(self, key, value)


# Global configuration instance
config = FrameworkConfig()

# Load environment-specific configuration
config.merge_env_config()

# Setup logging based on configuration
logger.remove()  # Remove default handler
if config.logging.console:
    logger.add(
        lambda msg: print(msg, end=""),
        level=config.logging.level,
        format=config.logging.format,
        colorize=True,
    )

if config.logging.file and config.logging.file_path:
    Path(config.logging.file_path).parent.mkdir(parents=True, exist_ok=True)
    logger.add(
        config.logging.file_path,
        level=config.logging.level,
        format=config.logging.format,
        rotation=config.logging.max_file_size,
        retention=config.logging.retention,
        encoding="utf-8",
    )

logger.info(f"Framework configuration loaded for environment: {config.environment}")
logger.info(f"Browser: {config.browser.name}, Headless: {config.headless}")
logger.info(f"Base URL: {config.base_url}, Timeout: {config.timeout}ms")

__all__ = [
    "FrameworkConfig",
    "BrowserConfig",
    "DeviceConfig",
    "APIConfig",
    "DatabaseConfig",
    "CloudConfig",
    "CICDConfig",
    "MonitoringConfig",
    "NotificationConfig",
    "SecurityConfig",
    "PerformanceConfig",
    "AccessibilityConfig",
    "VisualConfig",
    "MobileConfig",
    "LoggingConfig",
    "TestDataConfig",
    "RetryConfig",
    "AdvancedConfig",
    "config",
]