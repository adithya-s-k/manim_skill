"""Utility functions for testing markdown skill files."""
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

    if not stripped or stripped.strip() == 'from manim import *':
        return False

    # Skip bash commands and CLI examples
    if any(x in code_block for x in ['manim -', 'pip install', 'manim checkhealth', '```bash']):
        return False

    # Skip snippets that are just showing method signatures
    # These reference self.play, self.add etc without full scene context
    lines_without_comments = [l.strip() for l in code_block.split('\n')
                             if l.strip() and not l.strip().startswith('#')]

    # If it's just self.method() calls without any object creation, skip it
    # These are documentation snippets showing API, not complete examples
    has_object_creation = any(
        '=' in line or 'Circle(' in line or 'Square(' in line or
        'Text(' in line or 'class ' in line
        for line in lines_without_comments
    )

    all_self_calls = all(
        line.startswith('self.') or line.startswith('from ') or line.startswith('import ')
        for line in lines_without_comments
    )

    if all_self_calls and not has_object_creation:
        return False

    # Check if code uses undefined variables (common in API docs showing usage patterns)
    # Look for variable usage without definition in the same block
    code_lower = code_block.lower()
    undefined_vars = ['mobject1', 'mobject2', 'mobject3', 'mob1', 'mob2']

    # Also check for references to variables like 'circle', 'square' without defining them
    # (when they appear in self.play but aren't created in the block)
    common_shapes = ['circle', 'square', 'text']
    for shape in common_shapes:
        # If shape is used but not created (no Circle(), Square(), Text())
        if shape in code_lower and f'{shape.capitalize()}(' not in code_block:
            # Check if it's in a self.play or similar context
            if f'({shape}' in code_lower or f', {shape}' in code_lower:
                return False

    if any(var in code_lower for var in undefined_vars):
        return False

    return True


def create_test_scene_from_code(code_block, test_name):
    """Create a complete test scene from a code block."""
    has_imports = 'from manim import' in code_block or 'import manim' in code_block
    scene_classes = extract_scene_classes(code_block)

    if scene_classes:
        if not has_imports:
            return f"from manim import *\n\n{code_block}"
        return code_block

    # Wrap snippet in a test scene
    lines = [line for line in code_block.split('\n') if line.strip()]
    indented_code = '\n'.join('        ' + line for line in lines)

    test_code = f"""from manim import *

class {test_name}(Scene):
    def construct(self):
{indented_code}
"""
    return test_code


def run_manim_scene(scene_code, scene_name, timeout=30):
    """Run a Manim scene and check if it executes without errors."""
    with tempfile.TemporaryDirectory() as tmpdir:
        scene_file = Path(tmpdir) / "test_scene.py"
        scene_file.write_text(scene_code)

        cmd = [
            "uv", "run", "manim",
            "-ql",
            "--disable_caching",
            "--format", "png",
            "-s",
            str(scene_file),
            scene_name
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

        success, error = run_manim_scene(scene_code, scene_name)

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
