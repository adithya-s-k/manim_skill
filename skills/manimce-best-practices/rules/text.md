---
name: text
description: Text mobjects, fonts, and text styling in Manim
metadata:
  tags: text, font, typography, markup, paragraph
---

# Text in Manim

The `Text` class renders text using Pango/Cairo, supporting various fonts and styles.

## Basic Text

```python
from manim import *

class TextExample(Scene):
    def construct(self):
        text = Text("Hello World")
        self.play(Write(text))
```

## Text Parameters

```python
text = Text(
    "Hello World",
    font_size=48,           # Size (default: 48)
    color=BLUE,             # Text color
    font="Arial",           # Font family
    weight=BOLD,            # NORMAL, BOLD, etc.
    slant=ITALIC,           # NORMAL, ITALIC, OBLIQUE
    line_spacing=1.5,       # Space between lines
)
```

## Font Size

```python
# Using font_size parameter
small = Text("Small", font_size=24)
medium = Text("Medium", font_size=48)
large = Text("Large", font_size=72)

# Using scale after creation
text = Text("Hello").scale(2)
```

## Custom Fonts

```python
# Use any installed system font
text = Text("Custom Font", font="Comic Sans MS")
text = Text("Monospace", font="Courier New")
text = Text("Serif", font="Times New Roman")
```

## Text Styling with MarkupText

Use Pango markup for mixed styling within one Text object:

```python
class MarkupExample(Scene):
    def construct(self):
        text = MarkupText(
            f'all in red <span fgcolor="{YELLOW}">except this</span>',
            color=RED
        )
        self.play(Write(text))
```

### Available Markup Tags

```python
# Bold and italic
text = MarkupText('<b>Bold</b> and <i>Italic</i>')

# Colors using fgcolor
text = MarkupText('<span fgcolor="yellow">Yellow</span>')

# Subscripts and superscripts
text = MarkupText('H<sub>2</sub>O and x<sup>2</sup>')

# Font size
text = MarkupText('<big>Big</big> and <small>small</small>')

# Underline and strikethrough
text = MarkupText('<u>Underline</u> and <s>Strike</s>')

# Double underline with color
text = MarkupText('<span underline="double" underline_color="green">text</span>')

# Monospace
text = MarkupText('type <tt>help</tt> for help')
```

### Gradients in MarkupText

```python
# Global gradient
text = MarkupText("nice gradient", gradient=(BLUE, GREEN))

# Inline gradient
text = MarkupText(
    'nice <gradient from="RED" to="YELLOW">colored</gradient> text'
)
```

### Escaping Special Characters

```python
# Must escape these characters:
# > as &gt;
# < as &lt;
# & as &amp;
text = MarkupText("5 &gt; 3 and 2 &lt; 4")
```

## Multi-line Text

```python
# Using \n for line breaks
text = Text("Line 1\nLine 2\nLine 3")

# Using Paragraph for better control
from manim import Paragraph

para = Paragraph(
    "This is a longer text",
    "that spans multiple lines",
    "with automatic alignment",
    line_spacing=0.5
)
```

## Coloring Parts of Text

```python
class ColoredText(Scene):
    def construct(self):
        text = Text("Hello World")
        text[0:5].set_color(RED)    # "Hello" in red
        text[6:11].set_color(BLUE)  # "World" in blue
        self.play(Write(text))
```

## Text with Gradients

```python
text = Text("Gradient Text")
text.set_color_by_gradient(RED, YELLOW, GREEN)
```

## Accessing Characters

```python
text = Text("ABCDE")

# Individual characters
text[0]  # 'A'
text[1]  # 'B'

# Slices
text[0:3]  # 'ABC'
text[-1]   # 'E'

# Iterate
for char in text:
    char.set_color(random_color())
```

## Text Positioning

```python
# Standard positioning methods work
text = Text("Hello")
text.to_edge(UP)
text.to_corner(UL)
text.move_to(ORIGIN)
text.next_to(other_mobject, DOWN)
```

## Best Practices

1. **Use Text for regular text** - Simple and fast
2. **Use MarkupText for mixed styles** - When you need multiple colors/weights
3. **Use MathTex for math** - Text doesn't render LaTeX
4. **Install fonts system-wide** - Manim uses system fonts
5. **Keep font_size consistent** - Use the same size for related text
