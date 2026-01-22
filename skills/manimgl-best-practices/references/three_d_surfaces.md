# 3D Surfaces - Reference Guide

**Example file**: `examples/three_d_surfaces.py`

## User Query Scenarios

This example addresses queries like:
- "Create a 3D surface visualization"
- "Show a parametric surface"
- "Animate camera rotation around object"
- "Create a torus/sphere/cone"
- "Show saddle surface"

## Scene Thinking Process (3b1b Style)

### 1. Core Concept
**Parametric Surfaces**: Define surfaces as functions (u,v) → (x,y,z). Camera movement reveals 3D structure.

### 2. Technical Implementation

#### Basic Parametric Surface
```python
surface = ParametricSurface(
    lambda u, v: [u, v, np.sin(u) * np.cos(v)],
    u_range=(-3, 3),
    v_range=(-3, 3),
    resolution=(30, 30),
)
surface.set_color(BLUE)
surface.set_opacity(0.8)
```

#### Camera Setup and Movement
```python
frame = self.frame
frame.reorient(-30, 70, 0)  # phi, theta, gamma
frame.set_height(10)

# Animate camera
self.play(frame.animate.reorient(30, 60, 0), run_time=3)
```

#### Sphere with Latitude/Longitude Lines
```python
# Latitude lines
for phi in np.linspace(-PI/2 + 0.3, PI/2 - 0.3, 6):
    line = ParametricCurve(
        lambda t: radius * np.array([
            np.cos(t) * np.cos(phi),
            np.sin(t) * np.cos(phi),
            np.sin(phi)
        ]),
        t_range=(0, TAU),
    )
```

#### Torus Parameterization
```python
R, r = 2, 0.7  # Major and minor radius
torus = ParametricSurface(
    lambda u, v: [
        (R + r * np.cos(v)) * np.cos(u),
        (R + r * np.cos(v)) * np.sin(u),
        r * np.sin(v)
    ],
    u_range=(0, TAU),
    v_range=(0, TAU),
)
```

### 3. Scene Variants

| Scene | Purpose |
|-------|---------|
| `ParametricSurface3D` | z = sin(x)cos(y) with camera orbit |
| `SphereSurface` | Sphere with grid lines, rotating |
| `ConeUnfolding` | 3D cone visualization |
| `SaddleSurface` | z = x² - y² with cross-sections |
| `TorusSurface` | Donut shape with rotation |

## Key Patterns

### Pattern: ThreeDAxes
```python
axes = ThreeDAxes(
    x_range=(-3, 3, 1),
    y_range=(-3, 3, 1),
    z_range=(-2, 2, 1),
)
```

### Pattern: Rotating Objects
```python
self.play(
    Rotate(surface, TAU, axis=UP, run_time=6, rate_func=linear),
)
```

### Pattern: Frame Reorientation
```python
# reorient(phi, theta, gamma, center, height)
frame.reorient(-30, 70, 0)  # Just angles
frame.animate.reorient(60, 60, 0)  # Animated
```

## Run Commands

```bash
manimgl three_d_surfaces.py ParametricSurface3D -w
manimgl three_d_surfaces.py SphereSurface -w
manimgl three_d_surfaces.py TorusSurface -w
manimgl three_d_surfaces.py SaddleSurface -w
```
