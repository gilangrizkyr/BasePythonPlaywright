# Professional Playwright Framework Dockerfile
# Multi-stage build for optimized image size

# =============================================================================
# BASE STAGE - Python and system dependencies
# =============================================================================
FROM python:3.12-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    # Core dependencies
    curl \
    wget \
    gnupg \
    software-properties-common \
    # Playwright dependencies
    libnss3 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libxss1 \
    libasound2 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcb-dri3-0 \
    libxcb-shm0 \
    libxcb1 \
    # Additional utilities
    git \
    vim \
    nano \
    htop \
    procps \
    net-tools \
    dnsutils \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r playwright && useradd -r -g playwright -s /bin/bash playwright

# Set working directory
WORKDIR /app

# Change ownership of working directory
RUN chown -R playwright:playwright /app

# Switch to non-root user
USER playwright

# =============================================================================
# DEPENDENCIES STAGE - Install Python dependencies
# =============================================================================
FROM base as dependencies

# Copy requirements file
COPY --chown=playwright:playwright requirements.txt .

# Install Python dependencies
RUN pip install --user --no-cache-dir -r requirements.txt

# =============================================================================
# PLAYWRIGHT STAGE - Install Playwright browsers
# =============================================================================
FROM dependencies as playwright-setup

# Install Playwright browsers
RUN playwright install --with-deps chromium firefox webkit

# Verify installation
RUN python -c "from playwright.sync_api import sync_playwright; print('Playwright installed successfully')"

# =============================================================================
# DEVELOPMENT STAGE - For development environment
# =============================================================================
FROM playwright-setup as development

# Copy source code
COPY --chown=playwright:playwright . .

# Create necessary directories
RUN mkdir -p reports/screenshots reports/videos reports/logs reports/html-report

# Set environment variables for development
ENV ENVIRONMENT=development \
    LOG_LEVEL=DEBUG \
    HEADLESS=false

# Expose port for any web server (if needed)
EXPOSE 8000

# Default command for development
CMD ["python", "-c", "print('Playwright Framework Development Environment Ready')"]

# =============================================================================
# TESTING STAGE - For CI/CD test execution
# =============================================================================
FROM playwright-setup as testing

# Copy source code
COPY --chown=playwright:playwright . .

# Create necessary directories
RUN mkdir -p reports/screenshots reports/videos reports/logs reports/html-report reports/junit-xml reports/allure-results

# Set environment variables for testing
ENV ENVIRONMENT=testing \
    LOG_LEVEL=INFO \
    HEADLESS=true \
    PARALLEL_WORKERS=2

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Default command for testing
CMD ["python", "-m", "pytest", "tests/", "--tb=short", "--junitxml=reports/junit-xml/results.xml"]

# =============================================================================
# PRODUCTION STAGE - Optimized for production use
# =============================================================================
FROM playwright-setup as production

# Copy source code (excluding development files)
COPY --chown=playwright:playwright core/ ./core/
COPY --chown=playwright:playwright decorators/ ./decorators/
COPY --chown=playwright:playwright pages/ ./pages/
COPY --chown=playwright:playwright tests/ ./tests/
COPY --chown=playwright:playwright pytest.ini .
COPY --chown=playwright:playwright requirements.txt .

# Create necessary directories
RUN mkdir -p reports/screenshots reports/videos reports/logs reports/html-report

# Set environment variables for production
ENV ENVIRONMENT=production \
    LOG_LEVEL=WARNING \
    HEADLESS=true \
    PARALLEL_WORKERS=4

# Add metadata labels
LABEL maintainer="Playwright Framework Team" \
      version="1.0.0" \
      description="Professional Playwright Automation Framework"

# Health check
HEALTHCHECK --interval=60s --timeout=30s --start-period=10s --retries=3 \
    CMD python -c "from core.base import BaseTest; print('Framework healthy')" || exit 1

# Default command for production
CMD ["python", "core/runner.py"]

# =============================================================================
# MULTI-STAGE TARGETS
# =============================================================================

# Default target is production
FROM production

# For development, use: docker build --target development -t playwright-dev .
# For testing, use: docker build --target testing -t playwright-test .
# For production, use: docker build -t playwright-prod .