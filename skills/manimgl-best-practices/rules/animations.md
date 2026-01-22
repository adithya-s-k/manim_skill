# ManimGL Animations

## Animation System Overview

ManimGL's animation system is built around the `Animation` base class. Specialized subclasses handle creation, transformation, and indication effects.

## Playing Animations

```python
# Single animation
self.play(ShowCreation(circle))

# Multiple animations simultaneously
self.play(
    ShowCreation(circle),
    Write(text),
)

# With run_time
self.play(ShowCreation(circle), run_time=2)

# With rate function
self.play(ShowCreation(circle), rate_func=smooth)
```

## Creation Animations

| Animation | Description |
|-----------|-------------|
| `ShowCreation` | Draw a VMobject's path (NOT `Create` like in ManimCE) |
| `Write` | Write text or LaTeX |
| `DrawBorderThenFill` | Draw outline then fill |
| `FadeIn` | Fade in with optional direction |
| `FadeOut` | Fade out with optional direction |
| `GrowFromCenter` | Scale up from center |
| `GrowFromPoint` | Scale up from a point |
| `GrowArrow` | Specialized for arrows |

```python
# ShowCreation for paths
self.play(ShowCreation(circle))

# Write for text
self.play(Write(Tex(R"\pi")))

# FadeIn with direction
self.play(FadeIn(square, shift=UP))
```

## Transform Animations

| Animation | Description |
|-----------|-------------|
| `Transform` | Morph one mobject into another (modifies original) |
| `ReplacementTransform` | Replace source with target |
| `TransformMatchingShapes` | Match similar shapes |
| `TransformMatchingTex` | Match LaTeX parts |
| `FadeTransform` | Fade while transforming |
| `MoveToTarget` | Move to mobject's `.target` |

```python
# Transform (modifies circle, becomes square)
self.play(Transform(circle, square))

# ReplacementTransform (removes circle, adds square)
self.play(ReplacementTransform(circle, square))

# Using .target
circle.generate_target()
circle.target.shift(RIGHT * 2)
circle.target.set_color(RED)
self.play(MoveToTarget(circle))
```

## Indication Animations

| Animation | Description |
|-----------|-------------|
| `Indicate` | Flash/pulse to draw attention |
| `ShowPassingFlash` | Flash along a path |
| `Flash` | Burst of light |
| `Circumscribe` | Draw circle/rect around |
| `Wiggle` | Wiggle the mobject |
| `FlashAround` | Flash effect around object |

```python
self.play(Indicate(important_text))
self.play(FlashAround(equation, run_time=2))
```

## Movement Animations

```python
# Using .animate syntax
self.play(circle.animate.shift(RIGHT * 2))
self.play(circle.animate.scale(2).set_color(RED))

# Rotate
self.play(Rotate(square, PI/2))
self.play(Rotate(square, 90 * DEGREES))  # Same thing

# MoveAlongPath
path = Line(LEFT, RIGHT)
self.play(MoveAlongPath(dot, path))
```

## LaggedStart and Groups

```python
# Staggered animations
self.play(LaggedStart(
    *[ShowCreation(mob) for mob in mobjects],
    lag_ratio=0.2
))

# AnimationGroup for simultaneous
self.play(AnimationGroup(
    ShowCreation(circle),
    Write(text),
    lag_ratio=0  # Simultaneous
))

# Succession for sequential
self.play(Succession(
    ShowCreation(circle),
    Write(text),
))
```

## Animation Parameters

Common parameters for all animations:

| Parameter | Description |
|-----------|-------------|
| `run_time` | Duration in seconds |
| `rate_func` | Easing function (smooth, linear, etc.) |
| `lag_ratio` | Stagger ratio for grouped animations |
| `remover` | Remove mobject after animation |
| `introducer` | Add mobject at animation start |

```python
self.play(
    ShowCreation(circle),
    run_time=3,
    rate_func=there_and_back,
)
```

## Rate Functions

Common rate functions:
- `smooth` - Default smooth easing
- `linear` - Constant speed
- `rush_into` - Fast start, slow end
- `rush_from` - Slow start, fast end
- `there_and_back` - Go and return
- `double_smooth` - Extra smooth

## Waiting

```python
self.wait()       # Default pause
self.wait(2)      # 2 second pause
self.wait(0.5)    # Half second
```
