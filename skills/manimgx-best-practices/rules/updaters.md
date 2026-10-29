---
name: updaters
description: ValueTracker, always_redraw, TracedPath and dt updaters in ManimGX
metadata:
  tags: updater, valuetracker, always_redraw, tracedpath, dt, dynamic
---

# Updaters in ManimGX

Updaters run every frame. Each receives the exact time since its last call; a `dt`-taking
updater runs on its own clock, so a simulation is identical at every frame rate. **Derive
state from time or other mobjects — do not count frames.**

## Basic updater

```python
import manimgx as m

class Follow(m.Scene):
    def construct(self):
        dot = m.Dot().shift(m.LEFT * 2)
        label = m.Text("me").next_to(dot, m.UP)
        label.add_updater(lambda mob: mob.next_to(dot, m.UP))
        self.add(dot, label)
        self.play(dot.animate.shift(m.RIGHT * 4), run_time=2)
```

## ValueTracker

```python
import manimgx as m

class Tracker(m.Scene):
    def construct(self):
        tracker = m.ValueTracker(0)
        number = m.DecimalNumber(0, num_decimal_places=2)
        number.add_updater(lambda mob: mob.set_value(tracker.get_value()))
        circle = m.Circle()
        circle.add_updater(lambda mob: mob.set(width=tracker.get_value()))
        self.add(number, circle)
        self.play(tracker.animate.set_value(4), run_time=3)
```

- `tracker.get_value()`, `tracker.set_value(x)`, `tracker.increment_value(dx)`.
- Animate with `tracker.animate.set_value(...)`.

## always_redraw

```python
line = m.always_redraw(lambda: m.Line(dot1.get_center(), dot2.get_center()))
```

Rebuilds the mobject every frame from current state.

## TracedPath

```python
path = m.TracedPath(dot.get_center, stroke_width=2, stroke_color=m.BLUE)
self.add(dot, path)
self.play(dot.animate.shift(m.RIGHT * 2 + m.UP * 2), run_time=3)
```

## dt updaters

```python
def spin(mob, dt):
    mob.rotate(dt * m.PI)

wheel.add_updater(spin)
```

The `dt` clock is frame-rate independent: the same simulation at 30 and 60 fps.

## Removing updaters

```python
mob.remove_updater(fn)
mob.clear_updaters()
```
