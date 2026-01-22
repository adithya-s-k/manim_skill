# Equation Transforms - Reference Guide

**Example file**: `examples/equation_transforms.py`

## User Query Scenarios

This example addresses queries like:
- "Show step-by-step equation derivation"
- "Animate the quadratic formula derivation"
- "Highlight parts of an equation"
- "Show variable substitution with color tracking"
- "Add braces to explain equation parts"

## Scene Thinking Process (3b1b Style)

### 1. Core Concept
**Mathematical Derivations**: Step-by-step equation manipulation is clearer when terms are color-coded and transformations are animated smoothly.

### 2. Technical Implementation

#### Color-Coded Terms with t2c
```python
eq = Tex(
    r"ax^2 + bx + c = 0",
    t2c={"a": RED, "b": GREEN, "c": BLUE, "x": YELLOW}
)
```

#### Smooth Equation Transformation
```python
eq1 = Tex(r"ax^2 + bx + c = 0", t2c=colors)
eq2 = Tex(r"x^2 + \frac{b}{a}x + \frac{c}{a} = 0", t2c=colors)
self.play(TransformMatchingTex(eq1.copy(), eq2))
```

**Key insight**: `TransformMatchingTex` matches characters between equations and morphs them smoothly.

#### Highlighting with SurroundingRectangle
```python
part = eq[r"a^2"]  # Select by tex string
rect = SurroundingRectangle(part, color=RED, buff=0.05)
self.play(ShowCreation(rect))
```

#### Brace Annotations
```python
brace = Brace(eq["F"], UP, color=BLUE)
label = brace.get_text("Force", font_size=30)
self.play(GrowFromCenter(brace), FadeIn(label, UP))
```

### 3. Scene Variants

| Scene | Purpose |
|-------|---------|
| `QuadraticFormula` | Full derivation with step labels |
| `HighlightAndTransform` | Highlighting + visual proof |
| `BraceAnnotations` | F=ma with labeled parts |
| `ColorCodedSubstitution` | u-substitution with tracking |

## Key Patterns

### Pattern: Step Labels
```python
step_label = Text("Divide by a", font_size=24, color=GREY)
step_label.next_to(eq2, LEFT, buff=0.5)
self.play(FadeIn(step_label, LEFT))
```

### Pattern: Final Answer Box
```python
final = Tex(r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")
box = SurroundingRectangle(final, color=GOLD, buff=0.2)
self.play(ShowCreation(box))
```

### Pattern: Selecting Equation Parts
```python
# By tex substring
eq["x^2"]  # Returns submobject matching "x^2"
eq[r"\frac{b}{a}"]  # LaTeX commands work too

# By index
eq[0]  # First character/group
```

## Run Commands

```bash
manimgl equation_transforms.py QuadraticFormula -w
manimgl equation_transforms.py HighlightAndTransform -w
manimgl equation_transforms.py BraceAnnotations -w
manimgl equation_transforms.py ColorCodedSubstitution -w
```
