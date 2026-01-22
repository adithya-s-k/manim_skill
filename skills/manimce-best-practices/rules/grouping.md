---
name: grouping
description: VGroup, Group, arrange, and layout patterns
metadata:
  tags: vgroup, group, arrange, layout, grid, submobjects
---

# Grouping Mobjects

Organize multiple mobjects into groups for collective manipulation.

## VGroup

VGroup (Vectorized Group) is for grouping VMobjects. Most commonly used.

```python
from manim import *

class VGroupExample(Scene):
    def construct(self):
        # Create a group
        group = VGroup(
            Circle(),
            Square(),
            Triangle()
        )

        # Operations apply to all members
        group.set_color(RED)
        group.shift(UP)

        self.add(group)
```

## Group

Group is for mixing different mobject types (VMobjects, ImageMobjects, etc.).

```python
class GroupExample(Scene):
    def construct(self):
        # Mix different types
        text = Text("Hello")
        group = Group(
            Circle(),
            text
        )
        self.add(group)
```

## Creating Groups

```python
# From individual mobjects
group = VGroup(circle, square, triangle)

# From a list
shapes = [Circle(), Square(), Triangle()]
group = VGroup(*shapes)

# Using list comprehension
group = VGroup(*[Circle() for _ in range(5)])

# Empty group, add later
group = VGroup()
group.add(Circle())
group.add(Square())
```

## arrange

Arrange mobjects in a line.

```python
class ArrangeExample(Scene):
    def construct(self):
        # Horizontal arrangement (default)
        row = VGroup(*[Circle().scale(0.3) for _ in range(5)])
        row.arrange(RIGHT, buff=0.5).shift(UP * 2)

        # Vertical arrangement
        column = VGroup(*[Square().scale(0.3) for _ in range(4)])
        column.arrange(DOWN, buff=0.5).shift(LEFT * 2)

        # With custom buffer
        spaced = VGroup(*[Triangle().scale(0.3) for _ in range(3)])
        spaced.arrange(RIGHT, buff=1).shift(DOWN * 2)

        self.add(row, column, spaced)
```

### Direction Options
```python
group.arrange(RIGHT)      # Left to right
group.arrange(LEFT)       # Right to left
group.arrange(UP)         # Bottom to top
group.arrange(DOWN)       # Top to bottom
```

## arrange_in_grid

Arrange in a grid pattern.

```python
class GridExample(Scene):
    def construct(self):
        # Auto grid
        grid = VGroup(*[Square().scale(0.3) for _ in range(20)])
        grid.arrange_in_grid()

        # Specify rows and columns
        grid = VGroup(*[Circle().scale(0.2) for _ in range(12)])
        grid.arrange_in_grid(rows=3, cols=4)

        # With spacing
        grid.arrange_in_grid(rows=3, cols=4, buff=0.5)

        self.add(grid)
```

## Accessing Group Members

```python
group = VGroup(Circle(), Square(), Triangle())

# By index
first = group[0]          # Circle
second = group[1]         # Square
last = group[-1]          # Triangle

# Slicing
first_two = group[0:2]    # VGroup with Circle and Square

# Iteration
for mob in group:
    mob.set_color(random_color())

# Length
num_items = len(group)
```

## Modifying Groups

```python
group = VGroup(Circle(), Square())

# Add mobjects
group.add(Triangle())
group.add(Star(), Pentagon())

# Remove mobjects
group.remove(circle)

# Insert at position
group.insert(0, new_mobject)

# Submobjects list
group.submobjects  # List of all children
```

## Group Transformations

```python
group = VGroup(Circle(), Square(), Triangle()).arrange(RIGHT)

# All transformations apply to entire group
group.shift(UP * 2)
group.scale(0.5)
group.rotate(PI / 4)
group.set_color(BLUE)

# But can target individuals
group[0].set_color(RED)  # Just the circle
```

## Nested Groups

```python
class NestedGroups(Scene):
    def construct(self):
        # Create sub-groups
        row1 = VGroup(*[Circle() for _ in range(3)]).arrange(RIGHT)
        row2 = VGroup(*[Square() for _ in range(3)]).arrange(RIGHT)
        row3 = VGroup(*[Triangle() for _ in range(3)]).arrange(RIGHT)

        # Group of groups
        all_rows = VGroup(row1, row2, row3).arrange(DOWN)

        self.add(all_rows)
```

## Useful Group Methods

```python
group = VGroup(Circle(), Square(), Triangle())

# Get bounding box info
group.get_center()
group.get_width()
group.get_height()

# Set position for whole group
group.move_to(ORIGIN)
group.to_edge(LEFT)

# Copy entire group
group_copy = group.copy()

# Match layout of another group
group1.match_height(group2)
group1.match_width(group2)
```

## Best Practices

1. **Use VGroup for VMobjects** - Better performance and compatibility
2. **Use arrange after creating** - Don't position individually then group
3. **Name your groups semantically** - `equation_parts` not `group1`
4. **Use nested groups for structure** - Rows within columns, etc.
5. **Copy groups when needed** - Avoid unintended modifications
