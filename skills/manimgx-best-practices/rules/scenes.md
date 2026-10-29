---
name: scenes
description: Scene, ThreeDScene, construct, play/wait/add, and sections in ManimGX
metadata:
  tags: scene, construct, play, wait, add, setup, three_d, section
---

# Scenes in ManimGX

A `Scene` is the canvas. Every animation lives in `construct()`.

## Basic scene

```python
import manimgx as m

class MyScene(m.Scene):
    def construct(self) -> None:
        circle = m.Circle(color=m.BLUE, fill_opacity=0.5)
        self.play(m.Create(circle))
        self.wait(1)
```

## Time passes only in `play` and `wait`

```python
self.add(mob)                 # appears instantly; no time passes
self.remove(mob)              # disappears instantly
self.play(m.Create(circle))   # 1 s unless run_time=
self.play(m.FadeIn(sq), run_time=2)
self.wait()                   # 1 s
self.wait(0.5)                # 0.5 s
```

- `self.play(a, b)` runs `a` and `b` at the same time.
- `run_time` on `AnimationGroup`/`Succession` controls the whole group.
- The video's last frame is the scene's end; the scene ends when `construct()` returns.

## setup()

`setup()` runs before `construct()`. Use it for scene-wide settings:

```python
import manimgx as m

class OnWhite(m.Scene):
    def setup(self):
        m.config.background_color = m.WHITE

    def construct(self) -> None:
        self.play(m.Write(m.Text("On white", color=m.BLACK)))
```

## ThreeDScene

Use `ThreeDScene` for 3D. Aim the camera with `set_camera_orientation`; every scene's camera
can move, so there is no `MovingCameraScene`.

```python
import manimgx as m

class In3D(m.ThreeDScene):
    def construct(self) -> None:
        self.set_camera_orientation(phi=65 * m.DEGREES, theta=-45 * m.DEGREES)
        self.begin_ambient_camera_rotation(rate=0.5)
        cube = m.Cube(side_length=3, fill_opacity=0.3, stroke_width=2)
        self.play(m.Create(cube), run_time=2)
        self.wait(4)
```

## Sections (slides)

`next_section` starts a new section of one video; `manimgx present` plays the sections as
slides. Only add sections when the task asks for a presentation.

```python
class Sections(m.Scene):
    def construct(self):
        title = m.Text("Title")
        definition = m.Text("A definition")
        self.play(m.Write(title))
        self.next_section("definition", notes="Start with the definition.")
        self.play(m.Write(definition))
```

## Multiple scenes in one file

The render command takes the scene name after the file:

```bash
manimgx render scene.py Intro
```
