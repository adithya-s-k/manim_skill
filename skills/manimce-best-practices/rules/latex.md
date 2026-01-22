---
name: latex
description: MathTex, Tex, LaTeX rendering and equation styling in Manim
metadata:
  tags: latex, mathtex, tex, equation, formula, math
---

# LaTeX in Manim

Manim uses LaTeX to render mathematical expressions and formatted text.

## MathTex vs Tex

- **MathTex**: Automatically wraps content in math mode (`align*` environment)
- **Tex**: Raw LaTeX - you control the mode

```python
from manim import *

class LaTeXComparison(Scene):
    def construct(self):
        # MathTex - auto math mode
        math = MathTex(r"E = mc^2")

        # Tex - need explicit math delimiters
        tex = Tex(r"$E = mc^2$")

        # Both render the same
        VGroup(math, tex).arrange(DOWN)
        self.add(math, tex)
```

## Basic MathTex

```python
class MathTexExample(Scene):
    def construct(self):
        # Simple equation
        eq1 = MathTex(r"x^2 + y^2 = z^2")

        # Fractions
        eq2 = MathTex(r"\frac{a}{b}")

        # Square roots
        eq3 = MathTex(r"\sqrt{2}")

        # Greek letters
        eq4 = MathTex(r"\alpha + \beta = \gamma")

        # Integrals
        eq5 = MathTex(r"\int_0^\infty e^{-x} dx")

        # Summations
        eq6 = MathTex(r"\sum_{n=1}^{\infty} \frac{1}{n^2}")

        equations = VGroup(eq1, eq2, eq3, eq4, eq5, eq6).arrange_in_grid(2, 3)
        self.add(equations)
```

## Coloring Parts of Equations

### Using set_color_by_tex

```python
class ColoredEquation(Scene):
    def construct(self):
        eq = MathTex(r"e^{i\pi} + 1 = 0")
        eq.set_color_by_tex("e", RED)
        eq.set_color_by_tex(r"\pi", BLUE)
        eq.set_color_by_tex("i", GREEN)
        self.add(eq)
```

### Using substrings_to_isolate

For precise coloring, isolate substrings first:

```python
class IsolatedColoring(Scene):
    def construct(self):
        eq = MathTex(
            r"e^x = x^0 + x^1 + \frac{1}{2}x^2 + \cdots",
            substrings_to_isolate=["x"]
        )
        eq.set_color_by_tex("x", YELLOW)
        self.add(eq)
```

### Using index_labels for debugging

```python
class DebugLabels(Scene):
    def construct(self):
        eq = MathTex(r"\frac{a}{b}")
        # Add index labels to see which index is which part
        self.add(index_labels(eq[0]))
        self.add(eq)
```

### Direct indexing

```python
eq = MathTex(r"a + b = c")
eq[0][0].set_color(RED)   # 'a'
eq[0][2].set_color(BLUE)  # 'b'
eq[0][4].set_color(GREEN) # 'c'
```

## Multi-part Equations

Split equations into parts for individual control:

```python
class MultiPartEquation(Scene):
    def construct(self):
        eq = MathTex("a", "^2", "+", "b", "^2", "=", "c", "^2")

        eq[0].set_color(RED)    # a
        eq[3].set_color(BLUE)   # b
        eq[6].set_color(GREEN)  # c

        self.play(Write(eq))
```

## Text with Math (Tex)

```python
class MixedContent(Scene):
    def construct(self):
        # Mix text and math
        tex = Tex(r"The area is $A = \pi r^2$")
        self.play(Write(tex))
```

## Custom LaTeX Packages

```python
class CustomPackage(Scene):
    def construct(self):
        template = TexTemplate()
        template.add_to_preamble(r"\usepackage{mathrsfs}")

        eq = Tex(
            r"$\mathscr{L}$",
            tex_template=template
        )
        self.add(eq)
```

## Equation Alignment

```python
class AlignedEquations(Scene):
    def construct(self):
        eqs = MathTex(
            r"a &= b + c \\",
            r"d &= e + f + g \\",
            r"h &= i"
        )
        self.add(eqs)
```

## Common LaTeX Symbols

```python
# Greek letters
MathTex(r"\alpha \beta \gamma \delta \epsilon")
MathTex(r"\Gamma \Delta \Theta \Lambda \Pi")

# Operators
MathTex(r"\times \div \pm \mp \cdot")

# Relations
MathTex(r"\leq \geq \neq \approx \equiv")

# Arrows
MathTex(r"\rightarrow \leftarrow \Rightarrow \Leftrightarrow")

# Sets
MathTex(r"\in \notin \subset \supset \cup \cap")

# Calculus
MathTex(r"\int \iint \oint \partial \nabla")
```

## Font Size

```python
# Using font_size parameter
eq = MathTex(r"E = mc^2", font_size=72)

# Using scale
eq = MathTex(r"E = mc^2").scale(2)
```

## Best Practices

1. **Use raw strings** - Always use `r"..."` for LaTeX
2. **Use MathTex for pure math** - Simpler than adding `$...$`
3. **Use Tex for mixed content** - When combining text and math
4. **Split for animation control** - Separate parts you'll animate differently
5. **Use substrings_to_isolate** - For reliable coloring of repeated elements
