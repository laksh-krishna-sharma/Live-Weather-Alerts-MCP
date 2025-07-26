#!/usr/bin/env python3
"""
Test runner script for the weather MCP project.
This script can be used to run all tests or specific test modules.
"""
import sys
import subprocess
from pathlib import Path


def run_tests(test_path=None, verbose=False, coverage=False, html_report=False):
    """Run tests with pytest."""
    cmd = ["python", "-m", "pytest"]
    
    if verbose:
        cmd.append("-v")
    
    if coverage:
        cmd.extend(["--cov=weather_mcp", "--cov=client"])
        if html_report:
            cmd.extend(["--cov-report=html", "--cov-report=term"])
        else:
            cmd.append("--cov-report=term")
    
    if test_path:
        cmd.append(test_path)
    else:
        cmd.append("tests/")
    
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=Path(__file__).parent.parent)
    return result.returncode


def main():
    """Main function to handle command line arguments."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run weather MCP project tests")
    parser.add_argument("--test", "-t", help="Specific test file or directory to run")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--coverage", "-c", action="store_true", help="Run with coverage")
    parser.add_argument("--html", action="store_true", help="Generate HTML coverage report")
    parser.add_argument("--list", "-l", action="store_true", help="List available test files")
    
    args = parser.parse_args()
    
    if args.list:
        print("Available test files:")
        test_dir = Path(__file__).parent
        for test_file in sorted(test_dir.glob("test_*.py")):
            print(f"  - {test_file.name}")
        return 0
    
    return run_tests(args.test, args.verbose, args.coverage, args.html)


if __name__ == "__main__":
    sys.exit(main())