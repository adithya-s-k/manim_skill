# ManimGX Skill Tests

End-to-end tests that verify every Python code block in the `manimgx-best-practices` skill
actually runs on ManimGX.

## Test Structure

- `test_utils.py` - extracts code blocks, skips documentation snippets, wraps runnable ones in
  a `Scene`, and renders them with `manimgx`
- `test_all_skills.py` - parallel test runner
- `README.md` - this documentation

## Prerequisites

ManimGX needs Python 3.13+ and installs as a CLI:

```bash
uv tool install --python 3.13 manimgx
manimgx --version
```

The runner uses a `manimgx` on `PATH` when it finds one. Otherwise it falls back to
`uv run --python 3.13 --with manimgx manimgx ...`, which resolves an ephemeral environment
per block (slower, but needs no setup). Set `MANIMGX_BIN=/path/to/manimgx` to force a binary.

## Usage

```bash
# Run all rule files in parallel
python3 tests/manimgx/test_all_skills.py

# One file
python3 tests/manimgx/test_all_skills.py scenes.md

# Control parallelism
python3 tests/manimgx/test_all_skills.py -j 4
```

## How It Works

1. **Extract**: every ` ```python ` block in `skills/manimgx-best-practices/rules/*.md`.
2. **Filter**: documentation snippets (bare method calls, undefined placeholders, CLI blocks)
   are skipped.
3. **Wrap**: a snippet becomes the body of a generated `Scene` with
   `import manimgx as m` and `from manimgx import *`; a block that already defines a scene is
   used as-is.
4. **Render**: `manimgx render scene.py SceneName -r 320x180 --fps 15`, enough to execute the
   code without paying for a full-quality video.

## Adding New Tests

Add a Python code block to a rule file. If it uses names it does not define, either define
them or keep it a clearly non-executable snippet — the filter skips the latter.

## Output

- `✓ PASSED` - the scene executed
- `✗ FAILED` - the scene raised; the failing block and the ManimGX traceback are printed
- `skipped` - documentation snippet, not executed
