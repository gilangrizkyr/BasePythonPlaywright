#!/bin/bash

# Quick start script untuk Playwright Automation Framework

echo "======================================"
echo "  Playwright Quick Start Script  "
echo "======================================"
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found. Run setup.py first"
    exit 1
fi

echo ""
echo "Available commands:"
echo "  run-tests          - Run all tests"
echo "  run-tests-verbose  - Run tests with verbose output"
echo "  run-single         - Run single test file (usage: ./quick-start.sh run-single tests/test_example.py)"
echo "  generate-report    - Generate HTML test report"
echo "  list-tests         - List all available tests"
echo ""

case "$1" in
    run-tests)
        echo "🧪 Running all tests..."
        pytest tests/
        ;;
    run-tests-verbose)
        echo "🧪 Running all tests (verbose)..."
        pytest tests/ -v
        ;;
    run-single)
        if [ -z "$2" ]; then
            echo "❌ Please specify test file path"
            exit 1
        fi
        echo "🧪 Running $2..."
        pytest "$2" -v
        ;;
    generate-report)
        echo "📊 Generating HTML report..."
        pytest tests/ --html=reports/report.html --self-contained-html
        echo "✅ Report generated: reports/report.html"
        ;;
    list-tests)
        echo "📋 Available tests:"
        pytest tests/ --collect-only -q
        ;;
    *)
        if [ -z "$1" ]; then
            echo "💡 No command specified. Try: ./quick-start.sh run-tests"
        else
            echo "❌ Unknown command: $1"
        fi
        ;;
esac
