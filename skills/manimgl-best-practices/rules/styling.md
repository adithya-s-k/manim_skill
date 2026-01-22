# Styling in ManimGL

ManimGL provides comprehensive styling options for mobjects including fill, stroke, opacity, and special effects.

## Fill Properties

### Basic Fill

```python
from manimlib import *

# Set fill at creation
circle = Circle(fill_color=BLUE, fill_opacity=0.7)

# Set fill after creation
square = Square()
square.set_fill(RED, opacity=0.5)
```

### Fill Examples

```python
class FillExample(Scene):
    def construct(self):
        # Solid fill
        solid = Circle(radius=1)
        solid.set_fill(BLUE, opacity=1.0)

        # Transparent fill
        transparent = Circle(radius=1)
        transparent.set_fill(GREEN, opacity=0.3)

        # No fill (just outline)
        outline = Circle(radius=1)
        outline.set_fill(opacity=0)
        outline.set_stroke(YELLOW, width=4)

        VGroup(solid, transparent, outline).arrange(RIGHT, buff=1)
        self.add(solid, transparent, outline)
```

## Stroke Properties

### Basic Stroke

```python
# Set stroke at creation
line = Line(stroke_color=WHITE, stroke_width=4)

# Set stroke after creation
circle = Circle()
circle.set_stroke(BLUE, width=3, opacity=0.8)
```

### Stroke Width

```python
# Different stroke widths
thin = Circle().set_stroke(width=1)
medium = Circle().set_stroke(width=4)
thick = Circle().set_stroke(width=10)

VGroup(thin, medium, thick).arrange(RIGHT, buff=0.5)
```

### Stroke Behind Fill

```python
# Draw stroke behind fill (useful for borders)
shape = Circle(fill_color=BLUE, fill_opacity=0.8)
shape.set_stroke(WHITE, width=6, opacity=1, background=True)
```

## Backstroke

The `backstroke` feature adds an outline behind text or shapes for better visibility.

```python
# Text with backstroke (black outline)
text = Text("Readable Text", font_size=60)
text.set_backstroke(BLACK, width=5)

# Works great over complex backgrounds
text.set_backstroke(BLACK, width=8, opacity=1.0)
```

### Backstroke Example

```python
class BackstrokeExample(Scene):
    def construct(self):
        # Create complex background
        background = VGroup(*[
            Circle(radius=2 * np.random.random(), color=random_color())
            for _ in range(20)
        ])
        background.set_opacity(0.3)
        self.add(background)

        # Text with backstroke stands out
        text = Text("Clear and Readable", font_size=72, color=WHITE)
        text.set_backstroke(BLACK, width=10)
        self.add(text)
```

## Opacity Control

### Fill Opacity

```python
# Control fill transparency
circle = Circle()
circle.set_fill_opacity(0.5)

# Animate opacity
self.play(circle.animate.set_fill_opacity(1.0))
```

### Stroke Opacity

```python
# Control stroke transparency
square = Square()
square.set_stroke_opacity(0.7)
```

### Overall Opacity

```python
# Set both fill and stroke opacity
mobject = Circle()
mobject.set_opacity(0.5)  # Affects both fill and stroke
```

## Gloss (3D)

### Adding Gloss to 3D Objects

```python
# Make objects glossy/shiny
sphere = Sphere(radius=2, color=BLUE)
sphere.set_gloss(0.8)  # 0 (matte) to 1 (very glossy)

# Get gloss value
gloss_value = sphere.get_gloss()
```

## Shadow (3D)

### Adding Shadows

```python
# Add shadow to 3D objects
cube = Cube(color=RED)
cube.set_shadow(0.6)  # 0 (no shadow) to 1 (strong shadow)

# Get shadow value
shadow_value = cube.get_shadow()
```

## Combined Styling

### Complete Styling Control

```python
class CompleteStyling(Scene):
    def construct(self):
        shape = Circle(radius=2)

        # Set all properties
        shape.set_fill(BLUE, opacity=0.7)
        shape.set_stroke(WHITE, width=4, opacity=1.0)
        shape.set_backstroke(BLACK, width=6)

        self.add(shape)
```

## Style Matching

### Match Style from Another Mobject

```python
# Create styled source
source = Circle()
source.set_fill(BLUE, opacity=0.7)
source.set_stroke(WHITE, width=3)

# Match style
target = Square()
target.match_style(source)  # Copies all styling

# Match specific properties
target2 = Triangle()
target2.match_fill(source)   # Copy fill only
target2.match_stroke(source) # Copy stroke only
target2.match_color(source)  # Copy color only
```

## Gradients and Color Transitions

### Gradient Fills

```python
# Gradient across submobjects
text = Text("Gradient")
text.set_submobject_colors_by_gradient(BLUE, GREEN, YELLOW)

# For shapes with submobjects
squares = VGroup(*[Square() for _ in range(10)])
squares.arrange(RIGHT)
squares.set_submobject_colors_by_gradient(RED, PURPLE)
```

## Visual Effects

### Glow Effect

