# Visual Techniques for Math Animation

Effective visualization patterns for explaining mathematical concepts.

## Core Principles

### 1. Progressive Disclosure
Never show everything at once. Build complexity gradually.

**Bad:** Show complete equation immediately
**Good:** Build equation term by term, explaining each part

```
Scene flow:
1. Show simple case: f(x) = x²
2. Add complexity: f(x) = ax²
3. Full form: f(x) = ax² + bx + c
```

### 2. Transform, Don't Replace
When possible, morph objects into new forms rather than fading out/in.

**Bad:** FadeOut(equation1), FadeIn(equation2)
**Good:** TransformMatchingTex(equation1, equation2)

This maintains visual continuity and shows the relationship between forms.

### 3. Color as Meaning
Use color consistently to encode meaning throughout the video.

**Pattern:**
- Input/given values: BLUE
- Output/results: GREEN
- Key terms being discussed: YELLOW highlight
- Errors/negatives: RED
- Neutral/supporting: WHITE/GREY

### 4. Spatial Relationships
Position encodes relationships:
- Left-to-right: transformation, time, causation
- Top-to-bottom: hierarchy, derivation
- Center: focus of attention
- Periphery: context, reference

---

## Animation Techniques

### Highlighting & Focus

**Indicate** - Brief flash to draw attention
```python
self.play(Indicate(term))
```

**Circumscribe** - Circle around important element
```python
self.play(Circumscribe(equation, color=YELLOW))
```

**FlashAround** - Dramatic attention on revelation
```python
self.play(FlashAround(result))
```

### Equation Manipulation

**Isolate terms** - Color or move specific parts
```python
equation.set_color_by_tex("x", BLUE)
```

**Step-by-step derivation** - Show each algebraic step
```python
step1 = MathTex(r"2x + 4 = 10")
step2 = MathTex(r"2x = 6")
step3 = MathTex(r"x = 3")
# Transform between steps with alignment
```

**Substitution** - Show value being plugged in
```python
# Animate the number moving into the variable's position
```

### Geometric Intuition

**Coordinate systems** - Always label axes
```python
axes = Axes(x_range=[-3, 3], y_range=[-2, 2])
labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
```

**Trace paths** - Show how points move
```python
trace = TracedPath(dot.get_center, stroke_color=YELLOW)
```

**Area visualization** - For integrals, sums
```python
area = axes.get_area(graph, x_range=[a, b], color=BLUE, opacity=0.5)
```

### 3D Techniques

**Camera orbiting** - Reveal 3D structure
```python
self.play(frame.animate.reorient(60, 70), run_time=3)
```

**Projection** - Show 3D object's 2D shadow
```python
# Helps connect 3D intuition to 2D formulas
```

**Slicing** - Cut through 3D objects
```python
# Show cross-sections to understand structure
```

---

## Common Visual Metaphors

### Vectors as Arrows
- Position vectors: arrows from origin
- Addition: tip-to-tail
- Scaling: stretching/shrinking

### Functions as Machines
- Input goes in one side
- Transformation happens
- Output comes out

### Matrices as Transformations
- Show grid being transformed
- Track where basis vectors go
- Emphasize determinant as area scaling

### Derivatives as Slopes
- Tangent line touching curve
- Zoom in to show local linearity
- Animate slope changing as point moves

### Integrals as Accumulation
- Riemann sums with rectangles
- Width → 0 animation
- Area filling under curve

---

## Scene Composition

### The Golden Layout
```
┌─────────────────────────────────┐
│           TITLE/CONTEXT         │  (top edge)
├─────────────────────────────────┤
│                                 │
│      MAIN VISUALIZATION         │  (center, largest area)
│                                 │
├─────────────────────────────────┤
│    EQUATION / FORMULA           │  (bottom third)
└─────────────────────────────────┘
```

### Side-by-Side Comparison
```
┌───────────────┬───────────────┐
│   BEFORE /    │   AFTER /     │
│   CONCEPT A   │   CONCEPT B   │
└───────────────┴───────────────┘
```

### Zoomed Detail
```
┌─────────────────────────────────┐
│  ┌─────┐                        │
│  │ZOOM │ ←── magnified detail   │
│  └─────┘                        │
│         Main context            │
└─────────────────────────────────┘
```

---

## Timing Guidelines

| Action | Typical Duration |
|--------|------------------|
| Simple shape creation | 0.5-1s |
| Text/equation writing | 1-2s |
| Transformation | 1-2s |
| Camera movement | 2-3s |
| Pause for absorption | 0.5-1s |
| Complex animation | 2-4s |

### Rhythm Pattern
Fast-fast-SLOW-fast-fast-SLOW

Quick animations for setup, slow down for key insights.

---

## Color Palettes

### Classic 3b1b
- Background: #1C1C1C (dark grey)
- Primary: #58C4DD (blue)
- Secondary: #83C167 (green)
- Accent: #FFFF00 (yellow)
- Warning: #FF6666 (red)

### High Contrast
- Background: #000000
- Primary: #FFFFFF
- Accent: #FFD700

### Soft Academic
- Background: #2D2D2D
- Primary: #6ECFFF
- Secondary: #98E898
- Accent: #FFE66D
