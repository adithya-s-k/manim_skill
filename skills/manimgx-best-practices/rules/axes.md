---
name: axes
description: Axes, NumberPlane, FunctionGraph and plotting in ManimGX
metadata:
  tags: axes, numberplane, functiongraph, plot, graph, coordinate
---

# Axes and graphing in ManimGX

## Axes

```python
import manimgx as m

class Plot(m.Scene):
    def construct(self):
        axes = m.Axes(x_range=[-3, 3], y_range=[-2, 2])
        curve = axes.plot(lambda x: x**2, color=m.BLUE)
        self.play(m.Create(axes), m.Create(curve))
```

- `x_range` / `y_range` are `[min, max, step]` (step optional).
- `axes.plot(fn, x_range=[...], color=...)` draws a function.
- `axes.c2p(x, y)` converts data coordinates to scene points.

## Labels and ticks

```python
labels = axes.get_axis_labels(x_label="x", y_label="y")
numbers = axes.get_number_labels()
self.add(labels)
```

## FunctionGraph

```python
graph = m.FunctionGraph(lambda x: x**2, x_range=[-3, 3], color=m.YELLOW)
```

`FunctionGraph` is independent of `Axes`; use it when you do not need tick marks.

## NumberLine and NumberPlane

```python
line = m.NumberLine(x_range=[-3, 3, 1])
plane = m.NumberPlane()
```

## Area under a curve

```python
area = axes.get_area(curve, x_range=[0, 2], color=m.BLUE, opacity=0.4)
self.add(area)
```

## Parametric curves

```python
import numpy as np

curve = m.ParametricFunction(
    lambda t: [np.cos(t), np.sin(t), 0],
    t_range=[0, 2 * np.pi],
)
```

Import NumPy yourself (`import numpy as np`); do not rely on ManimGX's star import to provide
it.
