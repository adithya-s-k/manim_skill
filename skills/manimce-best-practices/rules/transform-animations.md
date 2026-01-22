---
name: transform-animations
description: Transform, ReplacementTransform, and morphing animations
metadata:
  tags: transform, replacementtransform, morph, transformfromcopy
---

# Transform Animations

Animations that morph one mobject into another.

## Transform

Morphs the source mobject into the shape of the target. The source mobject is modified.

```python
class TransformExample(Scene):
    def construct(self):
        square = Square()
        circle = Circle()

        self.play(Create(square))
        self.play(Transform(square, circle))
        # Note: 'square' now looks like 'circle' but is still 'square'
```

**Important:** After Transform, the original variable still references the mobject, even though it looks like the target.

## ReplacementTransform

Morphs source into target and replaces the reference. More intuitive for most uses.

```python
class ReplacementTransformExample(Scene):
    def construct(self):
        square = Square()
        circle = Circle()
        triangle = Triangle()

        self.play(Create(square))
        self.play(ReplacementTransform(square, circle))
        # 'square' is removed, 'circle' is now in the scene
        self.play(ReplacementTransform(circle, triangle))
        # 'circle' is removed, 'triangle' is now in the scene
```

## Transform vs ReplacementTransform

```python
# Transform - source variable changes appearance
self.play(Transform(A, B))
# A is still in scene (but looks like B)
# B is NOT in scene

# ReplacementTransform - source is replaced by target
self.play(ReplacementTransform(A, B))
# A is removed from scene
# B is now in scene
```

## TransformFromCopy

Creates a copy of source and morphs it to target. Original remains unchanged.

```python
class TransformFromCopyExample(Scene):
    def construct(self):
        square = Square().shift(LEFT * 2)
        circle = Circle().shift(RIGHT * 2)

        self.add(square)
        self.play(TransformFromCopy(square, circle))
        # Both square and circle are now visible
```

## TransformMatchingShapes

Intelligently matches and transforms corresponding parts.

```python
class MatchingShapesExample(Scene):
    def construct(self):
        source = Text("ABC")
        target = Text("ABCD")

        self.play(Write(source))
        self.play(TransformMatchingShapes(source, target))
```

## TransformMatchingTex

Matches LaTeX parts by their TeX strings.

```python
class MatchingTexExample(Scene):
    def construct(self):
        eq1 = MathTex("a", "^2", "+", "b", "^2")
        eq2 = MathTex("a", "^2", "+", "2ab", "+", "b", "^2")

        self.play(Write(eq1))
        self.play(TransformMatchingTex(eq1, eq2))
```

## MoveToTarget

Pre-set a target state and animate to it.

```python
class MoveToTargetExample(Scene):
    def construct(self):
        square = Square()
        self.add(square)

        # Generate and modify target
        square.generate_target()
        square.target.shift(RIGHT * 2)
        square.target.set_color(RED)
        square.target.scale(2)

        self.play(MoveToTarget(square))
```

## Path Arc Transforms

Control the path of transformation with `path_arc`.

```python
class PathArcExample(Scene):
    def construct(self):
        dot1 = Dot(LEFT * 2)
        dot2 = Dot(RIGHT * 2)

        self.add(dot1)
        # Transform along an arc
        self.play(Transform(dot1, dot2, path_arc=PI/2))
```

## Chained Transformations

```python
class ChainedExample(Scene):
    def construct(self):
        shape = Square()
        self.play(Create(shape))

        # Chain of transformations
        for target in [Circle(), Triangle(), Star()]:
            self.play(Transform(shape, target))
            self.wait(0.5)
```

## Best Practices

1. **Use ReplacementTransform for clarity** - More intuitive variable behavior
2. **Use TransformFromCopy to preserve original** - When you need both visible
3. **Use TransformMatchingTex for equations** - Better alignment of matching parts
4. **Set path_arc for visual interest** - Curved paths look more dynamic
