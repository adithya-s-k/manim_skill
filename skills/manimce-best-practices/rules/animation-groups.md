---
name: animation-groups
description: AnimationGroup, LaggedStart, Succession for complex animation sequences
metadata:
  tags: animationgroup, laggedstart, succession, lag_ratio, sequence
---

# Animation Groups

Control how multiple animations play together.

## AnimationGroup

Play multiple animations with controlled timing.

```python
from manim import *

class AnimationGroupExample(Scene):
    def construct(self):
        circles = VGroup(*[Circle() for _ in range(5)]).arrange(RIGHT)

        # All animations play simultaneously (lag_ratio=0)
        self.play(AnimationGroup(
            *[Create(c) for c in circles],
            lag_ratio=0
        ))
```

### lag_ratio Parameter

Controls the delay between animation starts:
- `lag_ratio=0`: All start simultaneously
- `lag_ratio=0.5`: Each starts when previous is 50% complete
- `lag_ratio=1`: Each starts when previous finishes (sequential)

```python
class LagRatioDemo(Scene):
    def construct(self):
        squares = VGroup(*[Square() for _ in range(4)]).arrange(RIGHT)

        # Staggered start - each begins when previous is 25% done
        self.play(AnimationGroup(
            *[FadeIn(s) for s in squares],
            lag_ratio=0.25,
            run_time=2
        ))
```

## LaggedStart

Convenience class with default `lag_ratio=0.05` (5% overlap).

```python
class LaggedStartExample(Scene):
    def construct(self):
        dots = VGroup(*[Dot() for _ in range(10)]).arrange(RIGHT)

        # Rapid staggered animation
        self.play(LaggedStart(
            *[GrowFromCenter(d) for d in dots],
            lag_ratio=0.1
        ))
```

### Common LaggedStart Patterns

```python
# Staggered fade in
self.play(LaggedStart(*[FadeIn(m) for m in mobjects], lag_ratio=0.2))

# Wave effect
self.play(LaggedStart(
    *[m.animate.shift(UP * 0.5) for m in mobjects],
    lag_ratio=0.1
))

# Staggered color change
self.play(LaggedStart(
    *[m.animate.set_color(RED) for m in mobjects],
    lag_ratio=0.15
))
```

## Succession

Play animations one after another (equivalent to `lag_ratio=1`).

```python
class SuccessionExample(Scene):
    def construct(self):
        circle = Circle().shift(LEFT * 2)
        square = Square()
        triangle = Triangle().shift(RIGHT * 2)

        # Animations play in sequence
        self.play(Succession(
            Create(circle),
            Create(square),
            Create(triangle)
        ))
```

### Succession vs Multiple play() Calls

```python
# These are equivalent:

# Using Succession
self.play(Succession(
    Create(circle),
    Create(square)
))

# Using separate play calls
self.play(Create(circle))
self.play(Create(square))
```

Succession is useful when you want to treat sequential animations as a single unit.

## Combining Group Types

```python
class CombinedExample(Scene):
    def construct(self):
        group1 = VGroup(*[Circle() for _ in range(3)]).arrange(RIGHT).shift(UP)
        group2 = VGroup(*[Square() for _ in range(3)]).arrange(RIGHT).shift(DOWN)

        # First group appears with stagger, then second group
        self.play(Succession(
            LaggedStart(*[Create(c) for c in group1], lag_ratio=0.2),
            LaggedStart(*[Create(s) for s in group2], lag_ratio=0.2)
        ))
```

## LaggedStartMap

Apply an animation to all submobjects of a mobject with staggered timing.

```python
class LaggedStartMapExample(Scene):
    def construct(self):
        dots = VGroup(*[Dot(radius=0.16) for _ in range(35)]).arrange_in_grid(rows=5, cols=7)

        # Apply FadeIn to all dots with stagger
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.1))
        self.wait(0.5)

        # Change color with stagger using LaggedStart
        self.play(LaggedStart(
            *[dot.animate.set_color(YELLOW) for dot in dots],
            lag_ratio=0.05
        ))
```

LaggedStartMap is cleaner for applying the same animation to each submobject. For property changes, use LaggedStart with `.animate`.

## AnimationGroup with run_time

The total `run_time` is distributed among animations based on `lag_ratio`.

```python
self.play(AnimationGroup(
    *[Create(c) for c in circles],
    lag_ratio=0.5,
    run_time=4  # Total duration is 4 seconds
))
```

## Practical Examples

### Text Appearing Word by Word

```python
class WordByWord(Scene):
    def construct(self):
        words = VGroup(
            Text("Hello"),
            Text("World"),
            Text("!")
        ).arrange(RIGHT)

        self.play(LaggedStart(
            *[Write(w) for w in words],
            lag_ratio=0.5
        ))
```

### Grid Animation

```python
class GridAnimation(Scene):
    def construct(self):
        grid = VGroup(*[
            Square().scale(0.3)
            for _ in range(25)
        ]).arrange_in_grid(5, 5)

        # Diagonal wave effect
        self.play(LaggedStart(
            *[GrowFromCenter(s) for s in grid],
            lag_ratio=0.05
        ))
```

## Best Practices

1. **Use LaggedStart for visual polish** - Staggered animations look more dynamic
2. **Keep lag_ratio small (0.05-0.2)** - Too high feels slow
3. **Use Succession for distinct steps** - When animations are conceptually separate
4. **Adjust run_time with lag_ratio** - More items may need longer total time
