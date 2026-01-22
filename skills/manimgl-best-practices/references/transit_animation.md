# Transit Animations - Reference Guide

**Example file**: `examples/transit_animation.py`

## User Query Scenarios

This example addresses queries like:
- "Create a planet transit animation"
- "Show loading dots animation"
- "Animate a pendulum swing"
- "Create wave propagation"
- "Show orbital motion"

## Scene Thinking Process (3b1b Style)

### 1. Core Concept
**Transit/Periodic Motion**: Objects moving along paths, leaving traces, showing periodic behavior. Used for astronomical transits, loading indicators, physics demos.

### 2. Technical Implementation

#### Transit with Snapshots
```python
venus.add_updater(lambda m, dt: m.shift(dt * velocity * RIGHT))
copies = VGroup()
for _ in range(n_snapshots):
    self.wait(wait_time)
    copies.add(venus.copy().clear_updaters())
self.play(Transform(copies, VGroup(path)))  # Collapse to line
```

#### Orbital Motion with Depth Effect
```python
def update_planet(p):
    a = angle.get_value()
    x = 2.5 * np.cos(a)
    y = 0.5 * np.sin(a)  # Compressed y = tilted orbit
    p.move_to([x, y, 0])
    # Size varies with "depth"
    scale = 0.12 + 0.06 * np.sin(a)
    p.set_width(2 * scale)
```

#### Phase-Shifted Oscillation (Loading Dots)
```python
for i, dot in enumerate(dots):
    phase = i * TAU / n_dots
    dot.add_updater(lambda m, p=phase: m.set_y(
        original_y + 0.3 * np.sin(3 * time.get_value() + p)
    ))
```

#### Pendulum Physics
```python
omega = np.sqrt(g / length)  # Natural frequency
amplitude = PI / 4
theta.add_updater(lambda m: m.set_value(
    amplitude * np.cos(omega * time.get_value()) * np.exp(-0.05 * time.get_value())
))
```

### 3. Scene Variants

| Scene | Purpose |
|-------|---------|
| `TransitOfVenus` | Historical astronomical transit |
| `OrbitalTransit` | Exoplanet-style orbit with depth |
| `LoadingDots` | Classic loading animation |
| `WaveTransit` | Wave pulse propagation |
| `PendulumSwing` | Damped pendulum with trail |

## Key Patterns

### Pattern: Copy and Freeze
```python
copy = mobject.copy().clear_updaters()  # Snapshot current state
```

### Pattern: Continuous Time Updater
```python
time = ValueTracker(0)
time.add_updater(lambda m, dt: m.increment_value(dt))
```

## Run Commands

```bash
manimgl transit_animation.py TransitOfVenus -w
manimgl transit_animation.py LoadingDots -w
manimgl transit_animation.py PendulumSwing -w
```
