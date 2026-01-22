# Vector Fields - Reference Guide

**Example file**: `examples/vector_fields.py`

## User Query Scenarios

This example addresses queries like:
- "Create a vector field visualization"
- "Show particles flowing through a field"
- "Visualize electric field from charges"
- "Animate gradient descent"
- "Show fluid flow"

## Scene Thinking Process (3b1b Style)

### 1. Core Concept
**Vector Fields**: At each point in space, there's a vector showing direction and magnitude. Particles follow the field, revealing flow patterns.

### 2. Technical Implementation

#### Manual Arrow Field (Portable Approach)
```python
arrows = VGroup()
for x in np.arange(-3.5, 4, 0.7):
    for y in np.arange(-2.5, 3, 0.7):
        vx, vy = -y * 0.15, x * 0.15  # Rotation field
        arrow = Arrow(
            start=[x, y, 0],
            end=[x + vx, y + vy, 0],
            buff=0,
            stroke_width=2,
        )
        # Color by magnitude
        mag = np.sqrt(vx**2 + vy**2)
        arrow.set_color(interpolate_color(BLUE, YELLOW, mag / 0.5))
        arrows.add(arrow)
```

#### Particle Following Field
```python
def follow_field(mob, dt):
    x, y = mob.get_center()[:2]
    vx, vy = field_func(x, y)
    mob.shift(np.array([vx, vy, 0]) * dt)

dot.add_updater(follow_field)
trail = TracedPath(dot.get_center, stroke_color=RED)
```

#### Electric Dipole Field
```python
def E_field(pos):
    r1, r2 = pos - q1_pos, pos - q2_pos
    d1, d2 = np.linalg.norm(r1), np.linalg.norm(r2)
    E1 = r1 / d1**3   # From + charge
    E2 = -r2 / d2**3  # From - charge
    return E1 + E2
```

### 3. Scene Variants

| Scene | Purpose |
|-------|---------|
| `SimpleVectorField` | Rotation field with particle |
| `GradientFieldDemo` | Scalar field + gradient arrows |
| `ParticleFlow` | Multiple particles in vortex |
| `ElectricDipole` | Field from +/- charges |

## Key Patterns

### Pattern: Color by Magnitude
```python
mag = np.linalg.norm([vx, vy])
color = interpolate_color(BLUE, YELLOW, min(mag * scale, 1))
arrow.set_color(color)
```

### Pattern: LaggedStartMap for Many Arrows
```python
self.play(LaggedStartMap(GrowArrow, arrows, lag_ratio=0.02, run_time=2))
```

### Pattern: Closure for Updaters in Loops
```python
for i in range(n):
    dot = Dot(...)
    def make_updater():  # Closure captures current state
        def update(mob, dt):
            # use mob, not dot
            ...
        return update
    dot.add_updater(make_updater())
```

## Run Commands

```bash
manimgl vector_fields.py SimpleVectorField -w
manimgl vector_fields.py GradientFieldDemo -w
manimgl vector_fields.py ParticleFlow -w
manimgl vector_fields.py ElectricDipole -w
```
