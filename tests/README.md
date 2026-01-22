# Tests

This directory contains test suites for verifying Manim skills.

## Structure

```
tests/
├── manimce/          # Tests for Manim Community Edition (ManimCE) skills
│   ├── test_all_skills.py  # Main test runner with multiprocessing
│   ├── test_utils.py        # Test utilities
│   └── README.md            # ManimCE testing documentation
├── manimgl/          # Tests for ManimGL (3b1b version) skills
│   ├── test_all_skills.py  # Main test runner with multiprocessing
│   ├── test_utils.py        # Test utilities
│   └── README.md            # ManimGL testing documentation
└── README.md         # This file
```

## Test Suites

### Manim CE Tests

Tests for the `manimce-best-practices` skill to ensure all code examples work correctly.

**Quick Start:**
```bash
# Run all ManimCE tests in parallel
uv run python tests/manimce/test_all_skills.py

# Test specific file
uv run python tests/manimce/test_all_skills.py scenes.md

# Control parallelism
uv run python tests/manimce/test_all_skills.py -j 4
```

See [manimce/README.md](manimce/README.md) for detailed documentation.

### ManimGL Tests

Tests for the `manimgl-best-practices` skill to ensure all code examples work correctly.

**Quick Start:**
```bash
# Run all ManimGL tests in parallel
uv run python tests/manimgl/test_all_skills.py

# Test specific file
uv run python tests/manimgl/test_all_skills.py scenes.md

# Control parallelism
uv run python tests/manimgl/test_all_skills.py -j 4
```

See [manimgl/README.md](manimgl/README.md) for detailed documentation.

## Adding New Test Suites

When adding tests for other frameworks or skills:

1. Create a new subdirectory (e.g., `tests/manim_gl/`, `tests/other_framework/`)
2. Add test utilities and runner scripts specific to that framework
3. Update this README with the new test suite information
