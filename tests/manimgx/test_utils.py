"""Utility functions for testing ManimGX markdown skill files."""
import os
import re
import shutil
import tempfile
import subprocess
from pathlib import Path


def extract_python_code_blocks(markdown_content):
    """Extract Python code blocks from markdown content."""
    pattern = r'```python\n(.*?)```'
    matches = re.findall(pattern, markdown_content, re.DOTALL)
    return matches


def extract_scene_classes(code):
    """Extract Scene class names from Python code."""
    pattern = r'class\s+(\w+)\s*\((.*?Scene.*?)\):'
    matches = re.findall(pattern, code)
    return [match[0] for match in matches]


def is_executable_code(code_block):
    """Check if a code block is executable Python code."""
    stripped = '\n'.join(line for line in code_block.split('\n')
                        if line.strip() and not line.strip().startswith('#'))

    if not stripped or stripped.strip() in ('from manimgx import *', 'import manimgx as m'):
        return False

    # Skip bash commands, CLI examples, and config file content
    if any(x in code_block for x in ['manimgx render', 'manimgx inspect', 'manimgx present',
                                     'pip install', 'uv tool install', '```bash']):
        return False

    # Skip config access/modification snippets (these are meant as documentation)
    if 'config.' in code_block and 'class' not in code_block and not any('=' in line and '(' in line for line in code_block.split('\n')):
        return False

    lines_without_comments = [l.strip() for l in code_block.split('\n')
                             if l.strip() and not l.strip().startswith('#')]

    if not lines_without_comments:
        return False

    # Check if code has a complete Scene class definition
    has_scene_class = any('class ' in line and 'Scene' in line for line in lines_without_comments)

    has_object_creation = any('=' in line for line in lines_without_comments)

    all_self_calls = all(
        line.startswith('self.') or line.startswith('from ') or line.startswith('import ')
        for line in lines_without_comments
    )

    # Skip documentation snippets (method calls without complete context)
    if all_self_calls and not has_object_creation and not has_scene_class:
        return False

    code_lower = code_block.lower()

    doc_placeholders = [
        'mobject', 'mobject1', 'mobject2', 'mobject3',
        'mob', 'mob1', 'mob2',
        'target', 'leader', 'follower', 'updater_function',
        'mobjects', 'objects', 'circles', 'squares', 'dots',
        'group1', 'group2', 'group_copy', 'new_start', 'new_end',
        'start_point', 'end_point', 'other', 'shape',
        'text', 'equation',
    ]

    for placeholder in doc_placeholders:
        if placeholder in code_lower:
            is_defined = (
                f'{placeholder} = ' in code_lower or
                f'{placeholder}=' in code_lower or
                f'def ' in code_lower and f'{placeholder})' in code_lower or
                'for ' in code_lower and f'{placeholder} in' in code_lower
            )
            if not is_defined and not has_scene_class:
                return False

    shape_patterns = {
        'circle': 'Circle(', 'square': 'Square(', 'text': 'Text(',
        'line': 'Line(', 'dot': 'Dot(', 'arrow': 'Arrow(',
        'axes': 'Axes(', 'graph': 'FunctionGraph(', 'rect': 'Rectangle(',
        'arc': 'Arc(',
    }

    for var_name, constructor in shape_patterns.items():
        if var_name in code_lower and constructor not in code_block:
            if (f'({var_name}' in code_lower or
                f', {var_name}' in code_lower or
                f'{var_name}.' in code_lower):
                if not has_scene_class:
                    return False

    if not has_object_creation and not has_scene_class:
        bare_calls = all(
            '(' in line and ')' in line and '=' not in line and not line.startswith('def ')
            for line in lines_without_comments
            if not line.startswith('from ') and not line.startswith('import ')
        )
        if bare_calls:
            return False

    def is_constant_list_line(line):
        cleaned = re.sub(r'\([^)]*\)', '', line)
        parts = [p.strip() for p in cleaned.split(',') if p.strip()]
        if not parts:
            return False
        return all(
            part.replace('_', '').isalpha() and part.isupper()
            for part in parts
        )

    all_constant_lists = all(
        is_constant_list_line(line)
        for line in lines_without_comments
        if line and not line.startswith('from ') and not line.startswith('import ')
    )
    if all_constant_lists and not has_scene_class and not has_object_creation:
        return False

    def is_bare_identifier(line):
        code_part = line.split('#')[0].strip()
        if not code_part:
            return False
        return code_part.replace('_', '').isalnum() and code_part.isidentifier() and '(' not in code_part and '=' not in code_part

    all_bare_identifiers = all(
        is_bare_identifier(line)
        for line in code_block.split('\n')
        if line.strip() and not line.strip().startswith('#') and not line.strip().startswith('from ') and not line.strip().startswith('import ')
    )
    if all_bare_identifiers and not has_scene_class and not has_object_creation:
        relevant_lines = [l for l in code_block.split('\n') if l.strip() and not l.strip().startswith('#') and not l.strip().startswith('from ') and not l.strip().startswith('import ')]
        if len(relevant_lines) > 1:
            return False

    return True


