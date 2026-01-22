# Text in ManimGL

ManimGL provides powerful text rendering capabilities through the `Text` and `TexText` classes.

## Text Class

The `Text` class renders text using system fonts with extensive styling options.

### Basic Text Creation

```python
from manimlib import *

class TextExample(Scene):
    def construct(self):
        # Basic text
        text = Text("Hello ManimGL")
        self.add(text)
```

### Font Customization

```python
# Specify font and size
text = Text("Custom Font", font="Consolas", font_size=90)

# Different fonts for different parts
text = Text(
    "Mixed fonts example",
    t2f={"Mixed": "Consolas", "fonts": "Arial"}
)
```

### Text Coloring

```python
# Color entire text
text = Text("Colored Text", color=BLUE)

# Color specific words
text = Text(
    "The quick brown fox",
    t2c={"quick": BLUE, "brown": ORANGE, "fox": GREEN}
)
```

### Text Styling

```python
# Slant (italic)
text = Text(
    "Italic and bold text",
    t2s={"Italic": ITALIC},
    t2w={"bold": BOLD}
)

# Combine color, font, slant, and weight
text = Text(
    "Fully styled text",
    font="Arial",
    font_size=48,
    t2c={"styled": RED},
    t2s={"styled": ITALIC},
    t2w={"text": BOLD},
    t2f={"text": "Consolas"}
)
```

## TexText Class

`TexText` combines LaTeX rendering with text, useful for mixing text and math.

### Basic TexText

```python
# Text with LaTeX support
text = TexText("The integral $\\int_0^1 x^2 dx$ equals $\\frac{1}{3}$")

# With font size
text = TexText("Hello World", font_size=72)

# Isolate parts for coloring
text = TexText(
    "Einstein's $E = mc^2$",
    isolate=["E", "m", "c"]
)
text.set_color_by_tex("E", BLUE)
text.set_color_by_tex("m", GREEN)
text.set_color_by_tex("c", YELLOW)
```

## Text vs TexText

- **Text**: Uses system fonts, no LaTeX, better font control
- **TexText**: LaTeX support for math symbols, uses LaTeX's text rendering

### When to Use Each

```python
# Use Text for pure text with custom fonts
title = Text("Machine Learning", font="Helvetica", font_size=60)

# Use TexText when mixing text and inline math
description = TexText("The function $f(x) = x^2$ is convex")

# Use Tex for pure mathematical expressions
formula = Tex(R"\sum_{i=1}^n i = \frac{n(n+1)}{2}")
```

## Text Positioning

```python
# Basic positioning
text = Text("Top")
text.to_edge(UP)

# Arrange multiple texts
title = Text("Title")
subtitle = Text("Subtitle", font_size=36)
VGroup(title, subtitle).arrange(DOWN, buff=0.5)

# Set width
text = Text("Long text that needs to fit")
text.set_width(FRAME_WIDTH - 1)
```

## Text with Background

```python
# Set backstroke for readability
text = Text("With Background", font_size=60)
text.set_backstroke(BLACK, width=5)

# Background rectangle (manually)
from manimlib.mobject.svg.tex_mobject import BackgroundRectangle
text = Text("Text")
bg = BackgroundRectangle(text, color=BLACK, fill_opacity=0.8)
self.add(bg, text)
```

## VGroup for Text Layout

```python
# Group multiple text objects
line1 = Text("First line")
line2 = Text("Second line")
line3 = Text("Third line")

paragraph = VGroup(line1, line2, line3)
paragraph.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
paragraph.to_edge(LEFT)
```

## Full Example

```python
class ComprehensiveTextExample(Scene):
    def construct(self):
        # Title with custom font
        title = Text(
            "Text Rendering in ManimGL",
            font="Arial",
            font_size=72,
            color=BLUE
        )
        title.to_edge(UP)

        # Description with mixed styling
        desc = Text(
            "Mix different fonts, colors, and styles",
            font="Helvetica",
            font_size=36,
            t2c={"fonts": RED, "colors": GREEN, "styles": YELLOW},
            t2w={"Mix": BOLD}
        )
        desc.next_to(title, DOWN, buff=0.5)

        # Mathematical description using TexText
        math_desc = TexText(
            "For equations like $E = mc^2$, use Tex or TexText",
            font_size=30
        )
        math_desc.next_to(desc, DOWN, buff=1)

        # Add all with animations
        self.play(Write(title))
        self.play(FadeIn(desc, shift=DOWN))
        self.play(Write(math_desc))
        self.wait()
```

## Best Practices

1. **Font availability**: Ensure fonts are installed on the system
2. **Use Text for UI elements**: Better control over appearance
3. **Use TexText for mixed content**: When you need both text and math
4. **Backstroke for visibility**: Add backstroke to text over complex backgrounds
5. **VGroup for layout**: Group related text elements for easier positioning
6. **t2c/t2f/t2s/t2w**: Use dictionaries for per-word styling

## Common Patterns

### Creating a text label with background

```python
def create_label(text_str, color=WHITE):
    label = Text(text_str, font_size=40, color=color)
    label.set_backstroke(BLACK, width=5)
    return label
```

### Multi-line text with alignment

```python
lines = [Text(line) for line in [
    "Line 1",
    "Longer line 2",
    "Line 3"
]]
paragraph = VGroup(*lines)
paragraph.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
```

### Highlighted text

```python
sentence = Text(
    "This word is highlighted",
    t2c={"highlighted": YELLOW},
    t2w={"highlighted": BOLD}
)
```
