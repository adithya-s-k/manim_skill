---
name: shapes
description: Circle, Square, Rectangle, Polygon, Line, Arrow, Brace and connectors in ManimGX
metadata:
  tags: shapes, circle, square, rectangle, polygon, line, arrow, brace, geometry
---

# Shapes and lines in ManimGX

## Basic shapes

```python
import manimgx as m

class Shapes(m.Scene):
    def construct(self):
        circle = m.Circle(radius=1.5, color=m.BLUE, fill_opacity=0.5)
        square = m.Square(side_length=2, color=m.GREEN)
        rect = m.Rectangle(width=4, height=2, color=m.YELLOW)
        tri = m.Triangle(color=m.PURPLE)
        poly = m.Polygon(m.ORIGIN, m.RIGHT * 2, m.UP * 2, color=m.ORANGE)
        self.add(circle, square, rect, tri, poly)
```

More: `Ellipse(width=4, height=2)`, `RegularPolygon(n=6)`, `RoundedRectangle(width=4,
height=2, corner_radius=0.5)`.

## Circle helpers

```python
circle.get_radius()
circle.point_at_angle(m.PI / 4)
m.Circle().surround(triangle)                 # wrap another mobject
m.Circle().surround(triangle, buffer_factor=1.5)
```

## Lines and arrows

```python
line = m.Line(m.LEFT * 2, m.RIGHT * 2)
arrow = m.Arrow(m.LEFT * 2, m.RIGHT * 2, color=m.RED, stroke_width=6)
double = m.DoubleArrow(m.LEFT, m.RIGHT)
curved = m.CurvedArrow(m.LEFT, m.RIGHT, angle=m.PI / 2)
dashed = m.DashedLine(m.LEFT * 2, m.RIGHT * 2, dash_length=0.2)
vector = m.Vector([2, 1, 0], color=m.YELLOW)
```

## Braces

```python
rect = m.Rectangle(width=4, height=1)
brace = m.Brace(rect, m.DOWN)
label = brace.get_text("Width")
self.add(rect, brace, label)
```

Directions: `m.UP`, `m.DOWN`, `m.LEFT`, `m.RIGHT`.

## Connections

```python
c1 = m.Circle().shift(m.LEFT * 2)
c2 = m.Square().shift(m.RIGHT * 2)
line = m.Line(c1.get_center(), c2.get_center())
arrow = m.Arrow(c1.get_right(), c2.get_left(), buff=0.1)
```

Dynamic connections use `always_redraw` (see [updaters.md](updaters.md)):

```python
dot1 = m.Dot(m.LEFT * 2)
dot2 = m.Dot(m.RIGHT * 2)
line = m.always_redraw(lambda: m.Line(dot1.get_center(), dot2.get_center()))
```

## Styling

```python
shape.set_fill(m.BLUE, opacity=0.5)
shape.set_stroke(m.WHITE, width=3)
shape.set_color(m.RED)
```
