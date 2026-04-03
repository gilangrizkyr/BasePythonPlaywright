#!/usr/bin/env python3
"""
Professional Test Runner Script
===============================

Command-line interface for running Playwright tests with various options.
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.runner import AdvancedTestRunner, TestSuiteConfig
from core.config import config


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Professional Playwright Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py                          # Run all tests
  python run_tests.py --tags smoke regression  # Run specific tags
  python run_tests.py --browser firefox        # Use Firefox browser
  python run_tests.py --parallel 4             # Run with 4 parallel workers
  python run_tests.py --headless               # Run in headless mode
  python run_tests.py --report html            # Generate HTML report
  python run_tests.py --config custom_config.json  # Use custom config
  python run_tests.py --test tests/test_login.py   # Run specific test file
        """
    )

    # Test selection
    parser.add_argument(
        '--test', '-t',
        nargs='+',
        help='Specific test files or directories to run'
    )

    parser.add_argument(
        '--tags', '--marker', '-m',
        nargs='+',
        help='Test markers/tags to run (e.g., smoke regression e2e)'
    )

    # Browser options
    parser.add_argument(
        '--browser', '-b',
        choices=['chromium', 'firefox', 'webkit'],
        default=config.browser.name,
        help='Browser to use for testing'
    )

    # Execution options
    parser.add_argument(
        '--parallel', '-n',
        type=int,
        default=config.parallel.max_workers,
        help='Number of parallel workers'
    )

    parser.add_argument(
        '--headless',
        action='store_true',
        default=config.headless,
        help='Run browser in headless mode'
    )

    parser.add_argument(
        '--headed',
        action='store_true',
        help='Run browser in headed mode (overrides headless)'
    )

    # Reporting options
    parser.add_argument(
        '--report', '-r',
        choices=['html', 'json', 'junit', 'allure', 'all'],
        default='all',
        help='Report format to generate'
    )

    parser.add_argument(
        '--report-dir',
        default=config.REPORTS_DIR,
        help='Directory to store reports'
    )

    # Configuration options
    parser.add_argument(
        '--config',
        help='Path to custom configuration file'
    )

    parser.add_argument(
        '--env',
        choices=['development', 'staging', 'production', 'testing'],
        default='testing',
        help='Environment to run tests in'
    )

    # Debug options
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode with verbose logging'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be run without executing tests'
    )

    # Performance options
    parser.add_argument(
        '--performance',
        action='store_true',
        help='Enable performance monitoring'
    )

    parser.add_argument(
        '--accessibility',
        action='store_true',
        help='Enable accessibility testing'
    )

    parser.add_argument(
        '--security',
        action='store_true',
        help='Enable security scanning'
    )

    # Output options
    parser.add_argument(
        '--output', '-o',
        help='Output file for results'
    )

    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Quiet mode, minimal output'
    )

    return parser.parse_args()


def load_custom_config(config_path: str) -> Dict[str, Any]:
    """Load custom configuration from file"""
    if not Path(config_path).exists():
        print(f"Error: Configuration file '{config_path}' not found")
        sys.exit(1)

    try:
        import json
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading configuration: {e}")
        sys.exit(1)


