---
name: animations
description: Animation classes, .animate, run_time, rate functions and groups in ManimGX
metadata:
  tags: animation, animate, play, run_time, rate_func, laggedstart, succession, transform
---

# Animations in ManimGX

## `.animate`

`mob.animate.method(args)` animates a method call over the play's duration. Its calls apply
when the animation starts.

```python
import manimgx as m

class Move(m.Scene):
    def construct(self):
        square = m.Square()
        self.add(square)
        self.play(square.animate.shift(m.RIGHT * 2).scale(2))
        self.play(square.animate.set_color(m.RED))
```

- In a `Succession`, each `.animate` starts where the previous one ended.
- To animate a method of your own class, pass a function: `box.animate(lambda b: b.grow(2))`.

## Common animations

```python
m.Create(mob)                  # draw along its path
m.Write(mob)                   # write text / equations
m.FadeIn(mob, shift=m.UP)      # fade in, optionally moving
m.FadeOut(mob)
m.GrowFromCenter(mob)
m.Transform(a, b)              # a morphs into b; a stays in the scene
m.ReplacementTransform(a, b)   # a is replaced by b
m.TransformMatchingTex(eq1, eq2)
m.Rotate(mob, m.PI / 2)
m.Indicate(mob)                # emphasis
m.Circumscribe(mob)            # draw attention with a frame
```

Do not `Transform` between `Text` and `MathTex`; use `ReplacementTransform` between the same
kind, or `FadeOut` + `FadeIn`.

## Timing

```python
self.play(m.Create(circle), run_time=2)          # duration in seconds
self.play(circle.animate.shift(m.RIGHT), rate_func=m.smooth)
self.play(square.animate.shift(m.RIGHT * 3), run_time=2, rate_func=m.ease_out_bounce)
```

- `smooth` (default), `linear`, `rush_into`, `rush_from`, `there_and_back`,
  `ease_in_*`, `ease_out_*`, `ease_in_out_*`.
- Keep most animations between 0.5 and 3 seconds.

## Groups and sequences

```python
self.play(m.AnimationGroup(m.Create(a), m.Create(b), lag_ratio=0.5))
self.play(m.LaggedStart(m.Write(line1), m.Write(line2), lag_ratio=0.3))
self.play(m.Succession(m.Create(a), m.Transform(a, b)))
```

- `AnimationGroup` runs the animations together (with `lag_ratio`).
- `LaggedStart` starts each a little after the previous.
- `Succession` runs them one after another.
