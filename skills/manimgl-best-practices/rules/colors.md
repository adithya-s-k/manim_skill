# Colors in ManimGL

ManimGL provides extensive color support with built-in color constants, gradients, and color manipulation utilities.

## Color Constants

### Basic Colors

```python
# Primary colors
RED, GREEN, BLUE
YELLOW, CYAN, MAGENTA

# Grayscale
WHITE, GREY, GRAY, BLACK

# Common colors
ORANGE, PURPLE, PINK, BROWN
MAROON, TEAL, GOLD
```

### Color Variations

ManimGL provides color gradients with letter suffixes:

```python
# Blue variations (darkest to lightest)
BLUE_E  # Darkest blue
BLUE_D
BLUE_C
BLUE_B
BLUE_A  # Lightest blue

# Similarly for other colors:
RED_E, RED_D, RED_C, RED_B, RED_A
GREEN_E, GREEN_D, GREEN_C, GREEN_B, GREEN_A
YELLOW_E, YELLOW_D, YELLOW_C, YELLOW_B, YELLOW_A
```

### Usage Example

```python
from manimlib import *

class ColorExample(Scene):
    def construct(self):
        # Create circles with different color variations
        circles = VGroup(*[
            Circle(radius=0.5, color=color)
            for color in [BLUE_E, BLUE_D, BLUE_C, BLUE_B, BLUE_A]
        ])
        circles.arrange(RIGHT, buff=0.5)
        self.add(circles)
```

## Setting Colors

### Basic Color Setting

```python
# At creation
circle = Circle(color=BLUE)

# After creation
square = Square()
square.set_color(RED)

# Multiple mobjects
group = VGroup(Circle(), Square(), Triangle())
group.set_color(GREEN)
```

### Animated Color Changes

```python
class ColorAnimation(Scene):
    def construct(self):
        circle = Circle(color=BLUE)
        self.add(circle)

        # Animate color change
        self.play(circle.animate.set_color(RED))
        self.wait()

        # Another change
        self.play(circle.animate.set_color(YELLOW))
        self.wait()
```

## Gradients

### set_submobject_colors_by_gradient

```python
# Apply gradient to submobjects
text = Text("Gradient Text")
text.set_submobject_colors_by_gradient(BLUE, GREEN, YELLOW)

# Multiple objects with gradient
squares = VGroup(*[Square() for _ in range(10)])
squares.arrange(RIGHT)
squares.set_submobject_colors_by_gradient(RED, BLUE)
```

### Color Interpolation

```python
from manimlib.utils.color import interpolate_color

# Create color between two colors
mid_color = interpolate_color(RED, BLUE, 0.5)  # Purple

# Create gradient programmatically
n_colors = 10
gradient = [
    interpolate_color(RED, BLUE, alpha)
    for alpha in np.linspace(0, 1, n_colors)
]
```

## Advanced Color Techniques

### set_color_by_code (GLSL)

ManimGL allows dynamic coloring using GLSL code:

```python
# Color based on position
square = Square()
square.set_color_by_code("""
    color.r = x;
    color.g = y;
    color.b = 1.0;
""")
```

### set_color_by_xyz_func

```python
# Color based on 3D position
surface = Sphere(radius=2)
surface.set_color_by_xyz_func(
    glsl_snippet="float value = sqrt(x*x + y*y + z*z); return value;",
    min_value=0,
    max_value=5,
    colormap='viridis'
)
```

## Color for Text and LaTeX

### Coloring Text Parts

```python
# Color specific words
text = Text(
    "Red, Green, and Blue",
    t2c={"Red": RED, "Green": GREEN, "Blue": BLUE}
)
```

### Coloring LaTeX

```python
# Color math symbols
equation = Tex(
    R"E = mc^2",
    t2c={"E": BLUE, "m": GREEN, "c": YELLOW}
)

# Color by tex substring
formula = Tex(R"\int_0^1 x^2 dx")
formula.set_color_by_tex("x", BLUE)
formula.set_color_by_tex(R"\int", RED)
```

## RGB and Hex Colors

### Using RGB Values

```python
from manimlib.utils.color import rgb_to_color

# RGB values (0-1 range)
custom_color = rgb_to_color([0.5, 0.3, 0.8])
circle = Circle(color=custom_color)

# RGB from 0-255 range (convert to 0-1)
custom_color = rgb_to_color([128/255, 77/255, 204/255])
```

### Using Hex Colors

```python
from manimlib.utils.color import hex_to_rgb, rgb_to_color

# Hex color
hex_color = "#FF5733"
rgb = hex_to_rgb(hex_color)
color = rgb_to_color(rgb)

circle = Circle(color=color)
```

## Opacity and Transparency

### Setting Opacity

