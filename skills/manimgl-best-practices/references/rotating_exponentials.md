# Rotating Exponentials - Reference Guide

**Example file**: `examples/rotating_exponentials.py`

## User Query Scenarios

This example addresses queries like:
- "Visualize e^(it) on the complex plane"
- "Show Euler's formula animation"
- "Demonstrate how cosine comes from rotating exponentials"
- "Create a complex plane with rotating vector"
- "Show e^(iπ) = -1 visually"

## Scene Thinking Process (3b1b Style)

### 1. Core Concept
**Euler's Formula**: `e^(it) = cos(t) + i·sin(t)` - a rotating unit vector in the complex plane. Two counter-rotating exponentials sum to give real cosine.

### 2. Visual Design Decisions

**Why use ComplexPlane?**
- Natural coordinate system for complex numbers
- Built-in grid and labels
- `n2p()` method converts complex to point

**Why show the traced path?**
- Reveals the unit circle emerges naturally
- Shows the relationship between angle and position

### 3. Technical Implementation

#### Rotating Vector with TracedPath
```python
time_tracker = ValueTracker(0)

vector = Vector(RIGHT, color=YELLOW)
vector.add_updater(lambda v: v.put_start_and_end_on(
    ORIGIN,
    plane.n2p(np.exp(1j * time_tracker.get_value()))
))

tip_dot = Dot(color=YELLOW)
tip_dot.add_updater(lambda d: d.move_to(vector.get_end()))

traced = TracedPath(tip_dot.get_center, stroke_color=BLUE)
```

#### Counter-Rotating for Cosine
```python
# e^(it) rotates counter-clockwise
v1.add_updater(lambda v: v.put_start_and_end_on(
    ORIGIN, plane.n2p(np.exp(1j * t))
))
# e^(-it) rotates clockwise
v2.add_updater(lambda v: v.put_start_and_end_on(
    ORIGIN, plane.n2p(np.exp(-1j * t))
))
# Sum is always real: 2cos(t)
```

### 4. Scene Variants

| Scene | Purpose |
|-------|---------|
| `RotatingExponential` | Basic e^(it) visualization |
| `CounterRotatingExponentials` | Shows e^(it) + e^(-it) = 2cos(t) |
| `EulersFormula` | Famous e^(iπ) = -1 |
| `ComplexExponentialSpiral` | Decaying spiral e^((a+bi)t) |

## Key Patterns

### Pattern: always_redraw for Arcs
```python
angle_arc = always_redraw(lambda: Arc(
    start_angle=0,
    angle=time_tracker.get_value() % TAU,
    radius=0.3,
    color=GREEN
))
```

### Pattern: Complex Number to Point
```python
# Using ComplexPlane.n2p() (number to point)
point = plane.n2p(1 + 2j)  # Complex number
point = plane.n2p(np.exp(1j * theta))  # Euler form
```

## Run Commands

```bash
manimgl rotating_exponentials.py RotatingExponential -w
manimgl rotating_exponentials.py CounterRotatingExponentials -w
manimgl rotating_exponentials.py EulersFormula -w
manimgl rotating_exponentials.py ComplexExponentialSpiral -w
```