```python
# Create glow effect with multiple strokes
def add_glow(mobject, color=YELLOW, radius=0.5):
    glow_layers = VGroup(*[
        mobject.copy().set_stroke(
            color,
            width=width,
            opacity=0.3 / (i + 1)
        )
        for i, width in enumerate(range(2, 20, 2))
    ])
    return VGroup(glow_layers, mobject)

# Usage
circle = Circle(color=BLUE)
glowing_circle = add_glow(circle)
```

### Neon Effect

```python
def neon_style(mobject, color=BLUE):
    mobject.set_fill(color, opacity=0.2)
    mobject.set_stroke(color, width=3)
    mobject.set_backstroke(color, width=10, opacity=0.5)
    return mobject

# Usage
neon_text = neon_style(Text("NEON", font_size=90), BLUE)
```

## Style Presets

### Creating Reusable Styles

```python
# Define style functions
def outline_style(mobject):
    mobject.set_fill(opacity=0)
    mobject.set_stroke(WHITE, width=3)
    return mobject

def solid_style(mobject, color=BLUE):
    mobject.set_fill(color, opacity=1.0)
    mobject.set_stroke(color, width=0)
    return mobject

def glass_style(mobject, color=BLUE):
    mobject.set_fill(color, opacity=0.3)
    mobject.set_stroke(WHITE, width=2, opacity=0.8)
    mobject.set_gloss(0.9)
    return mobject

# Usage
circle1 = outline_style(Circle())
circle2 = solid_style(Circle(), RED)
circle3 = glass_style(Circle(), GREEN)
```

## Animating Styles

### Style Transitions

```python
class StyleAnimation(Scene):
    def construct(self):
        square = Square()
        square.set_fill(BLUE, opacity=0)
        square.set_stroke(WHITE, width=1)

        self.add(square)
        self.wait()

        # Animate style changes
        self.play(
            square.animate.set_fill(BLUE, opacity=0.7),
            square.animate.set_stroke(WHITE, width=5)
        )
        self.wait()

        # Change colors
        self.play(
            square.animate.set_fill(RED, opacity=0.9),
            square.animate.set_stroke(YELLOW, width=3)
        )
        self.wait()
```

## Full Styling Example

```python
class ComprehensiveStyleExample(Scene):
    def construct(self):
        # Different styling approaches
        shapes = VGroup()

        # Filled shape
        filled = Circle(radius=0.8)
        filled.set_fill(BLUE, opacity=0.8)
        filled.set_stroke(width=0)
        shapes.add(filled)

        # Outlined shape
        outlined = Circle(radius=0.8)
        outlined.set_fill(opacity=0)
        outlined.set_stroke(WHITE, width=4)
        shapes.add(outlined)

        # Transparent with border
        transparent = Circle(radius=0.8)
        transparent.set_fill(GREEN, opacity=0.3)
        transparent.set_stroke(GREEN, width=3)
        shapes.add(transparent)

        # With backstroke
        backstroke = Circle(radius=0.8)
        backstroke.set_fill(YELLOW, opacity=0.6)
        backstroke.set_stroke(WHITE, width=2)
        backstroke.set_backstroke(BLACK, width=5)
        shapes.add(backstroke)

        # Gradient (multiple submobjects)
        gradient_circles = VGroup(*[
            Circle(radius=0.15).shift(i * 0.3 * RIGHT)
            for i in range(-2, 3)
        ])
        gradient_circles.set_submobject_colors_by_gradient(RED, YELLOW)
        shapes.add(gradient_circles)

        # Arrange and display
        shapes.arrange(RIGHT, buff=1)
        self.play(LaggedStart(*[
            FadeIn(shape)
            for shape in shapes
        ], lag_ratio=0.2))
        self.wait()

        # Animate style transitions
        self.play(
            filled.animate.set_opacity(0.3),
            outlined.animate.set_stroke(YELLOW, width=8),
            transparent.animate.set_fill(RED, opacity=0.8)
        )
        self.wait()
```

## Best Practices

1. **Opacity for layering**: Use transparency to show overlapping elements
2. **Backstroke for readability**: Add backstroke to text over complex backgrounds
3. **Consistent stroke width**: Maintain visual hierarchy with consistent widths
4. **Fill vs stroke**: Use fill for areas, stroke for borders
5. **Gloss for realism**: Add gloss to 3D objects for more realistic appearance
6. **Match style for consistency**: Use style matching for consistent appearance
7. **Gradients for flow**: Use gradients to show transitions or relationships

## Common Patterns

### Outline style for emphasis

```python
def emphasize(mobject):
    return mobject.set_stroke(YELLOW, width=8, opacity=1.0)
```

### Transparent overlay

```python
def overlay(mobject, color=BLUE):
    return mobject.set_fill(color, opacity=0.2)
```

### Clean UI style

```python
def ui_style(mobject):
    mobject.set_fill(BLUE_C, opacity=0.9)
    mobject.set_stroke(WHITE, width=2)
    return mobject
```

### Highlighted text

```python
text = Text("Important", font_size=60)
text.set_fill(YELLOW, opacity=1.0)
text.set_backstroke(BLACK, width=8)
text.set_stroke(WHITE, width=1)
```
