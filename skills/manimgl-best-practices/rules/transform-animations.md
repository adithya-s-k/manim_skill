# Transform Animations in ManimGL

Transform animations morph one mobject into another or animate changes to mobject properties.

## Transform

The basic `Transform` changes one mobject to look like another.

### Basic Transform

```python
from manimlib import *

class BasicTransform(Scene):
    def construct(self):
        square = Square()
        circle = Circle()

        self.play(ShowCreation(square))
        self.wait()

        # Transform square into circle
        self.play(Transform(square, circle))
        self.wait()

        # Note: After transform, square now looks like circle
        # but it's still the square object
```

### Key Insight

After `Transform(A, B)`:
- Object A remains in the scene
- Object A now looks like B
- Object B is not added to the scene

## ReplacementTransform

`ReplacementTransform` replaces the source with the target.

```python
class ReplacementTransformExample(Scene):
    def construct(self):
        square = Square(color=BLUE)
        circle = Circle(color=RED)

        self.play(ShowCreation(square))
        self.wait()

        # Replace square with circle
        self.play(ReplacementTransform(square, circle))
        self.wait()

        # After this, circle is in the scene, not square
```

### When to Use Each

```python
# Use Transform when:
# - You want to keep the same mobject reference
square.transform_into_circle = lambda: Transform(square, Circle())

# Use ReplacementTransform when:
# - You want to swap objects
# - The target object should remain
self.play(ReplacementTransform(old_text, new_text))
```

## TransformMatchingTex

Morphs LaTeX expressions by matching substrings.

```python
class TexTransformExample(Scene):
    def construct(self):
        eq1 = Tex(R"a^2 + b^2 = c^2")
        eq2 = Tex(R"a^2 = c^2 - b^2")

        self.play(Write(eq1))
        self.wait()

        # Matching parts smoothly transform
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait()
```

### With Color Mapping

```python
class ColoredTexTransform(Scene):
    def construct(self):
        # Set up equations with colors
        eq1 = Tex(
            R"(a + b)^2 = a^2 + 2ab + b^2",
            t2c={"a": BLUE, "b": GREEN}
        )
        eq2 = Tex(
            R"(a + b)^2 = (a + b)(a + b)",
            t2c={"a": BLUE, "b": GREEN}
        )

        self.play(Write(eq1))
        self.wait()
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait()
```

### With isolate Parameter

```python
# Isolate specific parts for better matching
eq1 = Tex(
    R"x^2 + 2x + 1",
    isolate=["x", "^2", "+", "1", "2"]
)
eq2 = Tex(
    R"(x + 1)^2",
    isolate=["x", "^2", "+", "1", "(", ")"]
)

self.play(Write(eq1))
self.wait()
self.play(TransformMatchingTex(eq1, eq2))
```

### With Key Mapping

```python
# Map specific substrings
eq1 = Tex(R"x^2 + y^2 = r^2")
eq2 = Tex(R"a^2 + b^2 = c^2")

self.play(Write(eq1))
self.wait()
self.play(TransformMatchingTex(
    eq1, eq2,
    key_map={
        "x": "a",
        "y": "b",
        "r": "c"
    }
))
```

## TransformMatchingShapes

Morphs objects by matching similar shapes.

```python
class ShapeTransform(Scene):
    def construct(self):
        # Source group
        source = VGroup(
            Circle(radius=0.5, color=BLUE),
            Square(side_length=1, color=GREEN),
            Triangle(color=YELLOW)
        )
        source.arrange(RIGHT, buff=0.5)

        # Target group
        target = VGroup(
            Circle(radius=1, color=RED),
            Square(side_length=0.5, color=PURPLE),
            Triangle(color=ORANGE)
        )
        target.arrange(DOWN, buff=0.5)

        self.play(ShowCreation(source))
        self.wait()
        self.play(TransformMatchingShapes(source, target))
        self.wait()
```

## MoveToTarget

Set a target state for a mobject and animate to it.

```python
class MoveToTargetExample(Scene):
    def construct(self):
        circle = Circle()
        self.play(ShowCreation(circle))

        # Set target state
        circle.generate_target()
        circle.target.shift(RIGHT * 3)
        circle.target.scale(2)
        circle.target.set_color(YELLOW)

        # Animate to target
        self.play(MoveToTarget(circle))
        self.wait()
```

### Multiple Targets

```python
# Set up multiple mobjects with targets
square = Square()
triangle = Triangle()

square.generate_target()
square.target.shift(LEFT * 2)

triangle.generate_target()
triangle.target.shift(RIGHT * 2)

self.play(
    MoveToTarget(square),
    MoveToTarget(triangle)
)
```

## FadeTransform

Cross-fades between two objects.

```python
class FadeTransformExample(Scene):
    def construct(self):
        text1 = Text("Hello", font_size=72)
        text2 = Text("World", font_size=72)

        self.play(Write(text1))
        self.wait()

        # Smooth cross-fade
        self.play(FadeTransform(text1, text2))
        self.wait()
```

## Rotate

Rotates a mobject.

```python
# Rotate by angle
square = Square()
self.play(Rotate(square, PI / 2))  # 90 degrees

# Rotate around a point
self.play(Rotate(square, PI, about_point=ORIGIN))

# Rotate around an axis (for 3D)
self.play(Rotate(cube, PI, axis=RIGHT))
```

