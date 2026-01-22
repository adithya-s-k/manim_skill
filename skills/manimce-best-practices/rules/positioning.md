---
name: positioning
description: move_to, next_to, align_to, shift and positioning methods
metadata:
  tags: position, move_to, next_to, shift, align, layout
---

# Positioning in Manim

Methods for placing and moving mobjects in the scene.

## Coordinate System

Manim uses a coordinate system where:
- Origin (0, 0, 0) is at the center of the screen
- X-axis: LEFT (-) to RIGHT (+)
- Y-axis: DOWN (-) to UP (+)
- Z-axis: IN (-) to OUT (+) (for 3D)

### Direction Constants
```python
UP = np.array([0, 1, 0])
DOWN = np.array([0, -1, 0])
LEFT = np.array([-1, 0, 0])
RIGHT = np.array([1, 0, 0])
ORIGIN = np.array([0, 0, 0])

# Diagonals
UL = UP + LEFT      # Upper left
UR = UP + RIGHT     # Upper right
DL = DOWN + LEFT    # Lower left
DR = DOWN + RIGHT   # Lower right
```

## move_to

Move to an absolute position.

```python
from manim import *

class MoveToExample(Scene):
    def construct(self):
        circle = Circle()

        # Move to origin
        circle.move_to(ORIGIN)

        # Move to specific coordinates
        circle.move_to(RIGHT * 2 + UP * 1)

        # Move to another mobject's position
        square = Square().shift(LEFT * 2)
        circle.move_to(square)

        # Move to a specific point of another mobject
        circle.move_to(square.get_top())
```

## shift

Move relative to current position.

```python
class ShiftExample(Scene):
    def construct(self):
        circle = Circle()

        # Shift in one direction
        circle.shift(RIGHT)
        circle.shift(UP * 2)

        # Shift in multiple directions
        circle.shift(RIGHT * 2 + UP * 1)

        # Chain shifts
        circle.shift(LEFT).shift(DOWN)
```

## next_to

Position relative to another mobject.

```python
class NextToExample(Scene):
    def construct(self):
        square = Square()
        circle = Circle()
        triangle = Triangle()

        # Place circle to the right of square
        circle.next_to(square, RIGHT)

        # With buffer (spacing)
        triangle.next_to(square, DOWN, buff=0.5)

        # Aligned to specific edge
        circle.next_to(square, RIGHT, aligned_edge=UP)
```

### buff Parameter
```python
# Default buffer
circle.next_to(square, RIGHT)  # Uses DEFAULT_MOBJECT_TO_MOBJECT_BUFFER

# Custom buffer
circle.next_to(square, RIGHT, buff=0)    # No gap
circle.next_to(square, RIGHT, buff=1)    # 1 unit gap
circle.next_to(square, RIGHT, buff=0.5)  # Half unit gap
```

## align_to

Align edges with another mobject.

```python
class AlignToExample(Scene):
    def construct(self):
        square = Square().shift(LEFT)
        circle = Circle().shift(RIGHT)

        # Align circle's left edge with square's left edge
        circle.align_to(square, LEFT)

        # Align tops
        circle.align_to(square, UP)

        # Align to a point
        circle.align_to(ORIGIN, DOWN)
```

## Edge Methods

Position at screen edges.

```python
class EdgeExample(Scene):
    def construct(self):
        # To screen edges
        text1 = Text("Top").to_edge(UP)
        text2 = Text("Bottom").to_edge(DOWN)
        text3 = Text("Left").to_edge(LEFT)
        text4 = Text("Right").to_edge(RIGHT)

        # With buffer
        text5 = Text("Buffered").to_edge(UP, buff=1)
```

## Corner Methods

Position at screen corners.

```python
class CornerExample(Scene):
    def construct(self):
        t1 = Text("UL").to_corner(UL)
        t2 = Text("UR").to_corner(UR)
        t3 = Text("DL").to_corner(DL)
        t4 = Text("DR").to_corner(DR)

        # With buffer
        t5 = Text("Buffered").to_corner(UL, buff=0.5)
```

## center

Center on screen or another mobject.

```python
mobject.center()           # Center on screen
mobject.center_on(other)   # Center on another mobject (custom helper)
```

## Getting Positions

```python
circle = Circle()

# Get various points
circle.get_center()        # Center point
circle.get_top()           # Top edge center
circle.get_bottom()        # Bottom edge center
circle.get_left()          # Left edge center
circle.get_right()         # Right edge center
circle.get_corner(UL)      # Upper left corner
circle.get_corner(DR)      # Lower right corner
circle.get_start()         # Start of path
circle.get_end()           # End of path
```

## Animated Positioning

```python
class AnimatedPosition(Scene):
    def construct(self):
        square = Square()
        self.add(square)

        # Animate movement
        self.play(square.animate.shift(RIGHT * 2))
        self.play(square.animate.move_to(UP * 2))
        self.play(square.animate.to_edge(LEFT))
```

## Best Practices

1. **Use next_to for relative positioning** - Maintains relationships
2. **Use move_to for absolute positioning** - Precise coordinates
3. **Use shift for relative adjustments** - Quick tweaks
4. **Use to_edge/to_corner for screen positioning** - Responsive layouts
5. **Adjust buff for visual spacing** - Don't let elements crowd
