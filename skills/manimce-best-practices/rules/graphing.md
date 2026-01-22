---
name: graphing
description: Plotting functions, parametric curves, and data visualization
metadata:
  tags: plot, graph, function, parametric, curve, data
---

# Graphing Functions

Plot mathematical functions and curves.

## Plotting Functions on Axes

```python
from manim import *

class BasicPlot(Scene):
    def construct(self):
        axes = Axes(x_range=[-3, 3], y_range=[-2, 8])

        # Plot a function
        graph = axes.plot(lambda x: x**2, color=BLUE)

        self.add(axes, graph)
```

## plot() Parameters

```python
class PlotParameters(Scene):
    def construct(self):
        axes = Axes(x_range=[-5, 5], y_range=[-2, 2])

        graph = axes.plot(
            lambda x: np.sin(x),
            x_range=[-PI, PI],    # Limit domain
            color=YELLOW,
            stroke_width=4,
        )

        self.add(axes, graph)
```

## Multiple Functions

```python
class MultiplePlots(Scene):
    def construct(self):
        axes = Axes(x_range=[-3, 3], y_range=[-2, 10])

        sin_graph = axes.plot(lambda x: np.sin(x), color=BLUE)
        cos_graph = axes.plot(lambda x: np.cos(x), color=RED)
        quad_graph = axes.plot(lambda x: x**2, color=GREEN)

        self.add(axes, sin_graph, cos_graph, quad_graph)
```

## Adding Labels to Graphs

```python
class GraphLabels(Scene):
    def construct(self):
        axes = Axes(x_range=[-3, 3], y_range=[-2, 10])
        graph = axes.plot(lambda x: x**2, color=BLUE)

        # Add label to graph
        label = axes.get_graph_label(
            graph,
            label=MathTex("y = x^2"),
            x_val=2,
            direction=UR
        )

        self.add(axes, graph, label)
```

## Parametric Curves

Plot curves defined by parametric equations.

```python
class ParametricExample(Scene):
    def construct(self):
        axes = Axes(x_range=[-3, 3], y_range=[-3, 3])

        # Circle: x = cos(t), y = sin(t)
        curve = axes.plot_parametric_curve(
            lambda t: np.array([np.cos(t), np.sin(t), 0]),
            t_range=[0, 2 * PI],
            color=YELLOW
        )

        self.add(axes, curve)
```

### Parametric Curve Examples

```python
# Lissajous curve
curve = axes.plot_parametric_curve(
    lambda t: np.array([np.sin(3*t), np.sin(2*t), 0]),
    t_range=[0, 2*PI],
)

# Spiral
curve = axes.plot_parametric_curve(
    lambda t: np.array([t*np.cos(t), t*np.sin(t), 0]),
    t_range=[0, 4*PI],
)

# Heart curve
curve = axes.plot_parametric_curve(
    lambda t: np.array([
        16 * np.sin(t)**3,
        13*np.cos(t) - 5*np.cos(2*t) - 2*np.cos(3*t) - np.cos(4*t),
        0
    ]) / 10,
    t_range=[0, 2*PI],
)
```

## ParametricFunction (standalone)

Create parametric curves without axes:

```python
class StandaloneParametric(Scene):
    def construct(self):
        curve = ParametricFunction(
            lambda t: np.array([np.cos(t), np.sin(t), 0]),
            t_range=[0, 2*PI],
            color=BLUE
        )
        self.add(curve)
```

## Area Under Curve

```python
class AreaUnderCurve(Scene):
    def construct(self):
        axes = Axes(x_range=[-1, 5], y_range=[-1, 10])
        graph = axes.plot(lambda x: x**2, x_range=[0, 3], color=BLUE)

        # Shade area under curve
        area = axes.get_area(
            graph,
            x_range=[0, 2],
            color=BLUE,
            opacity=0.5
        )

        self.add(axes, graph, area)
```

## Riemann Rectangles

```python
class RiemannRectangles(Scene):
    def construct(self):
        axes = Axes(x_range=[-1, 5], y_range=[-1, 10])
        graph = axes.plot(lambda x: x**2, color=BLUE)

        rects = axes.get_riemann_rectangles(
            graph,
            x_range=[0, 3],
            dx=0.5,
            color=YELLOW,
            stroke_width=1
        )

        self.add(axes, graph, rects)
```

## Animated Graphing

```python
class AnimatedGraph(Scene):
    def construct(self):
        axes = Axes(x_range=[-3, 3], y_range=[-2, 2])
        self.add(axes)

        graph = axes.plot(lambda x: np.sin(x), color=BLUE)

        # Animate the graph being drawn
        self.play(Create(graph), run_time=3)
```

## Moving Point on Graph

```python
class MovingPointOnGraph(Scene):
    def construct(self):
        axes = Axes(x_range=[-3, 3], y_range=[-2, 2])
        graph = axes.plot(lambda x: np.sin(x), color=BLUE)

        # Point that follows graph
        x_tracker = ValueTracker(-3)

        dot = always_redraw(lambda: Dot(
            axes.i2gp(x_tracker.get_value(), graph),
            color=YELLOW
        ))

        self.add(axes, graph, dot)
        self.play(x_tracker.animate.set_value(3), run_time=4)
```

## 3D Surface Plots

```python
class SurfacePlot(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()

        surface = axes.plot_surface(
            lambda u, v: np.sin(u) * np.cos(v),
            u_range=[-PI, PI],
            v_range=[-PI, PI],
            colorscale=[BLUE, GREEN, YELLOW],
        )

        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)
        self.add(axes, surface)
```

## Best Practices

1. **Set x_range on plot for discontinuities** - Avoid graphing undefined regions
2. **Use get_graph_label for clarity** - Label functions on the graph
3. **Match graph color to concept** - Consistent color coding
4. **Use i2gp for points on graphs** - Automatically handles conversion
5. **Animate graph creation** - More engaging than static display
