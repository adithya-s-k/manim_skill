# ManimGL LaTeX (Tex Class)

## Tex vs MathTex

**Important:** ManimGL uses `Tex` class (not `MathTex` like ManimCE).

```python
# ManimGL - use Tex with capital R raw strings
formula = Tex(R"\int_0^1 x^2 \, dx = \frac{1}{3}")

# NOT like ManimCE:
# formula = MathTex(r"\int...")  # Wrong for ManimGL
```

## Raw Strings with Capital R

Always use capital `R` for raw strings to avoid escaping issues:

```python
# Good - capital R
Tex(R"\frac{a}{b}")
Tex(R"\vec{v}")
Tex(R"\sum_{n=1}^{\infty}")

# Also works but less readable
Tex("\\frac{a}{b}")
```

## Color Mapping with t2c

Use `t2c` (tex_to_color) parameter to color specific parts:

```python
equation = Tex(
    R"E = mc^2",
    t2c={"E": BLUE, "m": GREEN, "c": YELLOW}
)
```

For more complex coloring:

```python
formula = Tex(
    R"\vec{F} = m\vec{a}",
    t2c={
        R"\vec{F}": BLUE,
        R"\vec{a}": RED,
        "m": GREEN,
    }
)
```

## set_color_by_tex

Color parts after creation:

```python
formula = Tex(R"\sum_{n=1}^{\infty} \frac{1}{n^2}")
formula.set_color_by_tex("n", BLUE)
formula.set_color_by_tex(R"\infty", YELLOW)
```

## Isolating Substrings

Get parts of a formula for animation:

```python
formula = Tex(R"a^2 + b^2 = c^2")

# Access by index
a_squared = formula[0]  # "a^2"

# Or use isolate parameter
formula = Tex(
    R"a^2", "+", R"b^2", "=", R"c^2",
)
# Now formula[0] is "a^2", formula[1] is "+", etc.
```

## Text vs Tex

```python
# Regular text
text = Text("Hello World")

# LaTeX math
math = Tex(R"\pi \approx 3.14159")

# Mixed (use TexText for text in math context)
mixed = TexText("The value of ", R"$\pi$", " is important")
```

## TexText

For text that may contain inline math:

```python
sentence = TexText(
    "The area is ", R"$\pi r^2$", ".",
    t2c={R"$\pi r^2$": YELLOW}
)
```

## Aligned Equations

```python
equations = Tex(R"""
    \begin{align*}
    f(x) &= x^2 + 2x + 1 \\
    &= (x + 1)^2
    \end{align*}
""")
```

## Common LaTeX Symbols

```python
# Greek letters
Tex(R"\alpha, \beta, \gamma, \delta, \theta, \phi, \pi")

# Operators
Tex(R"\sum, \prod, \int, \oint, \partial")

# Relations
Tex(R"\leq, \geq, \neq, \approx, \equiv")

# Sets
Tex(R"\in, \subset, \cup, \cap, \emptyset")

# Arrows
Tex(R"\rightarrow, \leftarrow, \Rightarrow, \Leftrightarrow")

# Fractions
Tex(R"\frac{a}{b}, \dfrac{a}{b}")

# Roots
Tex(R"\sqrt{x}, \sqrt[3]{x}")

# Matrices
Tex(R"\begin{pmatrix} a & b \\ c & d \end{pmatrix}")
```

## Font Size

```python
# Use font_size parameter
small = Tex(R"\pi", font_size=24)
large = Tex(R"\pi", font_size=72)

# Or scale after creation
small.scale(1.5)
```

## Backstroke for Readability

When placing text over colored backgrounds:

```python
label = Tex(R"f(x)")
label.set_backstroke(BLACK, 5)  # Black outline
```

## Debugging LaTeX

If LaTeX doesn't render:

1. Check for missing packages in your LaTeX installation
2. Try simpler expressions first
3. Check the intermediate `.tex` files in the output directory
4. Use `\text{}` for regular text inside math
