---
name: timing
description: Rate functions, easing, run_time, and animation timing control
metadata:
  tags: timing, rate_func, easing, smooth, linear, run_time
---

# Animation Timing

Control the speed and feel of animations with timing parameters.

## run_time

Controls how long an animation takes in seconds.

```python
from manim import *

class RunTimeExample(Scene):
    def construct(self):
        circle = Circle()

        # Default (1 second)
        self.play(Create(circle))

        # Longer animation
        self.play(circle.animate.shift(RIGHT), run_time=3)

        # Quick animation
        self.play(circle.animate.set_color(RED), run_time=0.5)
```

## Rate Functions

Rate functions control how the animation progresses over time (easing).

### Using Rate Functions

```python
self.play(
    circle.animate.shift(RIGHT),
    rate_func=smooth
)
```

### Common Rate Functions

```python
# Smooth start and end (default for most animations)
smooth

# Constant speed
linear

# Start slow, end fast
rush_into

# Start fast, end slow
rush_from

# Go there and back
there_and_back

# Go there and back with pause
there_and_back_with_pause

# Double smooth (extra smooth)
double_smooth

# Stay put (useful for delays in AnimationGroup)
lingering
```

### Ease Functions (CSS-like)

```python
# Ease in (start slow)
ease_in_sine
ease_in_quad
ease_in_cubic
ease_in_expo
ease_in_circ
ease_in_back    # Slight overshoot at start

# Ease out (end slow)
ease_out_sine
ease_out_quad
ease_out_cubic
ease_out_expo
ease_out_circ
ease_out_back   # Slight overshoot at end
ease_out_bounce # Bouncy ending

# Ease in-out (slow at both ends)
ease_in_out_sine
ease_in_out_quad
ease_in_out_cubic
ease_in_out_expo
ease_in_out_circ
ease_in_out_back
```

## Visual Comparison

```python
class RateFuncComparison(Scene):
    def construct(self):
        funcs = [linear, smooth, rush_into, rush_from, there_and_back]
        names = ["linear", "smooth", "rush_into", "rush_from", "there_and_back"]

        dots = VGroup()
        labels = VGroup()

        for i, (func, name) in enumerate(zip(funcs, names)):
            dot = Dot().shift(LEFT * 4 + DOWN * i)
            label = Text(name, font_size=24).next_to(dot, LEFT)
            dots.add(dot)
            labels.add(label)

        self.add(dots, labels)

        self.play(*[
            dot.animate(rate_func=func).shift(RIGHT * 8)
            for dot, func in zip(dots, funcs)
        ], run_time=3)
```

## Combining run_time and rate_func

```python
self.play(
    square.animate.shift(RIGHT * 3),
    run_time=2,
    rate_func=ease_out_bounce
)
```

## there_and_back

Animation goes forward then reverses.

```python
class ThereAndBackExample(Scene):
    def construct(self):
        square = Square()
        self.add(square)

        # Moves right then back to start
        self.play(
            square.animate.shift(RIGHT * 2),
            rate_func=there_and_back,
            run_time=2
        )
```

## Custom Rate Functions

Create your own rate function (takes t from 0 to 1, returns progress 0 to 1):

```python
def my_rate_func(t):
    # Quadratic ease
    return t ** 2

self.play(
    circle.animate.shift(RIGHT),
    rate_func=my_rate_func
)
```

## wait() Timing

```python
# Wait for default time (1 second)
self.wait()

# Wait for specific duration
self.wait(2)    # 2 seconds
self.wait(0.5)  # Half second
```

## Animation Speed Multiplier

Using `run_time` on AnimationGroup affects all children:

```python
self.play(AnimationGroup(
    Create(circle),
    Create(square),
    lag_ratio=0.5
), run_time=3)  # Total duration is 3 seconds
```

## Best Practices

1. **Use smooth for most animations** - Looks natural
2. **Use linear for constant motion** - Mechanical/precise movement
3. **Use ease_out_bounce for playful effects** - Attention-grabbing
4. **Keep run_time between 0.5-3 seconds** - Maintain viewer attention
5. **Use there_and_back for emphasis** - Show something temporarily
6. **Match rate_func to content** - Smooth for elegant, bouncy for fun
