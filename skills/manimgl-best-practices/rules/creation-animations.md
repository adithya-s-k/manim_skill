# Creation Animations in ManimGL

Creation animations bring mobjects into existence. ManimGL provides several animation classes for different creation effects.

## ShowCreation

**Note**: ManimGL uses `ShowCreation`, not `Create` (which is used in ManimCE).

### Basic Usage

```python
from manimlib import *

class CreationExample(Scene):
    def construct(self):
        circle = Circle()

        # ShowCreation draws the object
        self.play(ShowCreation(circle))
        self.wait()
```

### Different Mobjects

```python
# Works with any VMobject
self.play(ShowCreation(Circle()))
self.play(ShowCreation(Square()))
self.play(ShowCreation(Line(LEFT, RIGHT)))
self.play(ShowCreation(Text("Hello")))
```

### Reverse Creation

```python
# Uncreate (reverse of ShowCreation)
circle = Circle()
self.add(circle)
self.play(ShowCreation(circle, reverse=True))  # Uncreates
```

## Write

The `Write` animation is specifically for text and LaTeX.

### Writing Text

```python
# Write text letter by letter
text = Text("Hello World", font_size=60)
self.play(Write(text))

# Write LaTeX
formula = Tex(R"\int_0^1 x^2 dx = \frac{1}{3}")
self.play(Write(formula))
```

### Write Speed

```python
# Control writing speed with run_time
text = Text("Fast", font_size=72)
self.play(Write(text), run_time=0.5)

text2 = Text("Slow", font_size=72)
self.play(Write(text2), run_time=3)
```

## FadeIn

Fade objects into view.

### Basic FadeIn

```python
circle = Circle()
self.play(FadeIn(circle))
```

### FadeIn with Shift

```python
# Fade in while shifting
text = Text("Appearing", font_size=60)
self.play(FadeIn(text, shift=UP))

# From different directions
self.play(FadeIn(circle, shift=DOWN))
self.play(FadeIn(square, shift=LEFT))
self.play(FadeIn(triangle, shift=RIGHT))
```

### FadeIn with Scale

```python
# Fade in while scaling
circle = Circle()
self.play(FadeIn(circle, scale=0.5))  # Starts at half size

# Shrink while fading in
square = Square()
self.play(FadeIn(square, scale=2))  # Starts at double size
```

## DrawBorderThenFill

Draws the border first, then fills the shape.

```python
class DrawBorderExample(Scene):
    def construct(self):
        square = Square()
        square.set_fill(BLUE, opacity=0.7)
        square.set_stroke(WHITE, width=4)

        self.play(DrawBorderThenFill(square))
        self.wait()
```

## GrowFromCenter

Grows object from its center.

```python
circle = Circle()
self.play(GrowFromCenter(circle))

# Control growth speed
square = Square()
self.play(GrowFromCenter(square), run_time=2)
```

## GrowFromEdge

Grows object from a specific edge.

```python
square = Square()

# Grow from different edges
self.play(GrowFromEdge(square, DOWN))
# or: UP, DOWN, LEFT, RIGHT
```

## GrowFromPoint

Grows object from a specific point.

```python
circle = Circle()
point = np.array([2, 2, 0])

self.play(GrowFromPoint(circle, point))
```

## SpinInFromNothing

Spins object into view while growing.

```python
star = Star()
self.play(SpinInFromNothing(star))
```

## AnimationGroup for Multiple Creations

### Simultaneous Creation

```python
class MultipleCreations(Scene):
    def construct(self):
        shapes = VGroup(
            Circle().shift(LEFT * 2),
            Square(),
            Triangle().shift(RIGHT * 2)
        )

        # Create all simultaneously
        self.play(*[ShowCreation(shape) for shape in shapes])
        self.wait()
```

### Sequential Creation

```python
# One after another
for shape in shapes:
    self.play(ShowCreation(shape))
    self.wait(0.2)
```

## LaggedStart

Creates objects with a staggered delay.

```python
class LaggedCreation(Scene):
    def construct(self):
        circles = VGroup(*[
            Circle(radius=0.5).shift(i * RIGHT)
            for i in range(-3, 4)
        ])

        # Staggered creation
        self.play(LaggedStart(
            *[ShowCreation(circle) for circle in circles],
            lag_ratio=0.2  # Delay between each
        ))
        self.wait()
```

## Comparison: Creation Animations

