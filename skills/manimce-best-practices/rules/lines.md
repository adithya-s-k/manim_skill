---
name: lines
description: Line, Arrow, Vector, DashedLine and connectors
metadata:
  tags: line, arrow, vector, dashedline, brace, connector
---

# Lines and Arrows

Connect points and show relationships with lines and arrows.

## Line

Basic line between two points.

```python
from manim import *

class LineExample(Scene):
    def construct(self):
        # Line from two points
        line = Line(LEFT * 2, RIGHT * 2)

        # With styling
        styled_line = Line(
            UP * 2, DOWN * 2,
            color=BLUE,
            stroke_width=4
        )

        self.add(line, styled_line)
```

### Line Properties

```python
line = Line(LEFT, RIGHT)

# Get points
line.get_start()
line.get_end()
line.get_center()
line.get_length()
line.get_angle()

# Modify
line.put_start_and_end_on(new_start, new_end)
line.set_length(3)  # Keep direction, change length
```

## Arrow

Line with an arrowhead.

```python
class ArrowExample(Scene):
    def construct(self):
        # Basic arrow
        arrow = Arrow(LEFT * 2, RIGHT * 2)

        # Styled arrow
        styled = Arrow(
            start=UP,
            end=DOWN,
            color=RED,
            stroke_width=6,
            tip_length=0.4,
            max_tip_length_to_length_ratio=0.5
        )

        self.add(arrow, styled)
```

### Arrow Variations

```python
# Double-headed arrow
double = DoubleArrow(LEFT * 2, RIGHT * 2)

# Arrow with custom tip
arrow = Arrow(LEFT, RIGHT)
arrow.tip  # Access the tip mobject
```

## Vector

Arrow starting from origin (useful for physics/math).

```python
class VectorExample(Scene):
    def construct(self):
        # Vector from origin
        v1 = Vector([2, 1, 0], color=YELLOW)
        v2 = Vector([-1, 2, 0], color=GREEN)

        self.add(v1, v2)
```

## DashedLine

```python
class DashedLineExample(Scene):
    def construct(self):
        dashed = DashedLine(
            LEFT * 2, RIGHT * 2,
            dash_length=0.2,
            dashed_ratio=0.5,  # Ratio of dash to gap
            color=WHITE
        )
        self.add(dashed)
```

## TangentLine

Line tangent to a curve at a point.

```python
class TangentLineExample(Scene):
    def construct(self):
        circle = Circle(radius=2)

        # Tangent at specific point (t parameter 0-1 along curve)
        tangent = TangentLine(circle, alpha=0.25, length=3, color=YELLOW)

        self.add(circle, tangent)
```

## Brace

Curly brace for highlighting.

```python
class BraceExample(Scene):
    def construct(self):
        rect = Rectangle(width=4, height=1)

        # Brace under the rectangle
        brace = Brace(rect, DOWN)

        # With label
        brace_text = brace.get_text("Width")

        # Alternative: BraceLabel
        brace_label = BraceLabel(rect, "Width", DOWN)

        self.add(rect, brace, brace_text)
```

### Brace Directions

```python
brace_down = Brace(mobject, DOWN)
brace_up = Brace(mobject, UP)
brace_left = Brace(mobject, LEFT)
brace_right = Brace(mobject, RIGHT)
```

## CurvedArrow

Curved arrow between points.

```python
class CurvedArrowExample(Scene):
    def construct(self):
        curved = CurvedArrow(
            start_point=LEFT * 2,
            end_point=RIGHT * 2,
            angle=PI/2  # Curvature
        )
        self.add(curved)
```

## Elbow

Right-angle connector.

```python
class ElbowExample(Scene):
    def construct(self):
        elbow = Elbow(width=2, angle=PI/2)
        self.add(elbow)
```

## NumberLine Ticks

```python
class TicksExample(Scene):
    def construct(self):
        line = NumberLine(x_range=[-3, 3, 1])
        self.add(line)
```

## Connecting Mobjects

### Line Between Mobjects

```python
class ConnectMobjects(Scene):
    def construct(self):
        c1 = Circle().shift(LEFT * 2)
        c2 = Circle().shift(RIGHT * 2)

        # Line connecting centers
        line = Line(c1.get_center(), c2.get_center())

        # Arrow between edges
        arrow = Arrow(
            c1.get_right(),  # Right edge of c1
            c2.get_left(),   # Left edge of c2
            buff=0.1         # Small gap from edges
        )

        self.add(c1, c2, line, arrow)
```

### Dynamic Connections with Updaters

```python
class DynamicLine(Scene):
    def construct(self):
        dot1 = Dot(LEFT * 2)
        dot2 = Dot(RIGHT * 2)

        # Line that follows dots
        line = always_redraw(lambda: Line(
            dot1.get_center(),
            dot2.get_center(),
            color=YELLOW
        ))

        self.add(dot1, dot2, line)
        self.play(dot1.animate.shift(UP * 2), run_time=2)
```

## Best Practices

1. **Use Arrow for direction** - Clearer than plain lines
2. **Use Vector for physics/math** - Semantically meaningful
3. **Use Brace for labeling dimensions** - Professional look
4. **Use DashedLine for auxiliary lines** - Distinguishes from main content
5. **Use always_redraw for dynamic lines** - Updates with moving endpoints
