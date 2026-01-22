# Spring-Mass System - Reference Guide

**Example file**: `examples/spring_mass_system.py`

## User Query Scenarios

This example addresses queries like:
- "Create a spring animation with oscillation"
- "Show damped harmonic motion"
- "Visualize physics simulation with a mass on a spring"
- "Animate a spring-mass system with real-time graph"
- "Compare different damping coefficients"

## Scene Thinking Process (3b1b Style)

### 1. Identify the Core Concept
**Damped Harmonic Motion**: A mass attached to a spring oscillates, with amplitude decreasing over time due to friction/damping. The equation is: `x'' = -kx - μv`

### 2. Visual Design Decisions

**Why a parametric helix for the spring?**
- Looks realistic with 3D coils
- Stretches naturally when mass moves
- Uses `ParametricCurve` for smooth rendering

**Why track position on a number line?**
- Gives quantitative feedback
- Shows exact displacement values
- Easy to understand motion direction

### 3. Technical Implementation

#### Creating a Self-Contained Physics Component
```python
class SpringMassSystem(VGroup):
    def __init__(self, x0=0, v0=0, k=3, mu=0.1, ...):
        # Store physics state
        self.k = k
        self.mu = mu
        self.velocity = v0

        # Add physics updater
        self.add_updater(lambda m, dt: m.time_step(dt))
```

**Key insight**: Encapsulate physics + visuals in one VGroup subclass. This makes it reusable and keeps animation code clean.

#### Physics Integration (Euler Method)
```python
def time_step(self, delta_t, dt_size=0.01):
    state = [self.get_x(), self.velocity]
    for _ in range(sub_steps):
        x, v = state
        acceleration = -self.k * x - self.mu * v
        state[0] += v * true_dt
        state[1] += acceleration * true_dt
```

#### Dynamic Velocity/Force Vectors
```python
def get_velocity_vector(self, scale_factor=0.5, color=GREEN):
    vector = Vector(RIGHT, fill_color=color)
    vector.add_updater(lambda m: m.put_start_and_end_on(
        self.mass.get_center(),
        self.mass.get_center() + scale_factor * self.velocity * RIGHT
    ))
    return vector
```

### 4. Scene Variants

| Scene | Purpose |
|-------|---------|
| `SpringMassDemo` | Basic oscillation with velocity/force vectors |
| `SpringWithGraph` | Real-time x(t) graph using TracedPath |
| `MultipleSprings` | Compare different damping values |

## Key Patterns Demonstrated

### Pattern: Pausable Physics
```python
def pause(self):
    self._is_running = False

def unpause(self):
    self._is_running = True
```

### Pattern: TracedPath for Graphs
```python
tracking_point = Point()
tracking_point.add_updater(lambda p: p.move_to(
    axes.c2p(time_tracker.get_value(), spring.get_x())
))
position_graph = TracedPath(tracking_point.get_center, stroke_color=BLUE)
```

## Run Commands

```bash
# Basic demo
manimgl spring_mass_system.py SpringMassDemo -w

# With real-time graph
manimgl spring_mass_system.py SpringWithGraph -w

# Compare damping
manimgl spring_mass_system.py MultipleSprings -w
```
