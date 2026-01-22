# ManimGL Mobjects

## Mobject Hierarchy

```
Mobject (base class)
├── VMobject (vectorized - most common)
│   ├── VGroup
│   ├── Circle, Square, Rectangle, Line, Arrow
│   ├── Tex, Text, TexText
│   └── Axes, NumberPlane
├── Group (non-vectorized container)
├── ImageMobject
├── Point
└── 3D objects (Surface, ParametricSurface, etc.)
```

## Creating Mobjects

```python
# Geometric shapes
circle = Circle(radius=1, color=BLUE)
square = Square(side_length=2)
rect = Rectangle(width=3, height=2)
line = Line(LEFT, RIGHT)
arrow = Arrow(ORIGIN, UP)

# Text
text = Text("Hello")
math = Tex(R"\pi r^2")

# Groups
group = VGroup(circle, square)
```

## Positioning

```python
# Absolute position
circle.move_to(ORIGIN)
circle.move_to(RIGHT * 2 + UP)

# Relative to screen edges
circle.to_edge(UP)
circle.to_edge(LEFT, buff=1)
circle.to_corner(UL)

# Relative to other mobjects
square.next_to(circle, RIGHT)
square.next_to(circle, DOWN, buff=0.5)

# Alignment
group.align_to(other, UP)
group.align_to(other, LEFT)

# Shifting
circle.shift(RIGHT * 2)
circle.shift(UP + RIGHT)
```

## Styling

```python
# Fill
circle.set_fill(BLUE, opacity=0.5)

# Stroke (outline)
circle.set_stroke(WHITE, width=2)
circle.set_stroke(color=RED, width=4, opacity=0.8)

# Both
circle.set_style(
    fill_color=BLUE,
    fill_opacity=0.5,
    stroke_color=WHITE,
    stroke_width=2
)

# Color (affects both fill and stroke)
circle.set_color(RED)

# Backstroke (outline behind for readability)
text.set_backstroke(BLACK, 5)
```

## VGroup

Container for vectorized mobjects:

```python
# Create group
shapes = VGroup(circle, square, triangle)

# Arrange
shapes.arrange(RIGHT, buff=0.5)
shapes.arrange(DOWN, aligned_edge=LEFT)
shapes.arrange_in_grid(rows=2, cols=3)

# Apply to all
shapes.set_color(BLUE)
shapes.scale(0.5)
shapes.shift(UP)

# Access elements
shapes[0]  # First element
shapes[-1]  # Last element
shapes[1:3]  # Slice
```

## Group vs VGroup

```python
# VGroup - for vectorized mobjects (VMobject subclasses)
vgroup = VGroup(Circle(), Square())

# Group - for any mobjects including images, 3D, etc.
group = Group(ImageMobject("photo.png"), Circle())
```

## Common Methods

| Method | Description |
|--------|-------------|
| `.move_to(point)` | Move center to point |
| `.shift(vector)` | Move by vector |
| `.scale(factor)` | Scale by factor |
| `.rotate(angle)` | Rotate by angle (radians) |
| `.next_to(mob, dir)` | Position next to another |
| `.align_to(mob, dir)` | Align edge with another |
| `.to_edge(dir)` | Move to screen edge |
| `.to_corner(corner)` | Move to screen corner |
| `.get_center()` | Get center point |
| `.get_width()` | Get width |
| `.get_height()` | Get height |
| `.copy()` | Create a copy |

## Generating Targets

For animating to a modified version:

```python
circle.generate_target()
circle.target.shift(RIGHT * 2)
circle.target.scale(2)
circle.target.set_color(RED)

self.play(MoveToTarget(circle))
```

## Saving and Restoring State

```python
circle.save_state()
self.play(circle.animate.shift(RIGHT).scale(2))
# Later...
self.play(Restore(circle))
```

## Updaters

Dynamic behavior:

```python
# Always follow another mobject
label.add_updater(lambda m: m.next_to(dot, UP))

# Time-based
circle.add_updater(lambda m, dt: m.rotate(dt))

# Value-based with ValueTracker
tracker = ValueTracker(0)
circle.add_updater(
    lambda m: m.set_fill(opacity=tracker.get_value())
)
self.play(tracker.animate.set_value(1))
```

## Useful Shortcuts

```python
# f_always for common updater patterns
label.f_always.next_to(dot, UP)

# always (function form)
always(label.next_to, dot, UP)
```
