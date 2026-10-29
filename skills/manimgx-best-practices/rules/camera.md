---
name: camera
description: camera.frame, zoom, pan, ThreeDScene orientation and 3D objects in ManimGX
metadata:
  tags: camera, frame, zoom, pan, 3d, threedscene, surface, sphere, cube
---

# Camera and 3D in ManimGX

Every `Scene` has a moving camera. There is no `MovingCameraScene`; use `Scene` and animate
`self.camera.frame`.

## 2D camera: zoom and pan

```python
import manimgx as m

class Zoom(m.Scene):
    def construct(self):
        circle = m.Circle(radius=1.5, color=m.BLUE)
        self.add(circle)
        self.play(self.camera.frame.animate.scale(0.5).move_to(circle))
        self.play(self.camera.frame.animate.scale(2).move_to(m.ORIGIN))
```

- `self.camera.frame` is a mobject representing the visible rectangle.
- `.scale(k)` with `k < 1` zooms in; `k > 1` zooms out.
- `.move_to(point)` pans.

## 3D scene

```python
import manimgx as m

class In3D(m.ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65 * m.DEGREES, theta=-45 * m.DEGREES)
        axes = m.ThreeDAxes()
        sphere = m.Sphere(radius=1.5, fill_opacity=0.4)
        self.play(m.Create(axes), m.Create(sphere), run_time=2)
        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(4)
```

- `set_camera_orientation(phi=..., theta=...)` sets the view direction.
- `begin_ambient_camera_rotation(rate=...)` keeps it slowly turning.
- `move_camera(phi=..., theta=..., zoom=...)` animates a camera move.

## 3D objects

```python
m.Cube(side_length=3, fill_opacity=0.3, stroke_width=2)
m.Sphere(radius=1.5, fill_opacity=0.4)
m.Surface(lambda u, v: [u, v, u * v], u_range=[-2, 2], v_range=[-2, 2])
m.Cylinder(radius=1, height=2)
m.Cone(base_radius=1, height=2)
m.Line3D(start=m.ORIGIN, end=m.UP * 2)
```

## Fixed-in-frame text

In a `ThreeDScene`, text that should stay screen-aligned uses `add_fixed_in_frame_mobjects`:

```python
label = m.Text("Sphere", font_size=32).to_corner(m.UL)
self.add_fixed_in_frame_mobjects(label)
```
