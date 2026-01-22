"""Utility functions for testing ManimGL markdown skill files."""
import re
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

    if not stripped or stripped.strip() == 'from manimlib import *':
        return False

    # Skip bash commands, CLI examples, and config file content
    if any(x in code_block for x in ['manimgl ', 'pip install', '```bash', '[CLI]', '[output]', '[renderer]']):
        return False

    # Skip config access/modification snippets (these are meant as documentation)
    if 'config.' in code_block and 'class' not in code_block and not any('=' in line and '(' in line for line in code_block.split('\n')):
        return False

    # Skip snippets that are just showing method signatures
    lines_without_comments = [l.strip() for l in code_block.split('\n')
                             if l.strip() and not l.strip().startswith('#')]

    # Skip if no executable lines
    if not lines_without_comments:
        return False

    # Check if code has a complete Scene class definition
    has_scene_class = any('class ' in line and 'Scene' in line for line in lines_without_comments)

    # If it's just self.method() calls without any object creation, skip it
    has_object_creation = any(
        '=' in line for line in lines_without_comments
    )

    all_self_calls = all(
        line.startswith('self.') or line.startswith('from ') or line.startswith('import ')
        for line in lines_without_comments
    )

    # Skip documentation snippets (method calls without complete context)
    if all_self_calls and not has_object_creation and not has_scene_class:
        return False

    # Check for common undefined variable patterns in documentation
    code_lower = code_block.lower()

    # List of placeholder variable names commonly used in API documentation
    doc_placeholders = [
        'mobject', 'mobject1', 'mobject2', 'mobject3',
        'mob', 'mob1', 'mob2',
        'target', 'leader', 'follower',
        'updater_function',
        'mobjects',  # plural
        'objects',
        'circles',  # plural without definition
        'squares',
        'dots',
        'group1', 'group2',  # group placeholders
        'group_copy',
        'new_start', 'new_end',  # line placeholders
        'start_point', 'end_point',
        'other',  # generic placeholder for next_to, etc.
        'shape',  # generic shape placeholder
        'text',  # text/MathTex placeholder
        'equation',
        'frame',  # camera frame placeholder
        'light',  # light source placeholder
        'formula',  # formula placeholder
    ]

    # Skip checkpoint functions and interactive features (ManimGL specific)
    if 'checkpoint_paste' in code_lower or 'save_state' in code_lower or 'undo' in code_lower or '.embed()' in code_lower:
        if not has_scene_class:
            return False

    # Skip any code with .embed() as it opens interactive shell
    if '.embed()' in code_block:
        return False

    # Check if these placeholders are used but not defined
    for placeholder in doc_placeholders:
        # If placeholder is referenced but not created with = or as parameter
        if placeholder in code_lower:
            # Check if it's defined in the code
            is_defined = (
                f'{placeholder} = ' in code_lower or
                f'{placeholder}=' in code_lower or
                f'def ' in code_lower and f'{placeholder})' in code_lower or  # function parameter
                'for ' in code_lower and f'{placeholder} in' in code_lower  # loop variable
            )
            if not is_defined and not has_scene_class:
                return False

    # Check for shape variables used without creation
    shape_patterns = {
        'circle': 'Circle(',
        'square': 'Square(',
        'text': 'Text(',
        'line': 'Line(',
        'dot': 'Dot(',
        'arrow': 'Arrow(',
        'axes': 'Axes(',
        'graph': 'FunctionGraph(',
        'rect': 'Rectangle(',
        'arc': 'Arc(',
    }

    for var_name, constructor in shape_patterns.items():
        if var_name in code_lower and constructor not in code_block:
            # Check if it's used in a way that suggests it should exist
            if (f'({var_name}' in code_lower or
                f', {var_name}' in code_lower or
                f'{var_name}.' in code_lower):
                # Unless it's part of a complete scene
                if not has_scene_class:
                    return False

    # Skip pure API reference snippets (just function/class calls with no assignment)
    if not has_object_creation and not has_scene_class:
        # Check if all lines are just bare function calls
        bare_calls = all(
            '(' in line and ')' in line and '=' not in line and not line.startswith('def ')
            for line in lines_without_comments
            if not line.startswith('from ') and not line.startswith('import ')
        )
        if bare_calls:
            return False

    # Skip lines that are just comma-separated constant names (like color lists)
    def is_constant_list_line(line):
        # Remove comments in parentheses like "(or GRAY)"
        cleaned = re.sub(r'\([^)]*\)', '', line)
        parts = [p.strip() for p in cleaned.split(',') if p.strip()]
        if not parts:
            return False
        # Check if all parts are uppercase constant names
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

    # Skip bare identifier lists (API reference names like rate functions)
    def is_bare_identifier(line):
        # Remove inline comments first
        code_part = line.split('#')[0].strip()
        if not code_part:
            return False
        # Check if remaining part is just a single identifier (letters, numbers, underscores)
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


def create_test_scene_from_code(code_block, test_name):
    """Create a complete test scene from a code block."""
    has_imports = 'from manimlib import' in code_block or 'import manimlib' in code_block
    scene_classes = extract_scene_classes(code_block)

    if scene_classes:
        if not has_imports:
            return f"from manimlib import *\n\n{code_block}"
        return code_block

    # Wrap snippet in a test scene (use InteractiveScene as default for ManimGL)
    lines = [line for line in code_block.split('\n') if line.strip()]
    indented_code = '\n'.join('        ' + line for line in lines)

    test_code = f"""from manimlib import *

class {test_name}(InteractiveScene):
    def construct(self):
{indented_code}
"""
    return test_code


def run_manimgl_scene(scene_code, scene_name, timeout=30):
    """Run a ManimGL scene and check if it executes without errors."""
    with tempfile.TemporaryDirectory() as tmpdir:
        scene_file = Path(tmpdir) / "test_scene.py"
        scene_file.write_text(scene_code)

        cmd = [
            "manimgl",
            str(scene_file),
            scene_name,
            "--write_file",
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=tmpdir
            )

            if result.returncode == 0:
                return True, ""
            else:
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

        success, error = run_manimgl_scene(scene_code, scene_name)

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
