---
name: timing
description: Rate functions, easing, run_time, and animation timing control
metadata:
  tags: timing, rate_func, easing, smooth, linear, run_time, imports
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

```python
self.play(
    circle.animate.shift(RIGHT),
    rate_func=smooth
)
```

## Imports: only some rate functions come from `from manim import *`

This is the most common mistake with rate functions, and it fails at **render time**, not
at import time — so it surfaces partway through a long render.

`manim/utils/rate_functions.py` declares an `__all__` with **17 names**. A star-import
respects `__all__`, so `from manim import *` gives you those 17 and nothing else. Every
`ease_*` function is defined in that module but is **absent from `__all__`**:

```python
from manim import *

self.play(square.animate.shift(RIGHT), rate_func=ease_out_sine)
# NameError: name 'ease_out_sine' is not defined
```

Import them explicitly from the module:

```python
from manim import *
from manim.utils.rate_functions import ease_in_sine, ease_out_sine, ease_out_back

self.play(square.animate.shift(RIGHT), rate_func=ease_out_sine)   # works
```

Or reach them through the module object, which `manim/__init__.py` does bind:

```python
from manim import *
from manim import rate_functions as rf

self.play(square.animate.shift(RIGHT), rate_func=rf.ease_out_sine)
```

Check what your installed version exports:

```bash
python -c "from manim.utils.rate_functions import __all__; print(__all__)"
```

### Available with a bare `from manim import *`

All 17 star-exported names:

```python
linear                      # constant speed
smooth                      # sigmoid ease-in-out; the default for most animations
smoothstep                  # 3t^2 - 2t^3; zero speed at both ends
smootherstep                # zero speed AND acceleration at both ends
smoothererstep              # zero speed, acceleration and jerk at both ends
rush_into                   # start slow, end fast
rush_from                   # start fast, end slow
slow_into                   # sqrt-shaped ease in
double_smooth               # two smooth halves back to back
there_and_back              # go there and return
there_and_back_with_pause   # go, hold, return
running_start               # pulls back slightly before moving off
not_quite_there             # approaches only part of the way
wiggle                      # oscillates
squish_rate_func            # compress another rate func into a sub-interval
lingering                   # reaches the target at t=0.8, then holds
exponential_decay           # fast approach, long tail
```

`squish_rate_func` is a combinator rather than a curve:

```python
# run `smooth` only during the middle half of the animation
self.play(mob.animate.shift(UP), rate_func=squish_rate_func(smooth, 0.25, 0.75))
```

### Require an explicit import (CSS-like easing)

None of these are star-exported. All 30 live in `manim.utils.rate_functions`:

```python
from manim.utils.rate_functions import (
    ease_in_sine,    ease_out_sine,    ease_in_out_sine,
    ease_in_quad,    ease_out_quad,    ease_in_out_quad,
    ease_in_cubic,   ease_out_cubic,   ease_in_out_cubic,
    ease_in_quart,   ease_out_quart,   ease_in_out_quart,
    ease_in_quint,   ease_out_quint,   ease_in_out_quint,
    ease_in_expo,    ease_out_expo,    ease_in_out_expo,
    ease_in_circ,    ease_out_circ,    ease_in_out_circ,
    ease_in_back,    ease_out_back,    ease_in_out_back,     # slight overshoot
    ease_in_elastic, ease_out_elastic, ease_in_out_elastic,  # springy
    ease_in_bounce,  ease_out_bounce,  ease_in_out_bounce,   # bouncy
)
```

## Visual Comparison

Uses only star-exported names, so no extra import is needed:

```python
from manim import *

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

Note `dot.animate(rate_func=..., run_time=...)` — the `.animate` builder is callable, which
is how one animation inside a `play` gets its own timing while the others keep the default.

## Combining run_time and rate_func

```python
from manim import *
from manim.utils.rate_functions import ease_out_bounce   # not star-exported

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

A rate function takes `t` in [0, 1] and returns progress in [0, 1]:

```python
def my_rate_func(t):
    return t ** 2      # quadratic ease in

self.play(circle.animate.shift(RIGHT), rate_func=my_rate_func)
```

Manim clamps its own rate functions with two decorators, worth copying if your function
can be called slightly outside [0, 1] — it can be, at animation boundaries:

```python
from manim.utils.rate_functions import unit_interval, zero

@unit_interval       # returns 0 for t < 0 and 1 for t > 1
def my_ease(t):
    return t ** 2

@zero                # returns 0 outside [0, 1] -- for there-and-back shapes
def my_pulse(t):
    return 1 - abs(2 * t - 1)
```

Neither decorator is star-exported either.

## wait() Timing

```python
self.wait()      # default, 1 second
self.wait(2)     # 2 seconds
self.wait(0.5)   # half a second
```

## Animation Speed Multiplier

`run_time` on an `AnimationGroup` is the total for the group, distributed among the
children according to `lag_ratio`:

```python
self.play(AnimationGroup(
    Create(circle),
    Create(square),
    lag_ratio=0.5
), run_time=3)  # total duration is 3 seconds
```

## Best Practices

1. **Import the ease functions explicitly** — `from manim import *` does not provide them,
   and the failure is a `NameError` partway through a render.
2. **Use `smooth` for most animations** — it is the default and looks natural.
3. **Use `linear` for constant motion** — mechanical or precise movement, and for camera
   moves that should not feel like they accelerate.
4. **Use `ease_out_back` or `ease_out_bounce` for arrivals** — a small overshoot gives a
   mobject weight. Reserve it for things that matter; on every element it is noise.
5. **Keep `run_time` between 0.5 and 3 seconds** — under about 0.4s reads as a flicker
   rather than a movement.
6. **Use `there_and_back` for emphasis** — it is what `Indicate` and `Wiggle` are built on.
7. **Match `rate_func` to content** — smooth for elegant, bouncy for playful, `linear` when
   the constant rate is itself the point.
