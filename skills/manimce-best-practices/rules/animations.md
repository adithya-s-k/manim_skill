---
name: animations
description: Animation classes, playing animations, and animation timing in Manim
metadata:
  tags: animation, play, run_time, rate_func, animate
---

# Animations in Manim

Animations interpolate mobjects between states over time. They are played using `self.play()`.

## The .animate Syntax

The most common way to animate is using the `.animate` property:

```python
# Move a square to the right
self.play(square.animate.shift(RIGHT))

# Scale up
self.play(circle.animate.scale(2))

# Change color
self.play(text.animate.set_color(RED))

# Chain multiple changes
self.play(square.animate.shift(RIGHT).rotate(PI/4).set_color(BLUE))
```

## Animation Parameters

### run_time
Controls animation duration in seconds (default: 1).

```python
self.play(Create(circle), run_time=2)  # 2 second animation
self.play(Create(circle), run_time=0.5)  # Half second
```

### rate_func
Controls the animation's timing curve (easing).

```python
from manim import smooth, linear, there_and_back

self.play(square.animate.shift(RIGHT), rate_func=smooth)
self.play(square.animate.shift(RIGHT), rate_func=linear)
self.play(square.animate.shift(RIGHT), rate_func=there_and_back)
```

## Playing Multiple Animations

### Simultaneously

```python
# All play at the same time
self.play(
    Create(circle),
    FadeIn(square),
    Write(text)
)
```

### Sequentially

```python
# One after another
self.play(Create(circle))
self.play(FadeIn(square))
self.play(Write(text))

# Or use Succession
self.play(Succession(
    Create(circle),
    FadeIn(square),
    Write(text)
))
```

## Common Animation Classes

### Creation Animations
```python
Create(mobject)           # Draw the mobject progressively
Write(text)               # Write text/equations
FadeIn(mobject)           # Fade in from transparent
DrawBorderThenFill(mob)   # Draw outline, then fill
GrowFromCenter(mobject)   # Grow from center point
```

### Removal Animations
```python
FadeOut(mobject)          # Fade to transparent
Uncreate(mobject)         # Reverse of Create
ShrinkToCenter(mobject)   # Shrink to center and disappear
```

### Transform Animations
```python
Transform(mob1, mob2)              # Morph mob1 into mob2
ReplacementTransform(mob1, mob2)   # Replace mob1 with mob2
TransformFromCopy(mob1, mob2)      # Keep mob1, create mob2
```

### Movement Animations
```python
MoveToTarget(mobject)     # Move to preset target
Rotate(mobject, angle)    # Rotate by angle
Circumscribe(mobject)     # Draw attention with circle
```

## Animation vs Instant Changes

```python
# Animated change (visible transition)
self.play(circle.animate.set_color(RED))

# Instant change (no animation)
circle.set_color(RED)
self.add(circle)
```

## Best Practices

1. **Use .animate for simple transformations** - Cleaner than explicit Animation classes
2. **Keep run_time reasonable** - 0.5-2 seconds for most animations
3. **Use rate_func for polish** - `smooth` is usually better than `linear`
4. **Group related animations** - Play simultaneously when conceptually related
