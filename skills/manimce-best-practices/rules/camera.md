---
name: camera
description: MovingCameraScene, zoom, pan, and camera manipulation
metadata:
  tags: camera, zoom, pan, frame, movingcamerascene, 3d
---

# Camera Control

Control what the viewer sees with camera manipulation.

## MovingCameraScene

For 2D scenes with camera movement (zoom, pan).

```python
from manim import *

class CameraExample(MovingCameraScene):
    def construct(self):
        circle = Circle()
        square = Square().shift(RIGHT * 3)
        self.add(circle, square)

        # Access camera frame
        # self.camera.frame is the viewable area
```

## Zooming

### Zoom In/Out by Scaling Frame

```python
class ZoomExample(MovingCameraScene):
    def construct(self):
        dots = VGroup(*[Dot() for _ in range(100)])
        dots.arrange_in_grid(10, 10, buff=0.3)
        self.add(dots)

        # Zoom in (make frame smaller)
        self.play(self.camera.frame.animate.scale(0.5))
        self.wait()

        # Zoom out (make frame larger)
        self.play(self.camera.frame.animate.scale(4))
```

### Zoom to Specific Width

```python
class ZoomToWidth(MovingCameraScene):
    def construct(self):
        text = Text("Focus on me!")
        self.add(text)

        # Zoom to fit text with padding
        self.play(
            self.camera.frame.animate.set(width=text.width * 1.5)
        )
```

## Panning

### Move Camera to Location

```python
class PanExample(MovingCameraScene):
    def construct(self):
        c1 = Circle().shift(LEFT * 3)
        c2 = Circle().shift(RIGHT * 3)
        self.add(c1, c2)

        # Pan to first circle
        self.play(self.camera.frame.animate.move_to(c1))
        self.wait()

        # Pan to second circle
        self.play(self.camera.frame.animate.move_to(c2))
```

### Combined Zoom and Pan

```python
class ZoomAndPan(MovingCameraScene):
    def construct(self):
        square = Square().shift(LEFT * 2)
        triangle = Triangle().shift(RIGHT * 2)
        self.add(square, triangle)

        # Zoom in and pan simultaneously
        self.play(
            self.camera.frame.animate.scale(0.5).move_to(square)
        )
        self.wait()

        # Move to triangle (still zoomed)
        self.play(self.camera.frame.animate.move_to(triangle))
```

## Save and Restore Camera State

```python
class SaveRestoreCamera(MovingCameraScene):
    def construct(self):
        circle = Circle()
        self.add(circle)

        # Save current state
        self.camera.frame.save_state()

        # Make changes
        self.play(self.camera.frame.animate.scale(0.3).move_to(circle))
        self.wait()

        # Restore to saved state
        self.play(Restore(self.camera.frame))
```

## auto_zoom

Automatically zoom to fit mobjects.

```python
class AutoZoomExample(MovingCameraScene):
    def construct(self):
        squares = VGroup(*[
            Square().shift(RIGHT * i + UP * j)
            for i in range(-2, 3) for j in range(-2, 3)
        ])
        self.add(squares)

        # Zoom to fit specific mobject
        self.play(self.camera.auto_zoom(squares[0]))
        self.wait()

        # Zoom to fit all with margin
        self.play(self.camera.auto_zoom(squares, margin=1))
```

## 3D Camera (ThreeDScene)

```python
class ThreeDCameraExample(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        sphere = Sphere()
        self.add(axes, sphere)

        # Set initial camera orientation
        self.set_camera_orientation(
            phi=75 * DEGREES,    # Angle from z-axis
            theta=-45 * DEGREES  # Angle around z-axis
        )
```

### Animated Camera Rotation

```python
class RotatingCamera(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)

        self.set_camera_orientation(phi=75 * DEGREES, theta=0)

        # Continuous rotation
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)
        self.stop_ambient_camera_rotation()
```

### Move 3D Camera

```python
class Move3DCamera(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)

        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # Animate camera movement
        self.move_camera(
            phi=45 * DEGREES,
            theta=45 * DEGREES,
            run_time=3
        )
```

## Camera Background

```python
class CameraBackground(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = BLUE_E

        circle = Circle()
        self.add(circle)
```

## Best Practices

1. **Use MovingCameraScene for zoom/pan** - Regular Scene camera is static
2. **Save state before complex movements** - Easy to restore
3. **Use auto_zoom for dynamic content** - Automatically fits content
4. **Keep camera movements smooth** - Don't make viewers dizzy
5. **Use 3D camera rotation sparingly** - Can be disorienting
