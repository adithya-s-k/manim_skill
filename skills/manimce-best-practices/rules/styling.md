---
name: styling
description: Fill, stroke, opacity and visual styling of mobjects
metadata:
  tags: fill, stroke, opacity, style, width, appearance
---

# Styling Mobjects

Control the visual appearance of mobjects with fill, stroke, and opacity settings.

## Fill Properties

Fill controls the interior of shapes.

```python
from manim import *

class FillExample(Scene):
    def construct(self):
        # Set fill on creation
        circle = Circle(fill_color=BLUE, fill_opacity=0.8)

        # Set fill after creation
        square = Square()
        square.set_fill(RED, opacity=0.5)

        self.add(circle, square)
```

### Fill Methods
```python
mobject.set_fill(color=RED)                    # Color only
mobject.set_fill(RED, opacity=0.5)             # Color and opacity
mobject.set_fill(opacity=0.5)                  # Opacity only
mobject.set_fill_color(RED)                    # Color only (alternative)
mobject.set_fill_opacity(0.5)                  # Opacity only (alternative)
```

## Stroke Properties

Stroke controls the outline/border of shapes.

```python
class StrokeExample(Scene):
    def construct(self):
        # Set stroke on creation
        circle = Circle(stroke_color=BLUE, stroke_width=4)

        # Set stroke after creation
        square = Square()
        square.set_stroke(RED, width=8)

        self.add(circle, square)
```

### Stroke Methods
```python
mobject.set_stroke(color=RED)                  # Color only
mobject.set_stroke(RED, width=4)               # Color and width
mobject.set_stroke(width=4)                    # Width only
mobject.set_stroke(opacity=0.5)                # Opacity only
mobject.set_stroke_color(RED)                  # Color only (alternative)
mobject.set_stroke_width(4)                    # Width only (alternative)
mobject.set_stroke_opacity(0.5)                # Opacity only (alternative)
```

### Stroke Width Reference
```python
# Common stroke widths
DEFAULT_STROKE_WIDTH = 4
thin = 1
normal = 4
thick = 8
very_thick = 12
```

## Combined Styling

```python
class CombinedStyling(Scene):
    def construct(self):
        square = Square()
        square.set_fill(BLUE, opacity=0.5)
        square.set_stroke(YELLOW, width=6)
        self.add(square)
```

### Method Chaining
```python
square = Square().set_fill(RED, 0.5).set_stroke(WHITE, 4)
```

## The set_style Method

Set multiple style properties at once:

```python
square = Square()
square.set_style(
    fill_color=BLUE,
    fill_opacity=0.5,
    stroke_color=WHITE,
    stroke_width=4,
    stroke_opacity=1
)
```

## Opacity

Control transparency of mobjects:

```python
# Overall opacity
mobject.set_opacity(0.5)  # Affects both fill and stroke

# Separate opacities
mobject.set_fill_opacity(0.8)
mobject.set_stroke_opacity(0.3)

# Fade effect
mobject.fade(0.5)  # 0.5 = 50% faded (opposite of opacity)
```

## Background Rectangle

Add a background behind text or other mobjects:

```python
class BackgroundExample(Scene):
    def construct(self):
        text = Text("Important!")
        bg = BackgroundRectangle(text, fill_opacity=0.8, buff=0.1)
        group = VGroup(bg, text)
        self.add(group)
```

## Applying Style to Submobjects

```python
# Apply to all submobjects (family=True, default)
group.set_fill(RED, opacity=0.5, family=True)

# Apply only to parent, not submobjects
group.set_fill(RED, opacity=0.5, family=False)
```

## Style Based on Position

```python
class GradientFill(Scene):
    def construct(self):
        squares = VGroup(*[Square() for _ in range(5)]).arrange(RIGHT)

        for i, sq in enumerate(squares):
            opacity = (i + 1) / 5
            sq.set_fill(BLUE, opacity=opacity)

        self.add(squares)
```

## Copying Style

```python
# Copy style from another mobject
source = Circle().set_fill(RED, 0.5).set_stroke(WHITE, 4)
target = Square()
target.match_style(source)  # Now has same fill and stroke
```

## Best Practices

1. **Use fill_opacity for shapes** - Fully opaque fills can hide other elements
2. **Consistent stroke width** - Pick a width and stick with it
3. **Contrast fill and stroke** - Different colors help definition
4. **Use BackgroundRectangle for readability** - Behind text on busy backgrounds
5. **Chain methods for concise code** - But break lines if too long
