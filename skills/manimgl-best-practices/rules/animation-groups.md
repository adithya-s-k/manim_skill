# Animation Groups in ManimGL

Animation groups allow you to coordinate multiple animations, running them simultaneously, sequentially, or with staggered timing.

## AnimationGroup

Runs multiple animations together.

### Basic Usage

```python
from manimlib import *

class GroupExample(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        circle.shift(LEFT * 2)
        square.shift(RIGHT * 2)

        # Run both animations simultaneously
        self.play(AnimationGroup(
            ShowCreation(circle),
            ShowCreation(square)
        ))
        self.wait()
```

### Shorthand Syntax

```python
# Equivalent to AnimationGroup
self.play(
    ShowCreation(circle),
    ShowCreation(square)
)
```

## LaggedStart

Starts animations with a staggered delay.

### Basic LaggedStart

```python
class LaggedStartExample(Scene):
    def construct(self):
        circles = VGroup(*[
            Circle(radius=0.5).shift(i * RIGHT)
            for i in range(-3, 4)
        ])

        # Staggered creation
        self.play(LaggedStart(
            *[ShowCreation(c) for c in circles],
            lag_ratio=0.2,  # Delay ratio between animations
            run_time=3
        ))
        self.wait()
```

### lag_ratio Parameter

```python
# lag_ratio controls the delay
# 0 = all at once (like AnimationGroup)
# 1 = completely sequential (like Succession)
# 0.5 = overlapping animations

# Subtle overlap
self.play(LaggedStart(*animations, lag_ratio=0.1))

# More pronounced stagger
self.play(LaggedStart(*animations, lag_ratio=0.5))

# Nearly sequential
self.play(LaggedStart(*animations, lag_ratio=0.9))
```

## Succession

Runs animations one after another.

```python
class SuccessionExample(Scene):
    def construct(self):
        shapes = VGroup(
            Circle().shift(LEFT * 2),
            Square(),
            Triangle().shift(RIGHT * 2)
        )

        # One after another (no overlap)
        self.play(Succession(
            ShowCreation(shapes[0]),
            ShowCreation(shapes[1]),
            ShowCreation(shapes[2])
        ))
        self.wait()
```

### Succession vs Sequential play() Calls

```python
# Using Succession (all in one play call)
self.play(Succession(
    animation1,
    animation2,
    animation3
))

# Equivalent to separate play calls
self.play(animation1)
self.play(animation2)
self.play(animation3)
```

## Combining Animation Groups

### Nested Groups

```python
class NestedGroups(Scene):
    def construct(self):
        # Top row
        top = VGroup(*[Circle().shift(i*RIGHT) for i in range(-2, 3)])

        # Bottom row
        bottom = VGroup(*[Square().shift(i*RIGHT + 2*DOWN) for i in range(-2, 3)])

        # Stagger within each row, but rows appear simultaneously
        self.play(
            LaggedStart(*[ShowCreation(c) for c in top], lag_ratio=0.2),
            LaggedStart(*[ShowCreation(s) for s in bottom], lag_ratio=0.2),
        )
        self.wait()
```

### Sequential Groups

```python
# First group, then second group
self.play(Succession(
    LaggedStart(*[ShowCreation(t) for t in top], lag_ratio=0.2),
    LaggedStart(*[ShowCreation(b) for b in bottom], lag_ratio=0.2)
))
```

## LaggedStartMap

Applies an animation constructor to mobjects with lag.

```python
class LaggedStartMapExample(Scene):
    def construct(self):
        dots = VGroup(*[
            Dot().shift(i * RIGHT + j * UP)
            for i in range(-3, 4)
            for j in range(-2, 3)
        ])

        # Apply FadeIn to all dots with lag
        self.play(LaggedStartMap(
            FadeIn, dots,
            lag_ratio=0.05
        ))
        self.wait()
```

## Timing Control

### run_time for Groups

```python
# Total time for all animations
self.play(LaggedStart(
    *animations,
    lag_ratio=0.2,
    run_time=5  # Total duration
))

# Each animation's individual timing
self.play(LaggedStart(
    ShowCreation(circle, run_time=2),
    ShowCreation(square, run_time=1),
    lag_ratio=0.3
))
```

### rate_func with Groups

```python
# Apply rate function to entire group
self.play(
    LaggedStart(*animations, lag_ratio=0.2),
    rate_func=smooth
)

# Different rate functions for each
self.play(
    ShowCreation(circle, rate_func=linear),
    ShowCreation(square, rate_func=rush_into),
    ShowCreation(triangle, rate_func=rush_from)
)
```

## Practical Examples

### Text Appearance

```python
class TextReveal(Scene):
    def construct(self):
        title = Text("Animated Title", font_size=72)
        subtitle = Text("With smooth appearance", font_size=40)
        subtitle.next_to(title, DOWN)

        # Title letters appear one by one
        self.play(LaggedStart(
            *[FadeIn(char, shift=UP) for char in title],
            lag_ratio=0.05
        ))
        self.wait(0.3)

        # Subtitle fades in
        self.play(FadeIn(subtitle, shift=DOWN))
        self.wait()
```

### Grid Animation

