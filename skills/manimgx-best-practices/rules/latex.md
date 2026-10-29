---
name: latex
description: MathTex, Tex, Typst translation, coloring parts and multi-line equations in ManimGX
metadata:
  tags: latex, mathtex, tex, typst, formula, math, equation
---

# Math in ManimGX

ManimGX typesets math with Typst. You write LaTeX; the engine translates it. No LaTeX
installation, no packages.

## The three classes

- `MathTex(r"...")` — pure math, auto math mode.
- `Tex(r"words and $x^2$")` — mixed text and math; math in `$...$`.
- `Text("...")` — prose only.

```python
import manimgx as m

class Equation(m.Scene):
    def construct(self):
        eq = m.MathTex(r"E = mc^2", font_size=72, color=m.YELLOW)
        self.play(m.Write(eq))
```

Always use raw strings for math.

## What converts and what does not

Supported: fractions, roots, greek letters, integrals, sums, limits, relations, arrows, sets,
matrices, aligned equations — standard LaTeX.

Does **not** convert:

- `\usepackage`, `\def`, custom macros, `TexTemplate`.
- LaTeX packages and anything that needs a `.sty` file.
- CJK inside `MathTex`.

If a formula fails, simplify it. Do not add a package or retry the same string.

## Multi-part equations

Double braces make a part anywhere in the string:

```python
eq = m.MathTex("x={{y}}")      # two parts
eq[0].set_color(m.RED)
eq[1].set_color(m.BLUE)
```

Split explicitly for per-part animation:

```python
eq = m.MathTex("a", "^2", "+", "b", "^2", "=", "c", "^2")
eq[0].set_color(m.RED)
eq[3].set_color(m.BLUE)
eq[6].set_color(m.GREEN)
self.play(m.Write(eq))
```

## Coloring by substring

```python
eq = m.MathTex(
    r"e^x = x^0 + x^1 + \frac{1}{2}x^2 + \cdots",
    substrings_to_isolate=["x"],
)
eq.set_color_by_tex("x", m.YELLOW)
self.add(eq)
```

`set_color_by_tex` and `substrings_to_isolate` work in ManimGX; `TransformMatchingTex` uses
the same parts.

## Multi-line and aligned equations

```python
eqs = m.MathTex(
    r"a &= b + c \\",
    r"d &= e + f + g \\",
    r"h &= i",
)
self.add(eqs)
```

## Common symbols

```python
m.MathTex(r"\alpha \beta \gamma \delta \epsilon")
m.MathTex(r"\times \div \pm \cdot")
m.MathTex(r"\leq \geq \neq \approx \equiv")
m.MathTex(r"\rightarrow \leftarrow \Rightarrow \Leftrightarrow")
m.MathTex(r"\in \notin \subset \supset \cup \cap")
m.MathTex(r"\int_0^\infty e^{-x}\,dx")
m.MathTex(r"\sum_{n=1}^{\infty} \frac{1}{n^2}")
```