```python
# Transparent circle
circle = Circle(color=BLUE, fill_opacity=0.5)

# Change opacity
circle.set_opacity(0.7)

# Fill vs Stroke opacity
square = Square()
square.set_fill(BLUE, opacity=0.5)
square.set_stroke(WHITE, width=4, opacity=1.0)
```

## Color Utilities

### Getting Color from Mobject

```python
circle = Circle(color=BLUE)

# Get color
color = circle.get_color()

# Get fill color
fill_color = circle.get_fill_color()

# Get stroke color
stroke_color = circle.get_stroke_color()
```

### Color Matching

```python
# Match color from another mobject
circle = Circle(color=BLUE)
square = Square()
square.match_color(circle)

# Match fill color
square.match_fill(circle)

# Match stroke
square.match_stroke(circle)
```

## Color Schemes

### Creating Consistent Color Palettes

```python
# Define color scheme
COLOR_SCHEME = {
    "background": "#1e1e1e",
    "primary": BLUE_C,
    "secondary": GREEN_C,
    "accent": YELLOW_C,
    "text": WHITE,
    "highlight": RED_C
}

# Use in scene
class StyledScene(Scene):
    def construct(self):
        title = Text("Title", color=COLOR_SCHEME["primary"])
        subtitle = Text("Subtitle", color=COLOR_SCHEME["secondary"])
        highlight = Circle(color=COLOR_SCHEME["accent"])

        self.add(title, subtitle, highlight)
```

### 3Blue1Brown Color Scheme

```python
# Grant's typical colors
BLUE_3B1B = BLUE_C
GREEN_3B1B = GREEN_C
YELLOW_3B1B = YELLOW_C
RED_3B1B = RED_C

# Background
BACKGROUND_COLOR = "#0a0a0a"
```

## Gloss and Visual Properties

### Adding Gloss (for 3D)

```python
# Add glossy appearance
sphere = Sphere(radius=2, color=BLUE)
sphere.set_gloss(0.8)  # 0 to 1

# Get gloss value
gloss = sphere.get_gloss()
```

### Shadow

```python
# Add shadow (for 3D)
cube = Cube(color=RED)
cube.set_shadow(0.5)  # 0 to 1

# Get shadow value
shadow = cube.get_shadow()
```

## Full Color Example

```python
class ComprehensiveColorExample(Scene):
    def construct(self):
        # Color variations showcase
        blue_shades = VGroup(*[
            Circle(radius=0.4, color=color)
            for color in [BLUE_E, BLUE_D, BLUE_C, BLUE_B, BLUE_A]
        ])
        blue_shades.arrange(RIGHT, buff=0.3)
        blue_shades.to_edge(UP, buff=1)

        # Gradient
        squares = VGroup(*[Square(side_length=0.6) for _ in range(8)])
        squares.arrange(RIGHT, buff=0.2)
        squares.set_submobject_colors_by_gradient(RED, YELLOW, GREEN, BLUE)

        # Custom RGB color
        custom_circle = Circle(
            radius=1,
            color=rgb_to_color([0.8, 0.2, 0.6]),
            fill_opacity=0.7
        )
        custom_circle.shift(DOWN * 2)

        # Colored text
        text = Text(
            "Colorful Text",
            font_size=48,
            t2c={"Colorful": BLUE, "Text": GREEN}
        )
        text.next_to(custom_circle, UP, buff=0.5)

        # Add everything
        self.play(
            FadeIn(blue_shades, lag_ratio=0.1),
            FadeIn(squares, lag_ratio=0.1),
            ShowCreation(custom_circle),
            Write(text)
        )
        self.wait()

        # Animate color changes
        self.play(
            squares.animate.set_submobject_colors_by_gradient(PURPLE, ORANGE),
            custom_circle.animate.set_color(TEAL)
        )
        self.wait()
```

## Best Practices

1. **Use named constants**: Prefer `BLUE` over RGB values for readability
2. **Consistent color schemes**: Define color palettes for coherent visuals
3. **Gradients for emphasis**: Use gradients to show progression or relationships
4. **Opacity for layering**: Use transparency to show overlapping elements
5. **Color accessibility**: Ensure sufficient contrast for visibility
6. **t2c for LaTeX**: Color math expressions to highlight important parts
7. **Don't overdo it**: Too many colors can be distracting

## Common Patterns

### Rainbow gradient

```python
def rainbow_gradient(mobjects):
    colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
    VGroup(*mobjects).set_submobject_colors_by_gradient(*colors)
```

### Fade to color animation

```python
self.play(
    circle.animate.set_color(RED),
    run_time=2
)
```

### Color cycling

```python
colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
for color in colors:
    self.play(circle.animate.set_color(color), run_time=0.5)
    self.wait(0.2)
```