```python
class GridAnimation(Scene):
    def construct(self):
        grid = VGroup(*[
            Square(side_length=0.8).shift([i, j, 0])
            for i in range(-3, 4)
            for j in range(-2, 3)
        ])

        # Ripple effect
        self.play(LaggedStart(
            *[ShowCreation(square) for square in grid],
            lag_ratio=0.02,
            run_time=4
        ))
        self.wait()
```

### Wave Effect

```python
class WaveEffect(Scene):
    def construct(self):
        dots = VGroup(*[
            Dot().shift(i * 0.5 * RIGHT)
            for i in range(-10, 11)
        ])

        # Wave up and down
        def wave_animation(dot, delay):
            return Succession(
                Wait(delay),
                dot.animate.shift(UP),
                dot.animate.shift(DOWN)
            )

        self.add(dots)
        self.play(*[
            wave_animation(dot, i * 0.1)
            for i, dot in enumerate(dots)
        ])
        self.wait()
```

### Cascade Effect

```python
class CascadeEffect(Scene):
    def construct(self):
        squares = VGroup(*[
            Square(side_length=1).shift(i * 1.5 * DOWN)
            for i in range(-2, 3)
        ])

        # Cascade from top to bottom
        self.play(LaggedStart(
            *[
                AnimationGroup(
                    square.animate.shift(RIGHT * 3),
                    square.animate.set_color(random_color())
                )
                for square in squares
            ],
            lag_ratio=0.3
        ))
        self.wait()
```

## Simultaneous Transformations

### Multiple Object Transformations

```python
class SimultaneousTransforms(Scene):
    def construct(self):
        shapes = VGroup(
            Circle().shift(LEFT * 3),
            Square().shift(LEFT),
            Triangle().shift(RIGHT),
            Star().shift(RIGHT * 3)
        )

        self.play(LaggedStart(
            *[ShowCreation(s) for s in shapes],
            lag_ratio=0.2
        ))
        self.wait()

        # Transform all simultaneously with different targets
        targets = [
            Square().shift(LEFT * 3),
            Circle().shift(LEFT),
            Star().shift(RIGHT),
            Triangle().shift(RIGHT * 3)
        ]

        self.play(*[
            Transform(s, t)
            for s, t in zip(shapes, targets)
        ])
        self.wait()
```

## Best Practices

1. **Use LaggedStart for visual rhythm**: Creates more dynamic animations
2. **lag_ratio tuning**:
   - 0.1-0.3 for subtle effects
   - 0.5 for balanced overlap
   - 0.8-1.0 for nearly sequential
3. **Nested groups**: Combine for complex choreography
4. **Total run_time**: Set on the group for consistent timing
5. **Don't overuse**: Too many lagged animations can be distracting

## Common Patterns

### Fade out everything

```python
# Fade out all objects with lag
self.play(LaggedStart(
    *[FadeOut(mob) for mob in self.mobjects],
    lag_ratio=0.1
))
```

### Build complex figure

```python
# Build parts sequentially
self.play(Succession(
    ShowCreation(axes),
    ShowCreation(graph),
    Write(labels),
    FadeIn(legend)
))
```

### Reveal diagram

```python
# Reveal components with rhythm
components = [background, main_shape, decorations, labels]
self.play(LaggedStart(
    *[FadeIn(c, scale=0.8) for c in components],
    lag_ratio=0.4
))
```

### Synchronized movement

```python
# Move multiple objects together
objects = VGroup(circle, square, triangle)
self.play(*[
    obj.animate.shift(RIGHT * 2)
    for obj in objects
])
```

## Full Example

```python
class ComprehensiveGrouping(Scene):
    def construct(self):
        # Title
        title = Text("Animation Groups", font_size=60)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Create grid of dots
        dots = VGroup(*[
            Dot(color=interpolate_color(BLUE, RED, i/20))
            .shift([
                (i % 7 - 3) * 0.8,
                (i // 7 - 1.5) * 0.8,
                0
            ])
            for i in range(21)
        ])

        # Lagged appearance
        self.play(LaggedStart(
            *[FadeIn(dot, scale=0.5) for dot in dots],
            lag_ratio=0.05,
            run_time=3
        ))
        self.wait()

        # Synchronized color change
        self.play(*[
            dot.animate.set_color(YELLOW)
            for dot in dots
        ])
        self.wait()

        # Cascade disappearance
        self.play(LaggedStart(
            *[FadeOut(dot, shift=DOWN) for dot in dots],
            lag_ratio=0.05,
            run_time=2
        ))

        # Clean up
        self.play(FadeOut(title))
        self.wait()
```

## Debugging Groups

### Print timing information

```python
# Check total duration
group = LaggedStart(*animations, lag_ratio=0.2)
print(f"Group duration: {group.get_run_time()}")

# Visualize timing
for i, anim in enumerate(animations):
    print(f"Animation {i}: starts at {i * 0.2 * group.get_run_time()}")
```

### Test lag_ratio values

```python
# Try different values to find the right feel
for lag in [0.1, 0.3, 0.5, 0.7]:
    self.play(LaggedStart(*animations, lag_ratio=lag))
    self.wait()
```
