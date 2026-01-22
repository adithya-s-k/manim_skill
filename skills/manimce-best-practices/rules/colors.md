---
name: colors
description: Color constants, gradients, and color manipulation in Manim
metadata:
  tags: color, colors, gradient, rgb, hex, palette
---

# Colors in Manim

Manim provides predefined color constants and supports custom colors.

## Color Constants

### Primary Colors
```python
RED, GREEN, BLUE
YELLOW, ORANGE, PINK, PURPLE
WHITE, BLACK, GREY (or GRAY)
```

### Color Variants (Shades)
Most colors have variants from `_A` (lightest) to `_E` (darkest):
```python
BLUE_A, BLUE_B, BLUE_C, BLUE_D, BLUE_E
RED_A, RED_B, RED_C, RED_D, RED_E
GREEN_A, GREEN_B, GREEN_C, GREEN_D, GREEN_E
GREY_A, GREY_B, GREY_C, GREY_D, GREY_E
```

### Common Named Colors
```python
TEAL, TEAL_A, TEAL_B, TEAL_C, TEAL_D, TEAL_E
GOLD, GOLD_A, GOLD_B, GOLD_C, GOLD_D, GOLD_E
MAROON, MAROON_A, MAROON_B, MAROON_C, MAROON_D, MAROON_E
PURPLE, PURPLE_A, PURPLE_B, PURPLE_C, PURPLE_D, PURPLE_E
```

### Special Colors
```python
PURE_RED, PURE_GREEN, PURE_BLUE  # RGB primaries
LIGHT_GREY, DARK_GREY
LIGHTER_GREY, DARKER_GREY
LIGHT_BROWN, DARK_BROWN
```

## Using Colors

### Setting Color on Creation
```python
circle = Circle(color=RED)
square = Square(color=BLUE, fill_color=GREEN, fill_opacity=0.5)
text = Text("Hello", color=YELLOW)
```

### Setting Color After Creation
```python
circle = Circle()
circle.set_color(RED)
```

## Hex Colors

```python
# Use hex strings
circle = Circle(color="#FF5733")
square = Square(color="#2ECC71")

# RGB values (0-1 range)
from manim import rgb_to_color
custom = rgb_to_color([0.5, 0.2, 0.8])
```

## Fill vs Stroke Color

```python
square = Square()
square.set_fill(RED, opacity=0.8)      # Interior color
square.set_stroke(BLUE, width=4)       # Border color
```

### Combined Styling
```python
square = Square(
    color=BLUE,            # Sets both fill and stroke
    fill_opacity=0.5,      # Fill transparency
    stroke_width=4         # Border thickness
)
```

## Gradients

### Color Gradient on Mobject
```python
text = Text("GRADIENT")
text.set_color_by_gradient(RED, YELLOW, GREEN)
```

### Gradient Along Path
```python
line = Line(LEFT * 3, RIGHT * 3)
line.set_color_by_gradient(BLUE, GREEN, YELLOW)
```

## Color Interpolation

Create colors between two colors:

```python
from manim import interpolate_color

# Get color halfway between RED and BLUE
mid_color = interpolate_color(RED, BLUE, 0.5)

# Create a range of colors
colors = [interpolate_color(RED, BLUE, alpha) for alpha in np.linspace(0, 1, 10)]
```

## ManimColor Class

For advanced color manipulation, use ManimColor directly:

```python
from manim import ManimColor

# Create from various formats
color1 = ManimColor("#FF0000")           # From hex
color2 = ManimColor((0.0, 1.0, 0.5))     # From RGB floats (0-1)
color3 = ManimColor([255, 165, 0])       # From RGB ints (0-255)

# Color manipulation methods
lighter = color1.lighter()               # Lighter version
darker = color1.darker()                 # Darker version
inverted = color1.invert()               # Inverted color
with_alpha = color1.opacity(0.5)         # With 50% opacity

# Convert formats
hex_str = color1.to_hex()                # To hex string
rgb = color1.to_rgb()                    # To RGB float array
hsv = color1.to_hsv()                    # To HSV array

# Interpolation
mixed = color1.interpolate(color2, 0.5)  # Blend two colors
```

## Opacity

```python
# Set opacity (0 = transparent, 1 = opaque)
circle = Circle(fill_opacity=0.5, stroke_opacity=0.8)

# Modify opacity
circle.set_opacity(0.5)         # Both fill and stroke
circle.set_fill_opacity(0.7)    # Fill only
circle.set_stroke_opacity(0.3)  # Stroke only
```

## Color by Value

Color mobjects based on a value (useful for data visualization):

```python
class ColorByValue(Scene):
    def construct(self):
        dots = VGroup(*[Dot() for _ in range(10)]).arrange(RIGHT)

        for i, dot in enumerate(dots):
            # Color from blue (cold) to red (hot)
            dot.set_color(interpolate_color(BLUE, RED, i / 9))

        self.add(dots)
```

## Random Colors

```python
from manim import random_color, random_bright_color

circle = Circle(color=random_color())
square = Square(color=random_bright_color())
```

## Color Lists for Animations

```python
class ColorCycle(Scene):
    def construct(self):
        circle = Circle()
        self.add(circle)

        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        for color in colors:
            self.play(circle.animate.set_color(color), run_time=0.5)
```

## Best Practices

1. **Use color variants for depth** - `BLUE_E` for shadows, `BLUE_A` for highlights
2. **Maintain color consistency** - Use the same colors for related concepts
3. **Use opacity for layering** - Semi-transparent fills show overlapping
4. **Consider colorblind accessibility** - Avoid red-green only distinctions
5. **Use gradients sparingly** - They can be distracting