def _missing_imports(code_block):
    """The imports a snippet needs, whichever style it uses (`m.` or bare names)."""
    lines = []
    if 'import manimgx as m' not in code_block:
        lines.append('import manimgx as m')
    if 'from manimgx import *' not in code_block:
        lines.append('from manimgx import *')
    return '\n'.join(lines)


def create_test_scene_from_code(code_block, test_name):
    """Create a complete test scene from a code block."""
    scene_classes = extract_scene_classes(code_block)
    imports = _missing_imports(code_block)

    if scene_classes:
        if not imports:
            return code_block
        return f"{imports}\n\n{code_block}"

    lines = [line for line in code_block.split('\n') if line.strip()]
    indented_code = '\n'.join('        ' + line for line in lines)

    return f"""{imports}

class {test_name}(Scene):
    def construct(self):
{indented_code}
"""


def run_manimgx_scene(scene_code, scene_name, timeout=120):
    """Run a ManimGX scene and check if it executes without errors."""
    with tempfile.TemporaryDirectory() as tmpdir:
        scene_file = Path(tmpdir) / "test_scene.py"
        scene_file.write_text(scene_code)
        output = Path(tmpdir) / "test.mp4"

        cmd = [
            "uv", "run", "--python", "3.13", "--with", "manimgx",
            "manimgx", "render",
            str(scene_file), scene_name,
            "-r", "320x180", "--fps", "15",
            "-o", str(output),
        ]
        # A local `manimgx` (uv tool install) is faster than resolving the
        # ephemeral environment for every block.
        local = os.environ.get("MANIMGX_BIN") or shutil.which("manimgx")
        if local:
            cmd = [
                local, "render",
                str(scene_file), scene_name,
                "-r", "320x180", "--fps", "15",
                "-o", str(output),
            ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=tmpdir,
            )

            if result.returncode == 0:
                return True, ""
            error_msg = f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
            return False, error_msg

        except subprocess.TimeoutExpired:
            return False, f"Scene rendering timed out after {timeout} seconds"
        except Exception as e:
            return False, f"Error running scene: {str(e)}"


def test_markdown_file(markdown_path):
    """Test all Python code blocks in a markdown file."""
    print(f"\n{'='*60}")
    print(f"Testing: {markdown_path.name}")
    print(f"{'='*60}")

    content = markdown_path.read_text()
    code_blocks = extract_python_code_blocks(content)

    total = 0
    passed = 0
    failed = 0
    skipped = 0

    for idx, code_block in enumerate(code_blocks):
        if not is_executable_code(code_block):
            skipped += 1
            continue

        total += 1
        test_name = f"Test{markdown_path.stem.title().replace('-', '')}_{idx}"
        scene_code = create_test_scene_from_code(code_block, test_name)

        scene_classes = extract_scene_classes(scene_code)
        scene_name = scene_classes[0] if scene_classes else test_name

        print(f"\n  Block {idx}: Testing {scene_name}...", end=" ")

        success, error = run_manimgx_scene(scene_code, scene_name)

        if success:
            print("✓ PASSED")
            passed += 1
        else:
            print("✗ FAILED")
            print(f"    Code:\n{code_block[:200]}...")
            print(f"    Error: {error[:500]}")
            failed += 1

    print(f"\n  Summary: {passed}/{total} passed, {failed} failed, {skipped} skipped")
    return passed, failed, skipped
