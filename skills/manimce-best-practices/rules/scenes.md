---
name: scenes
description: Scene structure, construct method, and scene types in Manim
metadata:
  tags: scene, construct, setup, render, ThreeDScene, MovingCameraScene
---

# Scenes in Manim

A Scene is the canvas where all animations take place. Every Manim animation is defined within a Scene class.

## Basic Scene Structure

All animation code resides within the `construct()` method of a Scene subclass.

```python
from manim import *

class MyScene(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
        self.wait(1)
```

## Scene Lifecycle Methods

### construct()
The main method where you define your animation. Called automatically when rendering.

### setup()
Called before `construct()`. Use for initialization that should happen before animation logic.

```python
class MyScene(Scene):
    def setup(self):
        self.camera.background_color = BLUE_E

    def construct(self):
        circle = Circle()
        self.play(Create(circle))
```

## Scene Methods

### Adding and Removing Objects

```python
# Add without animation (instant)
self.add(mobject)
self.add(mobject1, mobject2, mobject3)

# Remove without animation
self.remove(mobject)

# Clear all mobjects
self.clear()
```

### Playing Animations

```python
# Play a single animation
self.play(Create(circle))

# Play multiple animations simultaneously
self.play(Create(circle), FadeIn(square))

# With run_time
self.play(Create(circle), run_time=2)
```

### Waiting

```python
# Wait for 1 second (default)
self.wait()

# Wait for specific duration
self.wait(2)
```

## Scene Types

### Scene (Default)
Standard 2D scene for most animations.

### ThreeDScene
For 3D animations with camera orientation control.

```python
class My3DScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        axes = ThreeDAxes()
        sphere = Sphere()
        self.add(axes, sphere)
```

### MovingCameraScene
For animations that require camera movement (zoom, pan).

```python
class ZoomScene(MovingCameraScene):
    def construct(self):
        circle = Circle()
        self.add(circle)
        self.play(self.camera.frame.animate.scale(0.5).move_to(circle))
```

## Multiple Scenes in One File

Render specific scene:
```bash
manim -pql file.py Scene1
```

Render all scenes:
```bash
manim -pql -a file.py
```
