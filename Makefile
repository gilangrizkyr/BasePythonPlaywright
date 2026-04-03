# Professional Playwright Framework Makefile
# ===========================================

.PHONY: help install setup test test-parallel test-smoke test-regression clean lint format docker-build docker-run docker-test docs

# Default target
help: ## Show this help message
	@echo "Professional Playwright Automation Framework"
	@echo "=========================================="
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

# =============================================================================
# SETUP AND INSTALLATION
# =============================================================================

install: ## Install Python dependencies
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt

setup: install ## Complete setup including Playwright browsers
	@echo "Setting up Playwright browsers..."
	playwright install
	@echo "Creating necessary directories..."
	mkdir -p reports/screenshots reports/videos reports/logs
	@echo "Setup complete!"

setup-dev: setup ## Setup for development environment
	@echo "Setting up development environment..."
	cp .env.example .env
	@echo "Please edit .env file with your configuration"

# =============================================================================
# TESTING
# =============================================================================

test: ## Run all tests
	@echo "Running all tests..."
	python run_tests.py

test-parallel: ## Run tests in parallel
	@echo "Running tests in parallel..."
	python run_tests.py --parallel 4

test-smoke: ## Run smoke tests only
	@echo "Running smoke tests..."
	python run_tests.py --tags smoke

test-regression: ## Run regression tests only
	@echo "Running regression tests..."
	python run_tests.py --tags regression

test-e2e: ## Run end-to-end tests
	@echo "Running E2E tests..."
	python run_tests.py --tags e2e

test-api: ## Run API tests only
	@echo "Running API tests..."
	python run_tests.py --tags api

test-ui: ## Run UI tests only
	@echo "Running UI tests..."
	python run_tests.py --tags ui

test-performance: ## Run performance tests
	@echo "Running performance tests..."
	python run_tests.py --tags performance --performance

test-accessibility: ## Run accessibility tests
	@echo "Running accessibility tests..."
	python run_tests.py --tags accessibility --accessibility

test-security: ## Run security tests
	@echo "Running security tests..."
	python run_tests.py --tags security --security

test-visual: ## Run visual regression tests
	@echo "Running visual regression tests..."
	python run_tests.py --tags visual

# =============================================================================
# BROWSER SPECIFIC TESTS
# =============================================================================

test-chromium: ## Run tests with Chromium
	@echo "Running tests with Chromium..."
	python run_tests.py --browser chromium

test-firefox: ## Run tests with Firefox
	@echo "Running tests with Firefox..."
	python run_tests.py --browser firefox

test-webkit: ## Run tests with WebKit
	@echo "Running tests with WebKit..."
	python run_tests.py --browser webkit

# =============================================================================
# DEBUG AND DEVELOPMENT
# =============================================================================

test-debug: ## Run tests in debug mode
	@echo "Running tests in debug mode..."
	python run_tests.py --debug --headed

test-headed: ## Run tests in headed mode (visible browser)
	@echo "Running tests in headed mode..."
	python run_tests.py --headed

test-dry-run: ## Show what tests would be run without executing
	@echo "Dry run - showing test discovery..."
	python run_tests.py --dry-run

# =============================================================================
# QUALITY ASSURANCE
# =============================================================================

lint: ## Run linting checks
	@echo "Running linting checks..."
	flake8 core/ decorators/ pages/ tests/ --max-line-length=120 --extend-ignore=E203,W503
	@echo "Linting complete!"

format: ## Format code with black
	@echo "Formatting code..."
	black core/ decorators/ pages/ tests/ --line-length=120
	isort core/ decorators/ pages/ tests/

type-check: ## Run type checking with mypy
	@echo "Running type checking..."
	mypy core/ decorators/ pages/ --ignore-missing-imports

quality: lint format type-check ## Run all quality checks

# =============================================================================
# REPORTING
# =============================================================================

report-html: ## Generate HTML report
	@echo "Generating HTML report..."
	python run_tests.py --report html

report-allure: ## Generate Allure report
	@echo "Generating Allure report..."
	python run_tests.py --report allure
	allure serve reports/allure-results

report-junit: ## Generate JUnit XML report
	@echo "Generating JUnit XML report..."
	python run_tests.py --report junit

reports: report-html report-junit ## Generate all reports

# =============================================================================
# DOCKER
# =============================================================================

docker-build: ## Build Docker image
	@echo "Building Docker image..."
	docker build -t playwright-framework .

docker-build-dev: ## Build development Docker image
	@echo "Building development Docker image..."
	docker build --target development -t playwright-framework:dev .

docker-run: ## Run Docker container
	@echo "Running Docker container..."
	docker run --rm -v $(PWD)/reports:/app/reports playwright-framework

docker-test: ## Run tests in Docker
	@echo "Running tests in Docker..."
	docker run --rm -v $(PWD)/reports:/app/reports playwright-framework python run_tests.py

docker-compose-up: ## Start all services with docker-compose
	@echo "Starting services with docker-compose..."
	docker-compose up -d

docker-compose-down: ## Stop all services
	@echo "Stopping services..."
	docker-compose down

docker-compose-test: ## Run tests with full docker-compose environment
	@echo "Running tests with docker-compose..."
	docker-compose run --rm playwright-runner

# =============================================================================
# CLEANUP
# =============================================================================

