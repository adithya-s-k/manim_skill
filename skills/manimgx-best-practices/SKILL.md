---
name: manimgx-best-practices
description: |
  Trigger when: (1) User mentions "manimgx" or "ManimGX", (2) Code contains `import manimgx` or `from manimgx import *`, (3) User runs `manimgx` CLI commands, (4) Working with Scene, MathTex, Text, or ManimGX's render/inspect workflow.

  Best practices for ManimGX — a Rust + wgpu animation engine that speaks Manim CE's API but decides how that code behaves. Covers the `manimgx` import, Typst text and math, per-frame timing, the always-moving camera, 3D, and the `manimgx render` / `manimgx inspect` loop.

  NOT for Manim Community Edition (`from manim import *`, the `manim` CLI) and NOT for ManimGL (`from manimlib import *`).
---

## How to use

Read individual rule files for detailed explanations and code examples:

### Core Concepts
- [rules/scenes.md](rules/scenes.md) - Scene, ThreeDScene, construct, play/wait/add, sections
- [rules/animations.md](rules/animations.md) - Animation classes, `.animate`, timing and groups
- [rules/differences.md](rules/differences.md) - ManimGX vs Manim CE: imports, names, Typst, frame, time

### Text & Math
- [rules/text.md](rules/text.md) - Text, fonts, CJK, Paragraph, BulletedList
- [rules/latex.md](rules/latex.md) - MathTex, Tex, Typst, coloring parts, multi-line equations

### Layout & Appearance
- [rules/positioning.md](rules/positioning.md) - move_to, next_to, align_to, shift, edge/corner
- [rules/shapes.md](rules/shapes.md) - Circle, Square, Rectangle, Polygon, Line, Arrow, Brace
- [rules/axes.md](rules/axes.md) - Axes, NumberPlane, FunctionGraph, plotting
- [rules/updaters.md](rules/updaters.md) - ValueTracker, always_redraw, `dt` updaters

### Camera, 3D & Rendering
- [rules/camera.md](rules/camera.md) - camera.frame, zoom/pan, ThreeDScene, 3D objects
- [rules/cli.md](rules/cli.md) - `manimgx render` / `inspect` / `present` flags, `m.config`
- [rules/inspect.md](rules/inspect.md) - storyboard, layout checks, the fix-and-re-inspect loop
- [rules/errors.md](rules/errors.md) - common errors, rename hints, repair strategy

## Working Examples

Complete, tested example files demonstrating common patterns:

- [examples/basic_animations.py](examples/basic_animations.py) - Shapes, text, lagged animations, transforms
- [examples/math_visualization.py](examples/math_visualization.py) - Equations, color-coded derivations
- [examples/graph_plotting.py](examples/graph_plotting.py) - Axes, functions, areas
- [examples/three_d.py](examples/three_d.py) - ThreeDScene, 3D axes and surfaces, camera

## Scene Templates

Copy and modify these templates to start new projects:

- [templates/basic_scene.py](templates/basic_scene.py) - Standard 2D scene template
- [templates/graph_scene.py](templates/graph_scene.py) - Axes and a plotted function
- [templates/threed_scene.py](templates/threed_scene.py) - 3D scene with a moving camera

## Quick Reference

### Basic Scene Structure
```python
import manimgx as m

class MyScene(m.Scene):
    def construct(self) -> None:
        # Create mobjects
        circle = m.Circle()

        # Add to scene (static)
        self.add(circle)

        # Or animate
        self.play(m.Create(circle))

        # Wait
        self.wait(1)
```

### Render Command
```bash
# The video (MP4) and a storyboard
manimgx render scene.py MyScene

# A quick draft
manimgx render scene.py -r 1280x720 --fps 30

# Inspect first: timeline + 2D layout checks, no video
manimgx inspect scene.py
```

### Key Differences from ManimCE

| Feature | ManimGX | Manim Community |
|---------|---------|-----------------|
| Import | `import manimgx as m` / `from manimgx import *` | `from manim import *` |
| CLI | `manimgx render` / `inspect` / `present` | `manim` |
| Math text | `MathTex(r"\pi")` → Typst | `MathTex(r"\pi")` → LaTeX |
| Scene | `Scene` (camera always moves) | `Scene` / `MovingCameraScene` |
| Create anim | `Create` | `Create` |
| Camera | `self.camera.frame` | `self.camera.frame` |
| Frame width | short side 8 units (16:9 ≈ 14.2 × 8) | 16:9 ≈ 14.2 × 8, tall 4.5 × 8 |
| NumPy | import it yourself | re-exported by star import |
| LaTeX packages | not supported (Typst) | supported |

### Common Pitfalls to Avoid

1. **`from manim import *`** - That is Manim CE. Use `import manimgx as m` or `from manimgx import *`.
2. **`manim -ql` / `manim.cfg` / plugins** - ManimGX has `manimgx render -r --fps`; no config files or plugins.
3. **CJK inside `MathTex`** - Use `Text` for prose and put it next to the formula.
4. **`MovingCameraScene`** - Every `Scene`'s camera moves; use `Scene`.
5. **`\usepackage` / `\def` / `TexTemplate`** - LaTeX is translated to Typst; packages and macros do not convert.
6. **Counting frames in updaters** - Derive state from time; `dt` updaters are frame-rate independent.
