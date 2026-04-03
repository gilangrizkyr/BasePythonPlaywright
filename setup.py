"""
Setup script for the Professional Playwright Automation Framework
=================================================================

This setup script configures the framework for distribution and development.
"""

import os
import re
from pathlib import Path
from setuptools import setup, find_packages


def read_file(filename):
    """Read file content"""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()


def get_version():
    """Extract version from core/__init__.py"""
    init_file = Path(__file__).parent / 'core' / '__init__.py'
    content = read_file(init_file)
    version_match = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', content, re.MULTILINE)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


def get_long_description():
    """Get long description from README.md"""
    readme = Path(__file__).parent / 'README.md'
    if readme.exists():
        return read_file(readme)
    return ''


def get_requirements():
    """Get requirements from requirements.txt"""
    requirements_file = Path(__file__).parent / 'requirements.txt'
    if requirements_file.exists():
        requirements = []
        for line in read_file(requirements_file).splitlines():
            line = line.strip()
            if line and not line.startswith('#'):
                requirements.append(line)
        return requirements
    return []


# Package metadata
PACKAGE_NAME = 'playwright-automation-framework'
VERSION = get_version()
DESCRIPTION = 'Professional Python Playwright Automation Framework with Enterprise Features'
LONG_DESCRIPTION = get_long_description()
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'
AUTHOR = 'Professional Automation Team'
AUTHOR_EMAIL = 'automation@company.com'
URL = 'https://github.com/company/playwright-automation-framework'
LICENSE = 'MIT'

# Classifiers for PyPI
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Intended Audience :: Information Technology',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    'Topic :: Software Development :: Testing',
    'Topic :: Software Development :: Quality Assurance',
    'Topic :: Internet :: WWW/HTTP :: Browsers',
]

# Keywords
KEYWORDS = [
    'playwright',
    'automation',
    'testing',
    'selenium',
    'web-testing',
    'e2e-testing',
    'api-testing',
    'performance-testing',
    'accessibility-testing',
    'visual-regression',
    'ci-cd',
    'pytest',
    'async',
    'enterprise',
    'professional',
]

# Requirements
INSTALL_REQUIRES = get_requirements()

# Extra requirements
EXTRAS_REQUIRE = {
    'dev': [
        'black>=22.0.0',
        'flake8>=4.0.0',
        'isort>=5.10.0',
        'mypy>=0.950',
        'pre-commit>=2.17.0',
        'pytest-cov>=3.0.0',
        'pytest-xdist>=2.5.0',
        'pytest-html>=3.1.0',
        'pytest-asyncio>=0.18.0',
        'pytest-playwright>=0.3.0',
        'pytest-benchmark>=4.0.0',
        'pytest-mock>=3.7.0',
    ],
    'docs': [
        'sphinx>=4.5.0',
        'sphinx-rtd-theme>=1.0.0',
        'myst-parser>=0.17.0',
    ],
    'monitoring': [
        'prometheus-client>=0.14.0',
        'grafana-api>=1.0.3',
        'influxdb-client>=1.28.0',
    ],
    'database': [
        'psycopg2-binary>=2.9.0',
        'pymongo>=4.1.0',
        'redis>=4.3.0',
        'sqlalchemy>=1.4.0',
    ],
    'mobile': [
        'Appium-Python-Client>=2.7.0',
        'selenium>=4.1.0',
    ],
    'cloud': [
        'boto3>=1.24.0',
        'azure-storage-blob>=12.13.0',
        'google-cloud-storage>=2.4.0',
    ],
    'security': [
        'bandit>=1.7.0',
        'safety>=2.2.0',
    ],
    'visual': [
        'Pillow>=9.0.0',
        'opencv-python>=4.6.0',
        'pixelmatch>=0.3.0',
    ],
    'api': [
        'requests>=2.28.0',
        'aiohttp>=3.8.0',
        'httpx>=0.23.0',
    ],
    'all': [],  # Will be populated below
}

# Add all extras to 'all'
for extra_deps in EXTRAS_REQUIRE.values():
    EXTRAS_REQUIRE['all'].extend(extra_deps)

# Remove duplicates from 'all'
EXTRAS_REQUIRE['all'] = list(set(EXTRAS_REQUIRE['all']))

# Package configuration
setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    packages=find_packages(exclude=['tests*', 'docs*', 'examples*']),
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'playwright-framework=core.runner:main',
            'pf-run=run_tests:main',
        ],
        'pytest11': [
            'playwright_framework=tests.conftest',
        ],
    },
    project_urls={
        'Documentation': 'https://playwright-framework.readthedocs.io/',
        'Source': 'https://github.com/company/playwright-automation-framework',
        'Tracker': 'https://github.com/company/playwright-automation-framework/issues',
        'Changelog': 'https://github.com/company/playwright-automation-framework/blob/main/CHANGELOG.md',
    },
    zip_safe=False,
)
