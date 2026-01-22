---
name: mobjects
description: Mobject types, VMobject, and the mobject hierarchy in Manim
metadata:
  tags: mobject, vmobject, group, submobjects, hierarchy
---

# Mobjects in Manim

Mobject (Mathematical Object) is the base class for all displayable objects in Manim.

## Mobject Hierarchy

```
Mobject (base class)
├── VMobject (Vectorized Mobject - most common)
│   ├── Circle, Square, Rectangle, Polygon
│   ├── Line, Arrow, Vector
│   ├── Text, MathTex, Tex
│   ├── Axes, NumberPlane
│   └── VGroup
├── ImageMobject (for images)
├── PMobject (point clouds)
└── Group (for non-VMobject collections)
```

## VMobject (Vectorized Mobject)

Most shapes you'll use are VMobjects - they're defined by Bézier curves.

```python
# Common VMobjects
circle = Circle()
square = Square()
rect = Rectangle(width=4, height=2)
triangle = Triangle()
polygon = Polygon(ORIGIN, RIGHT, UP)
line = Line(LEFT, RIGHT)
arrow = Arrow(LEFT, RIGHT)
```

## Creating Custom VMobjects

```python
class CustomShape(VMobject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Define points using set_points_as_corners or set_points_smoothly
        self.set_points_as_corners([
            LEFT, UP, RIGHT, DOWN, LEFT
        ])
```

## Mobject Properties

### Position and Size

```python
mobject.get_center()      # Returns center point
mobject.get_width()       # Returns width
mobject.get_height()      # Returns height
mobject.get_top()         # Top edge center point
mobject.get_bottom()      # Bottom edge center point
mobject.get_left()        # Left edge center point
mobject.get_right()       # Right edge center point
```

### Bounding Box Corners

```python
mobject.get_corner(UL)    # Upper left corner
mobject.get_corner(UR)    # Upper right corner
mobject.get_corner(DL)    # Lower left corner
mobject.get_corner(DR)    # Lower right corner
```

## Submobjects

Mobjects can contain other mobjects as submobjects.

```python
# Access submobjects
group = VGroup(Circle(), Square())
group.submobjects      # List of child mobjects
group[0]               # First submobject (Circle)
group[1]               # Second submobject (Square)

# Iterate over submobjects
for mob in group:
    mob.set_color(RED)
```

## Copying Mobjects

```python
# Create a copy
circle_copy = circle.copy()

# Copy and position
circle_copy = circle.copy().shift(RIGHT * 2)
```

## Method Chaining

Most mobject methods return `self`, allowing method chaining:

```python
circle = Circle().set_color(RED).shift(LEFT).scale(2)
```

## Best Practices

1. **Use VMobject for custom shapes** - Better rendering and animation support
2. **Prefer VGroup over Group** - VGroup works better with most animations
3. **Use copy() when reusing** - Avoid unintended modifications to original
4. **Chain methods for readability** - But break into lines if too long
