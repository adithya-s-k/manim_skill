# ManimGL Scenes

## Scene Types

ManimGL provides several scene types:

### InteractiveScene (Recommended)

The default for most development. Supports interactive mode with `-se` flag.

```python
from manimlib import *

class MyScene(InteractiveScene):
    def construct(self):
        circle = Circle()
        self.play(ShowCreation(circle))
        self.wait()
```

### Scene (Base Class)

Basic scene without interactive features:

```python
class BasicScene(Scene):
    def construct(self):
        self.play(Write(Text("Hello")))
```

### ThreeDScene

For 3D animations with proper camera setup:

```python
from manimlib import *

class My3DScene(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)
        self.camera.frame.reorient(-45*DEGREES, 75*DEGREES)
```

## The construct Method

All scene logic goes in `construct()`:

```python
class MyScene(InteractiveScene):
    def construct(self):
        # 1. Create mobjects
        circle = Circle(color=BLUE)
        square = Square(color=RED)

        # 2. Position them
        circle.shift(LEFT * 2)
        square.shift(RIGHT * 2)

        # 3. Animate
        self.play(ShowCreation(circle), ShowCreation(square))

        # 4. Wait for viewer
        self.wait(2)
```

## Adding vs Playing

```python
# Static add (instant, no animation)
self.add(circle)

# Animated add
self.play(ShowCreation(circle))
self.play(FadeIn(square))
```

## Scene Methods

| Method | Description |
|--------|-------------|
| `self.play(*anims)` | Play animations |
| `self.wait(t)` | Wait t seconds |
| `self.add(*mobs)` | Add mobjects instantly |
| `self.remove(*mobs)` | Remove mobjects |
| `self.clear()` | Clear all mobjects |
| `self.embed()` | Drop into IPython shell |

## Interactive Mode

Run with `-se` flag to enter at a specific line:

```bash
manimgl scene.py MyScene -se 15
```

In the shell:
```python
checkpoint_paste()           # Run clipboard code with animations
checkpoint_paste(skip=True)  # Run instantly
checkpoint_paste(record=True) # Record while running
```

## Class Attributes

Define scene configuration as class attributes:

```python
class MyScene(InteractiveScene):
    camera_class = ThreeDCamera  # Use 3D camera
    random_seed = 42             # For reproducibility

    def construct(self):
        ...
```
