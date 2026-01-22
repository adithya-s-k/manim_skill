# Integration Visualization - Reference Guide

**Example file**: `examples/integration_visualization.py`

## User Query Scenarios

This example addresses queries like:
- "Show the area under a curve"
- "Visualize Riemann sums converging to integral"
- "Animate definite integral accumulation"
- "Show integral of e^(-x) equals 1"

## Scene Thinking Process (3b1b Style)

### 1. Core Concept
**Definite Integral**: The integral ∫f(x)dx represents accumulated area under curve f(x). Riemann sums with shrinking rectangles converge to the true integral.

### 2. Technical Implementation

#### Animated Area Fill (Using Polygon)
```python
def get_area_polygon():
    t = t_tracker.get_value()
    xs = np.linspace(0, t, 50)
    # Points along curve
    points = [axes.c2p(x, f(x)) for x in xs]
    # Close the polygon along x-axis
    points.append(axes.c2p(t, 0))
    points.append(axes.c2p(0, 0))
    poly = Polygon(*points)
    poly.set_fill(BLUE_E, opacity=0.5)
    poly.set_stroke(width=0)
    return poly

area = always_redraw(get_area_polygon)
```

**Key insight**: ManimGL doesn't have `axes.get_area()`, so build polygons manually from curve points.

#### Riemann Sum Rectangles
```python
for i in range(n):
    x = start + i * dx
    height = f(x)
    rect = Rectangle(
        width=dx * axes.x_axis.get_unit_size(),
        height=height * axes.y_axis.get_unit_size(),
    )
    rect.move_to(axes.c2p(x + dx/2, height/2))
```

### 3. Scene Variants

| Scene | Purpose |
|-------|---------|
| `AreaUnderCurve` | Basic accumulating area animation |
| `RiemannSums` | Rectangles converging (n=4,8,16,32) |
| `ExponentialDecay` | ∫e^(-x)dx = 1 with live area counter |

## Key Patterns

### Pattern: Live Value Display
```python
value_label = Tex(r"\text{Area} \approx 0.00")
value_num = value_label.make_number_changeable("0.00")
value_num.add_updater(lambda m: m.set_value(computed_area))
```

### Pattern: Progressive Rectangle Refinement
```python
for n in [4, 8, 16, 32]:
    new_rects = create_rectangles(n)
    self.play(ReplacementTransform(current_rects, new_rects))
    current_rects = new_rects
```

## Run Commands

```bash
manimgl integration_visualization.py AreaUnderCurve -w
manimgl integration_visualization.py RiemannSums -w
manimgl integration_visualization.py ExponentialDecay -w
```
