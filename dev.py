#!/usr/bin/env python3
"""Development script for running code quality tools."""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str) -> bool:
    """Run a command and return True if successful."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


def main():
    """Run all development tools."""
    print("🚀 Running Taiwan Air Quality development tools...")
    
    project_root = Path(__file__).parent
    src_path = project_root / "src"
    tests_path = project_root / "tests"
    
    commands = [
        (["uv", "run", "black", str(src_path), str(tests_path)], "Code formatting with Black"),
        (["uv", "run", "isort", str(src_path), str(tests_path)], "Import sorting with isort"),
        (["uv", "run", "flake8", str(src_path), str(tests_path)], "Linting with flake8"),
        (["uv", "run", "mypy", str(src_path)], "Type checking with mypy"),
        (["uv", "run", "pytest", str(tests_path), "-v"], "Running tests"),
    ]
    
    success_count = 0
    for cmd, description in commands:
        if run_command(cmd, description):
            success_count += 1
    
    print(f"\n📊 Results: {success_count}/{len(commands)} tools completed successfully")
    
    if success_count == len(commands):
        print("🎉 All development tools passed!")
        sys.exit(0)
    else:
        print("⚠️  Some tools failed. Please review the output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
