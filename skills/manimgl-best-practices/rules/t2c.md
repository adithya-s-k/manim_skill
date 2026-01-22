# Tex to Color Map (t2c) in ManimGL

The `t2c` parameter (tex_to_color_map) is a powerful feature for coloring specific parts of LaTeX expressions.

## Basic t2c Usage

### Coloring Math Symbols

```python
from manimlib import *

class T2CExample(Scene):
    def construct(self):
        # Color specific variables
        equation = Tex(
            R"E = mc^2",
            t2c={"E": BLUE, "m": GREEN, "c": YELLOW}
        )
        self.add(equation)
```

### Coloring Substrings

```python
# Color parts of the formula
formula = Tex(
    R"\int_0^1 x^2 \, dx = \frac{1}{3}",
    t2c={
        R"\int": BLUE,
        "x": GREEN,
        R"\frac{1}{3}": YELLOW
    }
)
```

## Advanced t2c Patterns

### Coloring Multiple Instances

```python
# All instances of a variable get colored
series = Tex(
    R"\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}",
    t2c={
        "n": BLUE,     # Colors all 'n's
        R"\pi": RED,
        R"\sum": GREEN
    }
)
```

### Using isolate with t2c

```python
# Isolate specific parts for individual control
equation = Tex(
    R"a^2 + b^2 = c^2",
    isolate=["a", "b", "c", "^2"],
    t2c={
        "a": RED,
        "b": GREEN,
        "c": BLUE,
        "^2": YELLOW
    }
)
```

## Dynamic Coloring

### set_color_by_tex

```python
# Color after creation
formula = Tex(R"f(x) = x^2 + 2x + 1")
formula.set_color_by_tex("x", BLUE)
formula.set_color_by_tex("f", GREEN)
formula.set_color_by_tex("1", YELLOW)
```

### Gradient Coloring

```python
# Apply gradient to entire formula
formula = Tex(R"\nabla \times \vec{E} = -\frac{\partial \vec{B}}{\partial t}")
formula.set_submobject_colors_by_gradient(BLUE, GREEN, YELLOW)
```

## Text Coloring (Text class)

### t2c for Text Objects

```python
# Color words in Text
text = Text(
    "The quick brown fox jumps",
    t2c={
        "quick": BLUE,
        "brown": ORANGE,
        "fox": GREEN
    }
)
```

### Multiple Styling Options

```python
# Combine t2c, t2f, t2s, t2w
text = Text(
    "Different styles and colors",
    t2c={"Different": RED, "colors": BLUE},
    t2f={"styles": "Consolas"},
    t2s={"styles": ITALIC},
    t2w={"Different": BOLD}
)
```

## Complex Examples

### Physics Equation with Color Coding

```python
class ColoredPhysicsEquation(Scene):
    def construct(self):
        # Maxwell's equation with color-coded components
        maxwell = Tex(
            R"\nabla \times \vec{E} = -\frac{\partial \vec{B}}{\partial t}",
            t2c={
                R"\nabla": BLUE,
                R"\vec{E}": RED,
                R"\vec{B}": GREEN,
                "t": YELLOW
            }
        )
        self.play(Write(maxwell))
        self.wait()
```

### Step-by-Step Derivation

```python
class ColoredDerivation(Scene):
    def construct(self):
        # Initial equation
        eq1 = Tex(
            R"(a + b)^2 = a^2 + 2ab + b^2",
            t2c={"a": BLUE, "b": GREEN}
        )

        # Expanded form
        eq2 = Tex(
            R"(a + b)^2 = (a + b)(a + b)",
            t2c={"a": BLUE, "b": GREEN}
        )

        # Show transformation
        self.play(Write(eq1))
        self.wait()
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait()
```

### Highlighting Specific Terms

```python
class HighlightTerms(Scene):
    def construct(self):
        # Quadratic formula with highlighted discriminant
        formula = Tex(
            R"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
            t2c={
                "x": WHITE,
                "b": BLUE,
                "a": GREEN,
                "c": YELLOW,
                R"b^2 - 4ac": RED  # Discriminant in red
            }
        )

        # Add label for discriminant
        discriminant_label = Text("Discriminant", color=RED, font_size=30)
        discriminant_label.next_to(formula, DOWN)

        self.play(Write(formula))
        self.play(FadeIn(discriminant_label, shift=UP))
        self.wait()
```

## Coloring LaTeX Operators

```python
# Color different operator types
expression = Tex(
    R"\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}",
    t2c={
        R"\int": BLUE,          # Integral
        "e": GREEN,              # Exponential
        R"\pi": RED,            # Pi
        "x": YELLOW,            # Variable
        "2": ORANGE             # Exponent
    }
)
```

## Best Practices

1. **Use raw strings with R**: Always use `R"..."` for LaTeX strings in ManimGL
2. **Test isolate first**: Use `isolate=` to verify what can be colored independently
3. **Consistent color scheme**: Use meaningful colors (e.g., variables in blue, constants in green)
4. **Don't over-color**: Too many colors can be distracting
5. **Color for emphasis**: Highlight the important parts you want viewers to focus on

## Common Patterns

### Creating a color scheme for math

```python
MATH_COLORS = {
    "variables": BLUE,
    "constants": GREEN,
    "operators": YELLOW,
    "results": RED
}

equation = Tex(
    R"x^2 + y^2 = r^2",
    t2c={
        "x": MATH_COLORS["variables"],
        "y": MATH_COLORS["variables"],
        "r": MATH_COLORS["constants"]
    }
)
```

### Animating color changes

```python
class AnimateColorChange(Scene):
    def construct(self):
        formula = Tex(R"f(x) = x^2")

        # Start with one color
        formula.set_color(BLUE)
        self.add(formula)
        self.wait()

        # Animate to different colors
        self.play(formula.animate.set_color_by_tex("x", RED))
        self.wait()
```

## Troubleshooting

### If t2c doesn't work:

1. Check if the substring exists exactly in the LaTeX string
2. Use `isolate=` to separate the part you want to color
3. Remember that spacing matters in LaTeX
4. Use raw strings `R"..."` not regular strings

### Example of common issue:

```python
# This might not work if spaces don't match:
wrong = Tex(R"a+b", t2c={"a + b": RED})  # Won't match "a+b"

# This will work:
right = Tex(R"a + b", t2c={"a": RED, "b": BLUE})
```