clean: ## Clean up generated files
	@echo "Cleaning up generated files..."
	rm -rf reports/ logs/ .pytest_cache/ __pycache__/ .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

clean-all: clean ## Clean up everything including virtual environment
	@echo "Cleaning up everything..."
	rm -rf venv/ .venv/ env/ .env node_modules/
	docker system prune -f

# =============================================================================
# UTILITIES
# =============================================================================

deps-update: ## Update Python dependencies
	@echo "Updating dependencies..."
	pip install --upgrade pip
	pip install --upgrade -r requirements.txt

deps-freeze: ## Freeze current dependencies
	@echo "Freezing dependencies..."
	pip freeze > requirements.txt

env-check: ## Check environment setup
	@echo "Checking environment..."
	python --version
	pip --version
	playwright --version
	which python
	which pip

info: ## Show project information
	@echo "Professional Playwright Automation Framework"
	@echo "=========================================="
	@echo "Python version: $$(python --version)"
	@echo "Playwright version: $$(playwright --version 2>/dev/null || echo 'Not installed')"
	@echo "Working directory: $$(pwd)"
	@echo "Reports directory: reports/"
	@echo "Environment: $$(cat .env | grep ENVIRONMENT | cut -d'=' -f2 || echo 'Not set')"

# =============================================================================
# CI/CD
# =============================================================================

ci-setup: ## Setup for CI environment
	@echo "Setting up CI environment..."
	pip install -r requirements.txt
	playwright install --with-deps

ci-test: ci-setup ## Run tests in CI environment
	@echo "Running CI tests..."
	python run_tests.py --report all --parallel 2

ci-smoke: ci-setup ## Run smoke tests in CI
	@echo "Running CI smoke tests..."
	python run_tests.py --tags smoke --report junit

# =============================================================================
# DEVELOPMENT HELPERS
# =============================================================================

new-test: ## Create a new test file template
	@echo "Creating new test template..."
	@read -p "Enter test name: " testname; \
	echo "from core.base import BaseTest"; \
	echo ""; \
	echo ""; \
	echo "class Test$${testname^}(BaseTest):"; \
	echo "    \"\"\"Test $${testname}\"\"\""; \
	echo ""; \
	echo "    async def run_test(self):"; \
	echo "        \"\"\"Run the test\"\"\""; \
	echo "        # Your test code here"; \
	echo "        pass"; \
	} > "tests/test_$${testname}.py"; \
	echo "Created tests/test_$${testname}.py"

new-page: ## Create a new page object template
	@echo "Creating new page template..."
	@read -p "Enter page name: " pagename; \
	echo "from core.base import BasePage"; \
	echo ""; \
	echo ""; \
	echo "class $${pagename^}Page(BasePage):"; \
	echo "    \"\"\"$${pagename^} page object\"\"\""; \
	echo ""; \
	echo "    def _init_elements(self):"; \
	echo "        \"\"\"Initialize page elements\"\"\""; \
	echo "        # Add element definitions here"; \
	echo "        pass"; \
	echo ""; \
	echo "    def get_page_elements(self):"; \
	echo "        \"\"\"Get page elements mapping\"\"\""; \
	echo "        return {}"; \
	echo ""; \
	echo "    async def is_loaded(self):"; \
	echo "        \"\"\"Check if page is loaded\"\"\""; \
	echo "        return True"; \
	} > "pages/$${pagename}.py"; \
	echo "Created pages/$${pagename}.py"

# =============================================================================
# MONITORING AND DEBUGGING
# =============================================================================

monitor: ## Start monitoring dashboard
	@echo "Starting monitoring dashboard..."
	docker-compose up -d playwright-grafana playwright-prometheus
	@echo "Grafana: http://localhost:3001 (admin/admin)"
	@echo "Prometheus: http://localhost:9090"

logs: ## Show recent test logs
	@echo "Recent test logs:"
	@find reports/logs -name "*.log" -type f -exec ls -la {} \; 2>/dev/null | head -10 || echo "No logs found"

tail-logs: ## Tail the latest log file
	@echo "Tailing latest log file..."
	@latest_log=$$(find reports/logs -name "*.log" -type f -exec ls -t {} \; | head -1); \
	if [ -n "$$latest_log" ]; then \
		tail -f $$latest_log; \
	else \
		echo "No log files found"; \
	fi

# =============================================================================
# HELP
# =============================================================================

help-advanced: ## Show advanced commands
	@echo "Advanced Commands:"
	@echo "=================="
	@echo "Development:"
	@echo "  make new-test          - Create new test template"
	@echo "  make new-page          - Create new page object template"
	@echo "  make monitor           - Start monitoring dashboard"
	@echo ""
	@echo "Quality Assurance:"
	@echo "  make quality           - Run all quality checks"
	@echo "  make lint              - Run linting only"
	@echo "  make format            - Format code only"
	@echo "  make type-check        - Run type checking only"
	@echo ""
	@echo "Docker Advanced:"
	@echo "  make docker-build-dev  - Build development image"
	@echo "  make docker-compose-up - Start full environment"
	@echo ""
	@echo "Debugging:"
	@echo "  make test-debug        - Run tests in debug mode"
	@echo "  make test-headed       - Run tests with visible browser"
	@echo "  make logs              - Show recent logs"
	@echo "  make tail-logs         - Tail latest log file"