def build_pytest_command(args: argparse.Namespace) -> List[str]:
    """Build pytest command from arguments"""
    cmd = ['python', '-m', 'pytest']

    # Test selection
    if args.test:
        cmd.extend(args.test)
    else:
        cmd.append('tests/')

    # Markers/tags
    if args.tags:
        cmd.extend(['-m', ' or '.join(args.tags)])

    # Parallel execution
    if args.parallel > 1:
        cmd.extend(['-n', str(args.parallel)])

    # Browser configuration (passed via environment)
    os.environ['BROWSER_NAME'] = args.browser
    os.environ['HEADLESS'] = 'false' if args.headed else str(args.headless).lower()
    os.environ['ENVIRONMENT'] = args.environment

    # Reporting
    if args.report in ['html', 'all']:
        cmd.extend(['--html', f'{args.report_dir}/html-report/index.html'])

    if args.report in ['junit', 'all']:
        cmd.extend(['--junitxml', f'{args.report_dir}/junit-xml/results.xml'])

    if args.report in ['allure', 'all']:
        cmd.extend(['--alluredir', f'{args.report_dir}/allure-results'])

    # Debug options
    if args.debug or args.verbose:
        cmd.append('-v')
        cmd.append('-s')

    if args.debug:
        os.environ['LOG_LEVEL'] = 'DEBUG'

    if args.quiet:
        cmd.append('-q')

    if args.dry_run:
        cmd.append('--collect-only')

    # Performance and other features
    if args.performance:
        os.environ['PERFORMANCE_MONITORING'] = 'true'

    if args.accessibility:
        os.environ['ACCESSIBILITY_CHECKING'] = 'true'

    if args.security:
        os.environ['SECURITY_SCANNING'] = 'true'

    return cmd


async def run_with_advanced_runner(args: argparse.Namespace) -> None:
    """Run tests using the advanced test runner"""
    # Load custom config if provided
    config_data = {}
    if args.config:
        config_data = load_custom_config(args.config)

    # Override config with command line arguments
    config_data.update({
        'name': f'Playwright Test Suite - {args.env}',
        'browser': args.browser,
        'headless': args.headless if not args.headed else False,
        'parallel_workers': args.parallel,
        'environment': args.env,
        'report_path': args.report_dir,
    })

    # Create test suite configuration
    suite_config = TestSuiteConfig(**config_data)

    # Create and run test runner
    runner = AdvancedTestRunner(suite_config)
    results = await runner.run_suite()

    # Output results
    if args.output:
        import json
        with open(args.output, 'w') as f:
            json.dump({
                'summary': {
                    'total': results.total_tests,
                    'passed': results.passed,
                    'failed': results.failed,
                    'skipped': results.skipped,
                    'errors': results.errors,
                    'duration': results.duration,
                },
                'results': [
                    {
                        'test_name': r.test_name,
                        'status': r.status,
                        'duration': r.duration,
                        'error_message': r.error_message,
                    } for r in results.results
                ]
            }, f, indent=2)

    # Print summary
    if not args.quiet:
        print(f"\n{'='*60}")
        print("TEST EXECUTION SUMMARY")
        print(f"{'='*60}")
        print(f"Total Tests: {results.total_tests}")
        print(f"Passed: {results.passed}")
        print(f"Failed: {results.failed}")
        print(f"Skipped: {results.skipped}")
        print(f"Errors: {results.errors}")
        print(".2f")
        print(f"Pass Rate: {(results.passed / results.total_tests * 100):.1f}%" if results.total_tests > 0 else "0%")
        print(f"{'='*60}")

    # Exit with appropriate code
    if results.failed > 0 or results.errors > 0:
        sys.exit(1)


def run_with_pytest(args: argparse.Namespace) -> None:
    """Run tests using pytest directly"""
    import subprocess

    cmd = build_pytest_command(args)

    if not args.quiet:
        print(f"Running command: {' '.join(cmd)}")
        print(f"{'='*60}")

    try:
        result = subprocess.run(cmd, cwd=Path(__file__).parent)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\nTest execution interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"Error running tests: {e}")
        sys.exit(1)


def main() -> None:
    """Main entry point"""
    args = parse_arguments()

    # Set environment variables
    os.environ['PYTHONPATH'] = str(Path(__file__).parent)

    # Create reports directory
    Path(args.report_dir).mkdir(parents=True, exist_ok=True)

    # Choose runner based on arguments
    use_advanced_runner = (
        args.config or
        args.report in ['json', 'all'] or
        args.performance or
        args.accessibility or
        args.security or
        args.output
    )

    if use_advanced_runner:
        # Use advanced runner for complex scenarios
        asyncio.run(run_with_advanced_runner(args))
    else:
        # Use pytest directly for simple scenarios
        run_with_pytest(args)


if __name__ == '__main__':
    main()