---
name: updaters
description: Updaters, ValueTracker, and dynamic animations
metadata:
  tags: updater, valuetracker, dynamic, always, add_updater
---

# Updaters and Dynamic Animations

Updaters allow mobjects to automatically update based on other values or mobjects.

## Basic Updaters

Add a function that runs every frame.

```python
from manim import *

class UpdaterExample(Scene):
    def construct(self):
        dot = Dot()
        label = Text("Follow me").next_to(dot, UP)

        # Label always follows the dot
        label.add_updater(lambda m: m.next_to(dot, UP))

        self.add(dot, label)
        self.play(dot.animate.shift(RIGHT * 3), run_time=2)
        self.play(dot.animate.shift(DOWN * 2), run_time=2)
```

## Updater Syntax

```python
# Lambda function
mobject.add_updater(lambda m: m.move_to(target.get_center()))

# Named function
def follow_target(mob):
    mob.next_to(target, RIGHT)

mobject.add_updater(follow_target)

# With dt (delta time) parameter
def time_based_update(mob, dt):
    mob.rotate(dt * PI)  # Rotate based on time elapsed

mobject.add_updater(time_based_update)
```

## ValueTracker

A mobject that holds a numeric value. Perfect for animating parameters.

```python
class ValueTrackerExample(Scene):
    def construct(self):
        # Create tracker
        tracker = ValueTracker(0)

        # Create number display
        number = DecimalNumber(0, num_decimal_places=2)
        number.add_updater(lambda m: m.set_value(tracker.get_value()))

        # Create circle that grows with tracker
        circle = Circle()
        circle.add_updater(lambda m: m.set_width(tracker.get_value()))

        self.add(number, circle)

        # Animate the tracker
        self.play(tracker.animate.set_value(4), run_time=3)
        self.play(tracker.animate.set_value(1), run_time=2)
```

### ValueTracker Operations

```python
tracker = ValueTracker(5)

# Get and set value
current = tracker.get_value()
tracker.set_value(10)

# Increment
tracker.increment_value(2.5)

# Arithmetic operators (direct manipulation, no animation)
tracker += 1
tracker -= 2
tracker *= 3
tracker /= 2

# Animate changes
self.play(tracker.animate.set_value(100))
self.play(tracker.animate.increment_value(-50))
```

## DecimalNumber with ValueTracker

Display a changing number:

```python
class NumberDisplay(Scene):
    def construct(self):
        tracker = ValueTracker(0)

        number = DecimalNumber(
            0,
            num_decimal_places=2,
            include_sign=True,
            font_size=72
        )
        number.add_updater(lambda m: m.set_value(tracker.get_value()))
        number.add_updater(lambda m: m.move_to(ORIGIN))

        self.add(number)
        self.play(tracker.animate.set_value(100), run_time=3)
```

## always_redraw

Recreate a mobject every frame based on current values.

```python
class AlwaysRedrawExample(Scene):
    def construct(self):
        tracker = ValueTracker(1)

        # Line that always connects two points based on tracker
        line = always_redraw(
            lambda: Line(
                LEFT * 2,
                RIGHT * 2 * tracker.get_value()
            )
        )

        self.add(line)
        self.play(tracker.animate.set_value(2), run_time=2)
        self.play(tracker.animate.set_value(0.5), run_time=2)
```

## Common Updater Patterns

### Following Another Mobject
```python
follower.add_updater(lambda m: m.move_to(leader.get_center()))
follower.add_updater(lambda m: m.next_to(leader, RIGHT))
```

### Pointing at Another Mobject
```python
arrow = Arrow(ORIGIN, RIGHT)
arrow.add_updater(lambda m: m.put_start_and_end_on(
    start.get_center(),
    end.get_center()
))
```

### Rotating Continuously
```python
mobject.add_updater(lambda m, dt: m.rotate(dt * PI))
```

### Matching Properties
```python
# Match color
follower.add_updater(lambda m: m.set_color(leader.get_color()))

# Match position with offset
follower.add_updater(lambda m: m.move_to(leader.get_center() + UP))
```

## Removing Updaters

```python
# Remove specific updater
mobject.remove_updater(updater_function)

# Remove all updaters
mobject.clear_updaters()

# Suspend temporarily
mobject.suspend_updating()
mobject.resume_updating()
```

## Updaters with Animations

Updaters continue running during animations:

```python
class UpdaterDuringAnimation(Scene):
    def construct(self):
        dot = Dot()
        trail = TracedPath(dot.get_center, stroke_color=YELLOW)

        self.add(dot, trail)
        self.play(dot.animate.shift(RIGHT * 3 + UP * 2), run_time=3)
```

## TracedPath

Built-in updater for drawing paths:

```python
class TracedPathExample(Scene):
    def construct(self):
        dot = Dot()
        path = TracedPath(dot.get_center, stroke_width=2, stroke_color=BLUE)

        self.add(dot, path)
        self.play(
            dot.animate.shift(RIGHT * 2),
            dot.animate.shift(UP * 2),
            run_time=3
        )
```

## Best Practices

1. **Use ValueTracker for animated parameters** - Clean and controllable
2. **Use always_redraw for complex shapes** - When updaters get complicated
3. **Clear updaters when done** - Prevent performance issues
4. **Keep updater functions simple** - Complex logic can slow rendering
5. **Use dt for time-based animations** - Frame-rate independent
