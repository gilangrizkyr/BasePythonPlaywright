"""
Professional Utilities
======================

Advanced utility functions for Playwright automation with modern features,
data generation, file handling, and enterprise-grade capabilities.
"""

import asyncio
import json
import csv
import time
import random
import string
import hashlib
import base64
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Callable, TypeVar, Iterator
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from urllib.parse import urlparse, urljoin, parse_qs, urlencode
from functools import wraps, lru_cache
from contextlib import asynccontextmanager
import aiofiles
import aiohttp

from faker import Faker
from loguru import logger
from playwright.async_api import Page, Locator, ElementHandle, BrowserContext

from core.config import config


T = TypeVar('T')
faker = Faker()


@dataclass
class TestData:
    """Test data container"""
    name: str
    data: Dict[str, Any]
    tags: List[str] = field(default_factory=list)
    environment: str = "all"


@dataclass
class FileInfo:
    """File information"""
    path: Path
    size: int
    modified: datetime
    hash: str


class DataGenerator:
    """Advanced test data generator"""

    def __init__(self, locale: str = "en_US"):
        self.faker = Faker(locale)

    def generate_user(self) -> Dict[str, Any]:
        """Generate realistic user data"""
        return {
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name(),
            "email": self.faker.email(),
            "phone": self.faker.phone_number(),
            "address": {
                "street": self.faker.street_address(),
                "city": self.faker.city(),
                "state": self.faker.state(),
                "zip_code": self.faker.zipcode(),
                "country": self.faker.country(),
            },
            "birth_date": self.faker.date_of_birth(minimum_age=18, maximum_age=80).isoformat(),
            "company": self.faker.company(),
            "job_title": self.faker.job(),
        }

    def generate_credit_card(self, card_type: str = "visa") -> Dict[str, Any]:
        """Generate credit card data"""
        return {
            "number": self.faker.credit_card_number(card_type=card_type),
            "expiration_date": self.faker.credit_card_expire(),
            "cvv": self.faker.credit_card_security_code(),
            "cardholder_name": self.faker.name(),
            "type": card_type.upper(),
        }

    def generate_product(self) -> Dict[str, Any]:
        """Generate product data"""
        return {
            "name": self.faker.commerce.product_name(),
            "price": float(self.faker.commerce.price()),
            "category": self.faker.commerce.department(),
            "description": self.faker.text(max_nb_chars=200),
            "sku": self.faker.uuid4(),
            "in_stock": self.faker.boolean(chance_of_getting_true=80),
            "rating": round(random.uniform(1, 5), 1),
        }

    def generate_random_string(self, length: int = 10, chars: str = string.ascii_letters + string.digits) -> str:
        """Generate random string"""
        return ''.join(random.choice(chars) for _ in range(length))

    def generate_random_email(self, domain: Optional[str] = None) -> str:
        """Generate random email"""
        if domain:
            return f"{self.generate_random_string(8).lower()}@{domain}"
        return self.faker.email()

    def generate_random_phone(self, country_code: str = "+1") -> str:
        """Generate random phone number"""
        return f"{country_code} {self.faker.phone_number()}"

    def generate_random_date(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
        """Generate random date"""
        if start_date and end_date:
            start = datetime.fromisoformat(start_date)
            end = datetime.fromisoformat(end_date)
            random_date = start + timedelta(days=random.randint(0, (end - start).days))
            return random_date.isoformat()
        return self.faker.date_this_year().isoformat()

    def generate_test_data_batch(self, count: int, data_type: str = "user") -> List[Dict[str, Any]]:
        """Generate batch of test data"""
        generators = {
            "user": self.generate_user,
            "product": self.generate_product,
            "credit_card": self.generate_credit_card,
        }

        generator = generators.get(data_type, self.generate_user)
        return [generator() for _ in range(count)]


class FileManager:
    """Advanced file management utilities"""

    @staticmethod
    async def read_json_file(file_path: Union[str, Path]) -> Dict[str, Any]:
        """Read JSON file asynchronously"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        async with aiofiles.open(path, 'r', encoding='utf-8') as f:
            content = await f.read()
            return json.loads(content)

    @staticmethod
    async def write_json_file(file_path: Union[str, Path], data: Dict[str, Any], indent: int = 2) -> None:
        """Write JSON file asynchronously"""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(path, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(data, indent=indent, ensure_ascii=False))

    @staticmethod
    async def read_csv_file(file_path: Union[str, Path]) -> List[Dict[str, str]]:
        """Read CSV file asynchronously"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        async with aiofiles.open(path, 'r', encoding='utf-8') as f:
            content = await f.read()
            reader = csv.DictReader(content.splitlines())
            return list(reader)

    @staticmethod
    async def write_csv_file(file_path: Union[str, Path], data: List[Dict[str, Any]], fieldnames: Optional[List[str]] = None) -> None:
        """Write CSV file asynchronously"""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if not fieldnames and data:
            fieldnames = list(data[0].keys())

        async with aiofiles.open(path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            await f.write(','.join(fieldnames) + '\n')

            for row in data:
                csv_row = ','.join(str(row.get(field, '')) for field in fieldnames)
                await f.write(csv_row + '\n')

    @staticmethod
    def get_file_info(file_path: Union[str, Path]) -> FileInfo:
        """Get file information"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        stat = path.stat()
        file_hash = hashlib.md5(path.read_bytes()).hexdigest()

        return FileInfo(
            path=path,
            size=stat.st_size,
            modified=datetime.fromtimestamp(stat.st_mtime),
            hash=file_hash
        )

    @staticmethod
    def find_files_by_pattern(directory: Union[str, Path], pattern: str) -> List[Path]:
        """Find files by glob pattern"""
        path = Path(directory)
        return list(path.glob(pattern))

    @staticmethod
    async def copy_file(src: Union[str, Path], dst: Union[str, Path]) -> None:
        """Copy file asynchronously"""
        src_path = Path(src)
        dst_path = Path(dst)
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(src_path, 'rb') as src_f:
            async with aiofiles.open(dst_path, 'wb') as dst_f:
                await dst_f.write(await src_f.read())

    @staticmethod
    async def move_file(src: Union[str, Path], dst: Union[str, Path]) -> None:
        """Move file"""
        await FileManager.copy_file(src, dst)
        Path(src).unlink()


class WebUtilities:
    """Web-related utility functions"""

    @staticmethod
    def extract_domain(url: str) -> str:
        """Extract domain from URL"""
        parsed = urlparse(url)
        return parsed.netloc

    @staticmethod
    def build_url(base_url: str, path: str, params: Optional[Dict[str, Any]] = None) -> str:
        """Build URL with path and query parameters"""
        url = urljoin(base_url.rstrip('/') + '/', path.lstrip('/'))
        if params:
            parsed = urlparse(url)
            query_params = parse_qs(parsed.query)
            query_params.update(params)
            url = url.replace(parsed.query, urlencode(query_params, doseq=True))
        return url

    @staticmethod
    def parse_query_params(url: str) -> Dict[str, List[str]]:
        """Parse query parameters from URL"""
        parsed = urlparse(url)
        return parse_qs(parsed.query)

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    @staticmethod
    def generate_random_user_agent() -> str:
        """Generate random user agent string"""
        browsers = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        ]
        return random.choice(browsers)

    @staticmethod
    async def wait_for_page_load(page: Page, timeout: int = 30000) -> None:
        """Wait for page to fully load"""
        await page.wait_for_load_state("networkidle", timeout=timeout)

    @staticmethod
    async def wait_for_element_visible(page: Page, selector: str, timeout: int = 10000) -> Locator:
        """Wait for element to be visible"""
        locator = page.locator(selector)
        await locator.wait_for(state="visible", timeout=timeout)
        return locator

    @staticmethod
    async def take_full_page_screenshot(page: Page, filename: str) -> str:
        """Take full page screenshot"""
        path = Path(config.REPORTS_DIR) / "screenshots" / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        await page.screenshot(path=str(path), full_page=True)
        return str(path)

    @staticmethod
    async def get_page_performance_metrics(page: Page) -> Dict[str, Any]:
        """Get page performance metrics"""
        return await page.evaluate("""
            () => {
                const timing = performance.getEntriesByType('navigation')[0];
                const paint = performance.getEntriesByType('paint');
                const resources = performance.getEntriesByType('resource');

                return {
                    domContentLoaded: timing.domContentLoadedEventEnd - timing.domContentLoadedEventStart,
                    loadComplete: timing.loadEventEnd - timing.loadEventStart,
                    firstPaint: paint.find(p => p.name === 'first-paint')?.startTime || 0,
                    firstContentfulPaint: paint.find(p => p.name === 'first-contentful-paint')?.startTime || 0,
                    resourcesLoaded: resources.length,
                    totalResourceSize: resources.reduce((sum, r) => sum + (r.transferSize || 0), 0)
                };
            }
        """)


class APIUtilities:
    """API testing utilities"""

    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url.rstrip('/')
        self.session: Optional[aiohttp.ClientSession] = None
        self.headers = headers or {}

    async def setup_session(self) -> None:
        """Setup HTTP session"""
        if self.session is None:
            self.session = aiohttp.ClientSession(
                base_url=self.base_url,
                headers=self.headers,
                timeout=aiohttp.ClientTimeout(total=config.api.timeout / 1000)
            )

    async def teardown_session(self) -> None:
        """Teardown HTTP session"""
        if self.session:
            await self.session.close()
            self.session = None

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

                return result

        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"API request failed: {method} {endpoint} ({duration:.2f}s) - {e}")
            raise

    async def get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """GET request"""
        return await self.make_request("GET", endpoint, **kwargs)

    async def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """POST request"""
        if data:
            kwargs["json"] = data
        return await self.make_request("POST", endpoint, **kwargs)

    async def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """PUT request"""
        if data:
            kwargs["json"] = data
        return await self.make_request("PUT", endpoint, **kwargs)

    async def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """DELETE request"""
        return await self.make_request("DELETE", endpoint, **kwargs)

    @staticmethod
    def validate_json_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
        """Validate JSON against schema"""
        # Basic schema validation - could be enhanced with jsonschema library
        try:
            for key, expected_type in schema.items():
                if key in data:
                    if not isinstance(data[key], expected_type):
                        return False
            return True
        except:
            return False


class DatabaseUtilities:
    """Database testing utilities"""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None

    async def connect(self) -> None:
        """Connect to database"""
        # Database connection logic would go here
        # Implementation depends on database type
        pass

    async def disconnect(self) -> None:
        """Disconnect from database"""
        if self.connection:
            await self.connection.close()

    async def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Execute database query"""
        # Query execution logic would go here
        return []

    async def insert_data(self, table: str, data: Dict[str, Any]) -> int:
        """Insert data into table"""
        # Insert logic would go here
        return 0

    async def update_data(self, table: str, data: Dict[str, Any], where_clause: str) -> int:
        """Update data in table"""
        # Update logic would go here
        return 0

    async def delete_data(self, table: str, where_clause: str) -> int:
        """Delete data from table"""
        # Delete logic would go here
        return 0


class PerformanceUtilities:
    """Performance testing utilities"""

    @staticmethod
    def measure_execution_time(func: Callable) -> Callable:
        """Decorator to measure function execution time"""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            logger.debug(f"{func.__name__} executed in {duration:.2f}s")
            return result, duration
        return wrapper

    @staticmethod
    def calculate_average_response_time(times: List[float]) -> float:
        """Calculate average response time"""
        return sum(times) / len(times) if times else 0

    @staticmethod
    def calculate_percentile(times: List[float], percentile: float) -> float:
        """Calculate percentile from list of times"""
        if not times:
            return 0
        times_sorted = sorted(times)
        index = int(len(times_sorted) * percentile / 100)
        return times_sorted[min(index, len(times_sorted) - 1)]

    @staticmethod
    def check_performance_threshold(actual: float, threshold: float, metric_name: str) -> bool:
        """Check if performance metric meets threshold"""
        if actual > threshold:
            logger.warning(f"Performance threshold exceeded for {metric_name}: {actual:.2f} > {threshold:.2f}")
            return False
        return True


class SecurityUtilities:
    """Security testing utilities"""

    @staticmethod
    def hash_string(text: str, algorithm: str = "sha256") -> str:
        """Hash string using specified algorithm"""
        if algorithm == "md5":
            return hashlib.md5(text.encode()).hexdigest()
        elif algorithm == "sha1":
            return hashlib.sha1(text.encode()).hexdigest()
        else:
            return hashlib.sha256(text.encode()).hexdigest()

    @staticmethod
    def encode_base64(text: str) -> str:
        """Encode string to base64"""
        return base64.b64encode(text.encode()).decode()

    @staticmethod
    def decode_base64(encoded: str) -> str:
        """Decode base64 string"""
        return base64.b64decode(encoded).decode()

    @staticmethod
    def generate_random_password(length: int = 12) -> str:
        """Generate secure random password"""
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choice(chars) for _ in range(length))

    @staticmethod
    def check_password_strength(password: str) -> Dict[str, Any]:
        """Check password strength"""
        score = 0
        feedback = []

        if len(password) >= 8:
            score += 1
        else:
            feedback.append("Password should be at least 8 characters long")

        if re.search(r'[A-Z]', password):
            score += 1
        else:
            feedback.append("Password should contain uppercase letters")

        if re.search(r'[a-z]', password):
            score += 1
        else:
            feedback.append("Password should contain lowercase letters")

        if re.search(r'\d', password):
            score += 1
        else:
            feedback.append("Password should contain digits")

        if re.search(r'[!@#$%^&*]', password):
            score += 1
        else:
            feedback.append("Password should contain special characters")

        strength = "weak"
        if score >= 4:
            strength = "strong"
        elif score >= 3:
            strength = "medium"

        return {
            "score": score,
            "strength": strength,
            "feedback": feedback
        }


# Global instances
data_generator = DataGenerator()
file_manager = FileManager()
web_utils = WebUtilities()
performance_utils = PerformanceUtilities()
security_utils = SecurityUtilities()


__all__ = [
    "DataGenerator",
    "FileManager",
    "WebUtilities",
    "APIUtilities",
    "DatabaseUtilities",
    "PerformanceUtilities",
    "SecurityUtilities",
    "TestData",
    "FileInfo",
    "data_generator",
    "file_manager",
    "web_utils",
    "performance_utils",
    "security_utils",
]