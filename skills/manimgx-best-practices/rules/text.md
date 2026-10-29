---
name: text
description: Text, fonts, CJK, Paragraph and BulletedList in ManimGX
metadata:
  tags: text, font, cjk, typst, paragraph, bulletedlist, title
---

# Text in ManimGX

`Text` typesets prose with Typst, using the fonts ManimGX ships. There is no Pango/Cairo and
no system-font setup.

## Basic Text

```python
import manimgx as m

class Hello(m.Scene):
    def construct(self):
        text = m.Text("Hello World", font_size=48)
        self.play(m.Write(text))
```

## Parameters

```python
text = m.Text(
    "Hello World",
    font_size=48,        # an em is font_size / 96 scene units
    color=m.BLUE,
    weight=m.BOLD,       # NORMAL, BOLD, ...
    slant=m.ITALIC,      # NORMAL, ITALIC, OBLIQUE
    line_spacing=1.5,
)
```

- `font_size` default 48; `Text(...).scale(2)` also works.
- `font=` names a family; a family ManimGX doesn't ship is read from the system. You do not
  need to name a font for Chinese/Japanese/Korean — the bundled Noto CJK fonts fall back per
  character.

## CJK

```python
import manimgx as m

class Chinese(m.Scene):
    def construct(self):
        self.play(m.Write(m.Text("勾股定理")))
```

- `Text("中文")` works as-is; do not pass `font="Noto Sans CJK SC"` just to get glyphs.
- Never put CJK inside `MathTex`; put the Chinese label in `Text` next to the formula.

## Multi-line and lists

```python
para = m.Paragraph("First line", "second line", "third line", line_spacing=0.5)
bullets = m.BulletedList("Point one", "Point two", "Point three")
title = m.Title("A title")
```

## Coloring and gradients

```python
text = m.Text("Hello World")
text[0:5].set_color(m.RED)     # "Hello"
text[6:11].set_color(m.BLUE)   # "World"
text.set_color_by_gradient(m.RED, m.YELLOW, m.GREEN)
```

## Positioning

`Text` is a mobject; every placement method works:

```python
text.to_edge(m.UP)
text.to_corner(m.UL)
text.move_to(m.ORIGIN)
text.next_to(other, m.DOWN, buff=0.3)
```

## MarkupText is not available

Manim CE's Pango `MarkupText` does not exist in ManimGX. Use `Text` with `color=`, or
`Tex`/`Typst` for rich inline styling.
