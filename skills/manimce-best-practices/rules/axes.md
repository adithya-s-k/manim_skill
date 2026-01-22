---
name: axes
description: Axes, NumberPlane, and coordinate systems in Manim
metadata:
  tags: axes, numberplane, coordinate, grid, numberline
---

# Coordinate Systems

Create axes, grids, and number lines for mathematical visualizations.

## Axes

Basic 2D coordinate axes.

```python
from manim import *

class AxesExample(Scene):
    def construct(self):
        # Default axes
        axes = Axes()
        self.add(axes)
```

### Customizing Axes

```python
class CustomAxes(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-5, 5, 1],      # [min, max, step]
            y_range=[-3, 3, 1],
            x_length=10,              # Physical length on screen
            y_length=6,
            axis_config={
                "color": BLUE,
                "include_tip": True,
                "include_numbers": True,
            },
            x_axis_config={
                "numbers_to_include": [-4, -2, 0, 2, 4],
            },
            y_axis_config={
                "numbers_to_include": [-2, 0, 2],
            },
        )
        self.add(axes)
```

### Adding Labels

```python
class AxesLabels(Scene):
    def construct(self):
        axes = Axes(x_range=[-5, 5], y_range=[-3, 3])

        # Add axis labels
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")

        # Custom labels
        x_label = axes.get_x_axis_label(MathTex(r"\theta"))
        y_label = axes.get_y_axis_label(MathTex(r"f(\theta)"))

        self.add(axes, x_label, y_label)
```

## NumberPlane

Grid with axes - shows coordinate lines.

```python
class NumberPlaneExample(Scene):
    def construct(self):
        # Default plane
        plane = NumberPlane()
        self.add(plane)
```

### Customizing NumberPlane

```python
class CustomPlane(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
            axis_config={
                "color": WHITE,
            },
        )
        self.add(plane)
```

## ComplexPlane

For visualizing complex numbers.

```python
class ComplexPlaneExample(Scene):
    def construct(self):
        plane = ComplexPlane()

        # Plot complex number
        z = complex(2, 1)  # 2 + i
        dot = Dot(plane.n2p(z), color=YELLOW)
        label = MathTex("2+i").next_to(dot, UR)

        self.add(plane, dot, label)
```

## NumberLine

Single axis line.

```python
class NumberLineExample(Scene):
    def construct(self):
        line = NumberLine(
            x_range=[-5, 5, 1],
            length=10,
            include_numbers=True,
            include_tip=True,
        )
        self.add(line)
```

## Coordinate Conversions

```python
class CoordinateConversion(Scene):
    def construct(self):
        axes = Axes(x_range=[-5, 5], y_range=[-3, 3])

        # Convert coordinates to screen position
        point = axes.c2p(2, 1)  # coords_to_point: (2, 1) -> screen position

        # Convert screen position to coordinates
        coords = axes.p2c(point)  # point_to_coords: screen -> (x, y)

        dot = Dot(point, color=RED)
        self.add(axes, dot)
```

### Shorthand Methods

```python
axes = Axes()

# c2p = coords_to_point
axes.c2p(x, y)

# p2c = point_to_coords
axes.p2c(point)

# i2gp = input_to_graph_point (for graphs)
axes.i2gp(x, graph)

# For NumberPlane/ComplexPlane
plane.n2p(complex_number)  # number_to_point
plane.p2n(point)           # point_to_number
```

## ThreeDAxes

For 3D visualizations.

```python
class ThreeDAxesExample(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-4, 4, 1],
            x_length=8,
            y_length=8,
            z_length=6,
        )

        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.add(axes)
```

## Plotting Points

```python
class PlotPoints(Scene):
    def construct(self):
        axes = Axes(x_range=[-5, 5], y_range=[-3, 3])

        points = [(1, 2), (-2, 1), (3, -1), (0, 2)]
        dots = VGroup(*[
            Dot(axes.c2p(x, y), color=YELLOW)
            for x, y in points
        ])

        self.add(axes, dots)
```

## Best Practices

1. **Set appropriate ranges** - Don't include unnecessary empty space
2. **Match x_length/y_length to range ratio** - Prevents distortion
3. **Use NumberPlane for transformations** - Grid shows distortion clearly
4. **Use c2p for all coordinate work** - Don't manually convert
5. **Include numbers sparingly** - Too many numbers clutter the display
