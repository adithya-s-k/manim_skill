---
name: creation-animations
description: Create, Write, FadeIn, DrawBorderThenFill and other creation animations
metadata:
  tags: create, write, fadein, fadeout, grow, shrink, uncreate
---

# Creation Animations

Animations that introduce mobjects to the scene.

## Create

Draws a VMobject progressively along its path.

```python
from manim import *

class CreateExample(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
```

Best for: Geometric shapes, lines, arrows.

## Write

Simulates handwriting. Best for text and equations.

```python
class WriteExample(Scene):
    def construct(self):
        text = Text("Hello World")
        equation = MathTex(r"E = mc^2")

        self.play(Write(text))
        self.wait()
        self.play(Write(equation))
```

Write automatically sets appropriate timing based on text length.

## DrawBorderThenFill

Draws the outline first, then fills in the shape.

```python
class DrawBorderExample(Scene):
    def construct(self):
        square = Square(fill_opacity=0.8, color=BLUE)
        self.play(DrawBorderThenFill(square))
```

Best for: Shapes with fills where you want to emphasize the outline first.

## FadeIn / FadeOut

Simple opacity transitions.

```python
class FadeExample(Scene):
    def construct(self):
        circle = Circle()

        # Fade in
        self.play(FadeIn(circle))
        self.wait()

        # Fade out
        self.play(FadeOut(circle))
```

### Directional Fades

```python
# Fade in from a direction
self.play(FadeIn(square, shift=UP))      # Fade in while moving up
self.play(FadeIn(square, shift=LEFT))    # Fade in from right

# Fade out to a direction
self.play(FadeOut(square, shift=DOWN))   # Fade out while moving down
```

### Scale Fades

```python
self.play(FadeIn(circle, scale=0.5))   # Fade in while growing
self.play(FadeOut(circle, scale=2))    # Fade out while shrinking
```

## GrowFromCenter / ShrinkToCenter

```python
class GrowExample(Scene):
    def construct(self):
        circle = Circle()

        self.play(GrowFromCenter(circle))
        self.wait()
        self.play(ShrinkToCenter(circle))
```

## GrowFromPoint

Grow from a specific point.

```python
self.play(GrowFromPoint(circle, ORIGIN))
self.play(GrowFromPoint(circle, LEFT * 3))
```

## GrowFromEdge

Grow from a specific edge.

```python
self.play(GrowFromEdge(square, LEFT))   # Grow from left edge
self.play(GrowFromEdge(square, DOWN))   # Grow from bottom edge
```

## SpinInFromNothing

Object spins in while growing.

```python
self.play(SpinInFromNothing(circle))
```

## Uncreate

Reverse of Create - erases the mobject.

```python
self.play(Create(circle))
self.wait()
self.play(Uncreate(circle))  # Erases in reverse
```

## AddTextLetterByLetter

Types text one character at a time.

```python
class TypingExample(Scene):
    def construct(self):
        text = Text("Hello World")
        self.play(AddTextLetterByLetter(text, time_per_char=0.1))
```

Note: Only works with `Text`, not `MathTex`.

## Best Practices

1. **Use Write for text** - Looks more natural than Create
2. **Use Create for shapes** - Clean progressive drawing
3. **Use FadeIn for quick introductions** - When drawing isn't important
4. **Match removal to creation** - If you Create, use Uncreate; if FadeIn, use FadeOut
