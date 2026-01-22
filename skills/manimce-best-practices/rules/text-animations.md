---
name: text-animations
description: Write, AddTextLetterByLetter, TypeWithCursor text animations
metadata:
  tags: text, write, typing, letter, cursor, animation
---

# Text Animations

Animations specifically designed for text and equations.

## Write

The most common text animation. Simulates handwriting.

```python
from manim import *

class WriteExample(Scene):
    def construct(self):
        text = Text("Hello World")
        equation = MathTex(r"E = mc^2")

        self.play(Write(text))
        self.wait()
        self.play(Write(equation))
```

### Write Parameters

```python
self.play(Write(
    text,
    run_time=2,           # Override auto-calculated time
    rate_func=linear,     # Timing curve
    reverse=False,        # Write backwards if True
))
```

Write automatically adjusts `run_time` based on text length.

## AddTextLetterByLetter

Types text one character at a time.

```python
class LetterByLetterExample(Scene):
    def construct(self):
        text = Text("Typing effect")

        self.play(AddTextLetterByLetter(
            text,
            time_per_char=0.1  # Speed of typing
        ))
```

**Note:** Only works with `Text`, not `MathTex`.

## RemoveTextLetterByLetter

Reverse of AddTextLetterByLetter - removes character by character.

```python
class RemoveLetterByLetter(Scene):
    def construct(self):
        text = Text("Disappearing text")
        self.add(text)

        self.play(RemoveTextLetterByLetter(
            text,
            time_per_char=0.05
        ))
```

## TypeWithCursor

Types text with a visible cursor.

```python
class TypeWithCursorExample(Scene):
    def construct(self):
        text = Text("Typing with cursor")

        # Create cursor
        cursor = Rectangle(
            color=GREY_A,
            fill_color=GREY_A,
            fill_opacity=1.0,
            height=1.1,
            width=0.1,
        )

        self.play(TypeWithCursor(text, cursor))

        # Optional: blink cursor after typing
        self.play(Blink(cursor, blinks=3))
```

### Cursor Customization

```python
# Line cursor
cursor = Line(UP * 0.5, DOWN * 0.5, color=WHITE, stroke_width=2)

# Block cursor
cursor = Rectangle(width=0.5, height=1, fill_opacity=0.8, color=WHITE)

# Custom cursor position
self.play(TypeWithCursor(
    text,
    cursor,
    buff=0.05,           # Space between text and cursor
    keep_cursor_y=True,  # Keep cursor at consistent height
    leave_cursor_on=True # Show cursor after animation
))
```

## Blink (for cursors)

```python
class BlinkExample(Scene):
    def construct(self):
        cursor = Rectangle(height=1, width=0.1, fill_opacity=1)
        self.add(cursor)

        self.play(Blink(cursor, blinks=5, time_on=0.3, time_off=0.3))
```

## Word by Word Animation

Using LaggedStart for word-by-word appearance:

```python
class WordByWord(Scene):
    def construct(self):
        # Split into individual Text objects
        words = VGroup(
            Text("Hello"),
            Text("World"),
            Text("!")
        ).arrange(RIGHT, buff=0.3)

        self.play(LaggedStart(
            *[Write(word) for word in words],
            lag_ratio=0.5
        ))
```

## Equation Transformations

Animate between equations:

```python
class EquationTransform(Scene):
    def construct(self):
        eq1 = MathTex(r"a^2 + b^2 = c^2")
        eq2 = MathTex(r"c = \sqrt{a^2 + b^2}")

        self.play(Write(eq1))
        self.wait()
        self.play(TransformMatchingTex(eq1, eq2))
```

## Highlighting Text

```python
class HighlightText(Scene):
    def construct(self):
        text = Text("Important message")
        self.add(text)

        # Circumscribe (draw around)
        self.play(Circumscribe(text, color=YELLOW))

        # Indicate (pulse)
        self.play(Indicate(text, color=RED))

        # Flash
        self.play(Flash(text.get_center(), color=WHITE))
```

## Replacing Text

```python
class ReplaceText(Scene):
    def construct(self):
        text1 = Text("Before")
        text2 = Text("After")

        self.play(Write(text1))
        self.wait()

        # Transform text
        self.play(Transform(text1, text2))

        # Or replacement transform
        self.play(ReplacementTransform(text1, text2))
```

## Colored Text Animation

```python
class ColoredTextAnimation(Scene):
    def construct(self):
        text = Text("Colorful")
        self.play(Write(text))

        # Animate color change per letter
        self.play(LaggedStart(
            *[char.animate.set_color(random_bright_color()) for char in text],
            lag_ratio=0.1
        ))
```

## Best Practices

1. **Use Write for most text** - Natural and smooth
2. **Use AddTextLetterByLetter for "typing" effect** - Terminal/code aesthetics
3. **Use TypeWithCursor for interactive feel** - Good for tutorials
4. **Use TransformMatchingTex for equations** - Smooth mathematical transitions
5. **Adjust time_per_char for pacing** - 0.05-0.1 is usually good
6. **Only use Text (not MathTex) for letter-by-letter** - API limitation