```python
class CreationComparison(Scene):
    def construct(self):
        methods = [
            ("ShowCreation", ShowCreation),
            ("FadeIn", FadeIn),
            ("GrowFromCenter", GrowFromCenter),
            ("DrawBorderThenFill", DrawBorderThenFill),
        ]

        for name, AnimClass in methods:
            # Create label
            label = Text(name, font_size=30)
            label.to_edge(UP)

            # Create shape
            square = Square()
            square.set_fill(BLUE, opacity=0.7)
            square.set_stroke(WHITE, width=3)

            # Show animation
            self.play(Write(label))
            self.play(AnimClass(square))
            self.wait()
            self.play(FadeOut(VGroup(label, square)))
```

## Advanced Creation Patterns

### Partial Creation

```python
# Show only part of the creation
line = Line(LEFT * 3, RIGHT * 3)
self.play(
    ShowCreation(line),
    rate_func=lambda t: smooth(t * 0.5)  # Only 50% created
)
```

### Reversed Rate Function

```python
# Create backwards
circle = Circle()
self.play(
    ShowCreation(circle),
    rate_func=lambda t: 1 - smooth(t)  # Reverse
)
```

### Creation with Color Change

```python
class ColoredCreation(Scene):
    def construct(self):
        line = Line(LEFT * 3, RIGHT * 3)
        line.set_color_by_gradient(BLUE, RED)

        self.play(ShowCreation(line), run_time=2)
        self.wait()
```

## Writing Mathematical Content

### Writing Equations

```python
class WriteEquation(Scene):
    def construct(self):
        equation = Tex(R"E = mc^2")
        equation.scale(2)

        self.play(Write(equation))
        self.wait()

        # Color parts
        equation.set_color_by_tex("E", BLUE)
        equation.set_color_by_tex("m", GREEN)
        equation.set_color_by_tex("c", YELLOW)
        self.wait()
```

### Writing Multi-line Content

```python
class MultiLineWrite(Scene):
    def construct(self):
        lines = VGroup(
            Tex(R"a^2 + b^2 = c^2"),
            Tex(R"e^{i\pi} + 1 = 0"),
            Tex(R"\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}")
        )
        lines.arrange(DOWN, buff=0.5)

        # Write line by line
        for line in lines:
            self.play(Write(line))
            self.wait(0.5)
```

## Best Practices

1. **ShowCreation for shapes**: Use for geometric objects and paths
2. **Write for text**: Use for Text and Tex objects
3. **FadeIn for groups**: Good for bringing in multiple objects
4. **LaggedStart for sequences**: Creates visual rhythm
5. **Consistent timing**: Keep run_time similar for related objects
6. **Match animation to content**: Use appropriate animation for the context

## Common Patterns

### Create and highlight

```python
shape = Circle()
self.play(ShowCreation(shape))
self.play(shape.animate.set_color(YELLOW))
self.play(shape.animate.scale(1.5))
```

### Sequential text appearance

```python
title = Text("Title", font_size=72)
subtitle = Text("Subtitle", font_size=48)

self.play(Write(title))
self.wait(0.3)
self.play(FadeIn(subtitle, shift=UP))
```

### Grid creation

```python
grid = VGroup(*[
    Square(side_length=0.5).shift([i, j, 0])
    for i in range(-3, 4)
    for j in range(-2, 3)
])

self.play(LaggedStart(
    *[ShowCreation(square) for square in grid],
    lag_ratio=0.01
))
```

## Full Example

```python
class ComprehensiveCreation(Scene):
    def construct(self):
        # Title
        title = Text("Creation Animations", font_size=60)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Create shapes with different animations
        circle = Circle(radius=1, color=BLUE)
        circle.shift(LEFT * 3)

        square = Square(side_length=2, color=GREEN)
        square.set_fill(GREEN, opacity=0.5)

        triangle = Triangle(color=YELLOW)
        triangle.shift(RIGHT * 3)

        # Staggered creation
        self.play(
            ShowCreation(circle),
            FadeIn(square, scale=0.5),
            GrowFromCenter(triangle),
            run_time=2
        )
        self.wait()

        # Add formula
        formula = Tex(R"\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}")
        formula.next_to(title, DOWN, buff=1)
        self.play(Write(formula))
        self.wait(2)

        # Clear scene
        self.play(FadeOut(VGroup(title, circle, square, triangle, formula)))
```
