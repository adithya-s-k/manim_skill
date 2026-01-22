# ManimGL Skill Tests

This directory contains end-to-end tests to verify that all code examples in the `manimgl-best-practices` skill work correctly.

## Test Structure

- `test_utils.py` - Utility functions for extracting and running code from markdown files
- `test_all_skills.py` - Main test runner script with multiprocessing support
- `README.md` - This documentation

## Usage

### Test All Markdown Files (Parallel)

```bash
# Run all tests with default number of workers (CPU count)
uv run python tests/manimgl/test_all_skills.py

# Run with specific number of workers
uv run python tests/manimgl/test_all_skills.py -j 4

# Run single-threaded (sequential)
uv run python tests/manimgl/test_all_skills.py -j 1
```

### Test a Specific Markdown File

```bash
uv run python tests/manimgl/test_all_skills.py scenes.md
uv run python tests/manimgl/test_all_skills.py animations.md
```

## How It Works

1. **Markdown Testing**: The test utility extracts Python code blocks from markdown files, wraps them in Scene classes if needed, and runs them with ManimGL to verify they execute without errors.

2. **Multiprocessing**: Tests run in parallel using multiple CPU cores for faster execution.

3. **Smart Filtering**: The test utility automatically skips:
   - Documentation snippets (API references without complete context)
   - Bash commands and CLI examples
   - Code using undefined placeholder variables
   - Comma-separated constant lists

## Adding New Tests

Just add Python code blocks to your markdown files in the `skills/manimgl-best-practices/rules/` directory. They will be automatically tested the next time you run the test suite.

## Quick Iteration

To quickly iterate on fixing a specific file:

```bash
# Fix the markdown file
vim skills/manimgl-best-practices/rules/animations.md

# Test just that file
uv run python tests/manimgl/test_all_skills.py animations.md

# Repeat until all tests pass
```

## Test Output

- `✓ PASSED` - Code block executed successfully
- `✗ FAILED` - Code block failed with error (error details shown)
- `skipped` - Code block was skipped (documentation snippet)

## ManimGL Specifics

This test suite is specifically for ManimGL (3b1b's version), which differs from Manim Community Edition:

- Uses `from manimlib import *` instead of `from manim import *`
- Uses `manimgl` CLI command instead of `manim`
- Default scene type is `InteractiveScene`
- Different animation names (e.g., `ShowCreation` instead of `Create`)

## Prerequisites

Ensure ManimGL is installed and the `manimgl` command is available in your PATH:

```bash
# Check if manimgl is installed
manimgl --version

# Or try running with uv
uv run manimgl --version
```
