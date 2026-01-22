# ManimGL Frame (Camera) Control

## CameraFrame

In ManimGL, camera control is done through `self.camera.frame` (CameraFrame is a Mobject):

```python
frame = self.camera.frame

# Set euler angles for 3D orientation
frame.set_euler_angles(
    theta=-30 * DEGREES,
    phi=70 * DEGREES,
)
```

**Note:** In InteractiveScene, you can also use `self.frame` as a shortcut.

## CameraFrame Methods (from official docs)

The CameraFrame inherits standard Mobject methods plus these specific ones:

- `.to_default_state()` - Reset camera
- `.set_euler_angles(theta, phi, gamma)` - Set all angles
- `.set_theta(theta)` - Horizontal rotation
- `.set_phi(phi)` - Vertical rotation
- `.set_gamma(gamma)` - Roll
- `.increment_theta(dtheta)` - Add to theta
- `.increment_phi(dphi)` - Add to phi
- `.increment_gamma(dgamma)` - Add to gamma

Also inherits: `.shift()`, `.scale()`, `.move_to()`

```python
# Look down at 45 degrees, rotated 30 degrees
self.frame.reorient(45, -30, 0, ORIGIN, 8)

# Animate the reorientation
self.play(
    self.frame.animate.reorient(60, -45, 0, (1, 0, 0), 10),
    run_time=3
)
```

## Common Camera Operations

### Zoom

```python
# Zoom in (smaller height = closer)
self.play(self.frame.animate.set_height(4))

# Zoom out
self.play(self.frame.animate.set_height(12))
```

### Pan

```python
# Move camera center
self.play(self.frame.animate.move_to(RIGHT * 3))

# Shift camera
self.play(self.frame.animate.shift(UP * 2))
```

### Combined Movement

```python
self.play(
    self.frame.animate.reorient(50, -40, 0, (2, 1, 0), 6).set_anim_args(run_time=3)
)
```

## fix_in_frame()

Keep mobjects fixed in screen space during 3D camera movement:

```python
title = Text("My Title")
title.to_edge(UP)
title.fix_in_frame()  # Call on the mobject, not the scene!

self.add(title)

# Title stays fixed while camera moves
self.play(self.frame.animate.reorient(60, -45, 0))
```

**Key difference from ManimCE:** In ManimCE you call `self.add_fixed_in_frame_mobjects(title)`. In ManimGL you call `title.fix_in_frame()`.

## set_floor_plane()

Set the floor plane orientation for 3D scenes:

```python
self.set_floor_plane("xz")  # y is up, xz is floor
self.set_floor_plane("xy")  # z is up, xy is floor (default)
```

## Frame Animation Syntax

```python
# Chain with set_anim_args for run_time
self.play(
    self.frame.animate.reorient(45, -30, 0, ORIGIN, 8).set_anim_args(run_time=2)
)

# Multiple frame operations
self.play(
    self.frame.animate.shift(RIGHT * 2).set_height(6),
    run_time=1.5
)
```

## Background Rectangle

For scenes with 3D camera movement, add a background:

```python
background = FullScreenRectangle()
background.set_fill(BLACK, 1)
background.fix_in_frame()
self.add(background)
```

## Complete 3D Example

```python
class Camera3DDemo(InteractiveScene):
    def construct(self):
        # Background
        bg = FullScreenRectangle()
        bg.set_fill(GREY_E, 1)
        bg.fix_in_frame()
        self.add(bg)

        # Title fixed in frame
        title = Text("3D Demo")
        title.to_edge(UP)
        title.fix_in_frame()
        self.add(title)

        # 3D content
        cube = Cube(side_length=2)
        cube.set_color(BLUE)
        self.add(cube)

        # Animate camera
        self.play(
            self.frame.animate.reorient(60, -45, 0, ORIGIN, 8),
            run_time=3
        )

        # Rotate around
        self.play(
            self.frame.animate.reorient(60, 45, 0),
            run_time=4
        )
```