## Rotating (Continuous)

Creates a continuous rotation.

```python
# Continuous rotation
square = Square()
self.play(Rotating(square, radians=2*PI, run_time=4))

# Infinite rotation with updater
square.add_updater(lambda m, dt: m.rotate(0.1 * dt))
self.wait(10)
```

## ScaleInPlace

Scales without changing center position.

```python
circle = Circle()
self.play(ScaleInPlace(circle, 2))  # Double size

# Scale around a point
self.play(ScaleInPlace(circle, 0.5, about_point=RIGHT))
```

## ApplyMethod

Animates any mobject method.

```python
# Using .animate syntax (preferred)
self.play(circle.animate.shift(RIGHT))
self.play(circle.animate.scale(2))
self.play(circle.animate.set_color(BLUE))

# Old syntax (still works)
self.play(ApplyMethod(circle.shift, RIGHT))
self.play(ApplyMethod(circle.scale, 2))
```

## Complex Transformations

### apply_complex_function

Transform using complex number operations.

```python
class ComplexTransform(Scene):
    def construct(self):
        plane = ComplexPlane()
        plane.add_coordinate_labels(font_size=20)

        # Create shape on complex plane
        circle = Circle(radius=1, color=BLUE)

        self.add(plane, circle)
        self.wait()

        # Apply complex function (e.g., z^2)
        self.play(
            circle.animate.apply_complex_function(lambda z: z**2),
            run_time=3
        )
        self.wait()
```

### apply_function

Transform using arbitrary functions.

```python
# Apply custom transformation
grid = NumberPlane()

def wavy_transform(point):
    x, y, z = point
    return np.array([
        x,
        y + 0.5 * np.sin(2 * x),
        z
    ])

self.play(
    grid.animate.apply_function(wavy_transform),
    run_time=3
)
```

## Transformation Sequences

### Multi-step Transformations

```python
class TransformSequence(Scene):
    def construct(self):
        shapes = [
            Square(color=BLUE),
            Circle(color=GREEN),
            Triangle(color=YELLOW),
            Star(color=RED)
        ]

        current = shapes[0]
        self.play(ShowCreation(current))

        # Transform through each shape
        for next_shape in shapes[1:]:
            self.play(ReplacementTransform(current, next_shape))
            current = next_shape
            self.wait(0.3)
```

### Derivation Transformation

```python
class DerivationTransform(Scene):
    def construct(self):
        # Mathematical derivation
        steps = [
            Tex(R"x^2 - 4 = 0"),
            Tex(R"x^2 = 4"),
            Tex(R"x = \pm 2"),
        ]

        current = steps[0]
        self.play(Write(current))
        self.wait()

        for next_step in steps[1:]:
            next_step.move_to(current)
            self.play(TransformMatchingTex(current.copy(), next_step))
            current = next_step
            self.wait()
```

## Best Practices

1. **Transform vs ReplacementTransform**:
   - Use `Transform` to keep the object reference
   - Use `ReplacementTransform` to swap objects

2. **TransformMatchingTex**:
   - Use `isolate=` to control matching
   - Use `key_map=` for explicit mappings
   - Color consistently for smooth transitions

3. **Timing**:
   - Longer `run_time` for complex transformations
   - Match timing to content importance

4. **.animate syntax**:
   - Preferred for simple transformations
   - More readable and concise

5. **Path arc**:
   - Add `path_arc=90*DEGREES` for curved transformation paths

## Common Patterns

### Equation manipulation

```python
eq = Tex(R"2x + 4 = 10")
self.play(Write(eq))

eq2 = Tex(R"2x = 6")
eq2.move_to(eq)
self.play(TransformMatchingTex(eq.copy(), eq2))

eq3 = Tex(R"x = 3")
eq3.move_to(eq2)
self.play(TransformMatchingTex(eq2.copy(), eq3))
```

### Shape morphing

```python
shape = Circle()
self.play(ShowCreation(shape))

for new_shape in [Square(), Triangle(), Star(), Circle()]:
    self.play(Transform(shape, new_shape))
    self.wait(0.5)
```

### Text replacement

```python
text1 = Text("Before")
self.play(Write(text1))

text2 = Text("After")
text2.move_to(text1)
self.play(FadeTransform(text1, text2))
```

## Full Example

```python
class ComprehensiveTransform(Scene):
    def construct(self):
        # Title
        title = Text("Transformations", font_size=60)
        title.to_edge(UP)
        self.play(Write(title))

        # Shape transformations
        shape = Square(color=BLUE)
        self.play(ShowCreation(shape))
        self.wait()

        self.play(Transform(shape, Circle(color=GREEN)))
        self.wait()

        self.play(Transform(shape, Triangle(color=YELLOW)))
        self.wait()

        # Mathematical transformation
        eq1 = Tex(R"a^2 + b^2 = c^2")
        eq1.next_to(title, DOWN, buff=1)
        self.play(
            FadeOut(shape),
            Write(eq1)
        )
        self.wait()

        eq2 = Tex(R"c = \sqrt{a^2 + b^2}")
        eq2.move_to(eq1)
        self.play(TransformMatchingTex(eq1.copy(), eq2))
        self.wait()

        # Clean up
        self.play(FadeOut(VGroup(title, eq2)))
```
