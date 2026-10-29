---
name: differences
description: ManimGX vs Manim CE — imports, names, Typst, frame, time
metadata:
  tags: manimgx, differences, migration, manim-ce, imports, typst, frame
---

# ManimGX vs Manim CE

ManimGX keeps Manim CE's API (scenes, mobjects, animations, constants) so most CE code
runs after you replace `manim` with `manimgx`. But ManimGX decides how that code behaves.
This file lists what actually differs — treat it as authoritative over any Manim CE tutorial.

## Imports

- Every name is on the package: `import manimgx as m`, then `m.Circle`, or `from manimgx import *`.
- Manim CE's submodules do **not** exist: write `from manimgx import polylabel`, not `from manimgx.utils.polylabel import polylabel`.
- NumPy is not something you should rely on from the star import: `import numpy as np` yourself when you need it.
- Render with `manimgx render scene.py MyScene`. Manim CE's quality flags (`-ql`, `-qh`, …) are gone; use `-r`/`--resolution` and `--fps`.

## Typst instead of LaTeX

- You do **not** install LaTeX. `Tex` and `MathTex` translate LaTeX to Typst, which the engine typesets.
- LaTeX packages, `\def`, custom macros, and `TexTemplate`/`\usepackage` do **not** convert.
- `m.MathTex("x={{y}}")` makes a part wherever the double braces are (two parts here). Manim CE only made one at the start of a string or after a space. This changes `set_color_by_tex` / `TransformMatchingTex` behavior.
- Text is set with the fonts ManimGX ships (including Noto CJK), so documents look the same everywhere; you do not pick a system font just to get Chinese glyphs.

## The frame

- The frame's **short side is 8 units**, centred on the origin. A 16:9 video is ≈14.2 wide × 8 high; a 9:16 (tall) video is 8 wide × ≈14.2 high. Manim CE's tall frame was 4.5 wide — ManimGX's is not. A scene designed for 16:9 also fits 9:16 if its content stays inside the central 8×8 square.

## Time and animations

- Each frame shows the scene at its own exact time, at every frame rate. The video's last frame is the scene's end.
- Updaters receive the exact time since their last call and keep running while an animation plays their mobject. `dt` updaters run on their own clock, so a simulation is identical at every frame rate.
- `.animate` applies its calls when its animation starts; in a `Succession`, each `.animate` starts where the previous one ended.
- A rotation turns the mobject as one rigid piece, about one point.
- Animations of one mobject that start at the same time combine: their movements add.

## One name for each thing

ManimGX keeps one canonical name; the CE alternative usually still works but is deprecated:

| Prefer (ManimGX) | Avoid (CE alias) |
| --- | --- |
| `Scene` (camera always moves) | `MovingCameraScene` |
| `mob.animate.scale(2)` / `.set_color(RED)` | `ApplyMethod`, `ScaleInPlace`, `FadeToColor` |
| `VGroup` / `Group` (same class) | treating them as different |
| `.arrange(DOWN)` | `arrange_submobjects` |
| `.rotate(angle, about_point=ORIGIN)` | `rotate_about_origin` |
| `.get_top()` / property `width`, `height`, `color` | `get_edge_center(UP)`, `get_width()` |
| `mob.width = 2` / `mob.set(width=2)` | `set_width(2)` (not available) |
| `add_foreground_mobjects` | `add_foreground_mobject` |

Size is a property, and so is every other getter: read `mob.width`, write `mob.width = 2`
or `mob.set(width=2)`. There is no `set_width`/`set_height` on a mobject; use
`stretch_to_fit_width`/`scale_to_fit_width` when you mean to distort or fit.

## Types

Every keyword argument and every `.animate` chain is typed. A type checker (`ty`) finds a
misspelled keyword or a nonexistent name *before* you render. At runtime most mobjects and
animations silently ignore a keyword they don't take, so only the type checker tells you
about a typo. To animate a method of your own class through `.animate`, pass a function:
`box.animate(lambda b: b.grow(2))`.
