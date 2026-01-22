"""
Basic Animation Patterns for Manim Community

This file demonstrates fundamental animation techniques adapted from 3b1b patterns.
Run with: manim -pql basic_animations.py SceneName
"""

from manim import *


class ShapeCreation(Scene):
    """Demonstrates various ways to create and animate shapes."""

    def construct(self):
        # Create shapes
        circle = Circle(radius=1, color=BLUE, fill_opacity=0.5)
        square = Square(side_length=2, color=RED)
        triangle = Triangle(color=GREEN, fill_opacity=0.8)

        # Arrange shapes
        shapes = VGroup(circle, square, triangle).arrange(RIGHT, buff=1)

        # Different creation animations
        self.play(Create(circle))  # Draw outline progressively
        self.play(DrawBorderThenFill(square))  # Border first, then fill
        self.play(GrowFromCenter(triangle))  # Grow from center point

        self.wait()

        # Transform between shapes
        self.play(Transform(circle, square.copy().shift(UP * 2)))

        self.wait()


class TextAnimations(Scene):
    """Demonstrates text and LaTeX animations."""

    def construct(self):
        # Plain text
        title = Text("Manim Community", font_size=72, color=BLUE)
        self.play(Write(title))
        self.wait()

        # Move title up
        self.play(title.animate.to_edge(UP))

        # LaTeX math
        equation = MathTex(r"e^{i\pi} + 1 = 0", font_size=64)
        self.play(Write(equation))
        self.wait()

        # Transform equation
        expanded = MathTex(r"e^{i\pi} = -1", font_size=64)
        self.play(TransformMatchingTex(equation, expanded))

        self.wait()


class LaggedAnimations(Scene):
    """Demonstrates staggered animations using LaggedStart patterns."""

    def construct(self):
        # Create a grid of dots
        dots = VGroup(*[
            Dot(radius=0.15, color=interpolate_color(BLUE, RED, i / 24))
            for i in range(25)
        ]).arrange_in_grid(rows=5, cols=5, buff=0.5)

        # Staggered fade in
        self.play(
            LaggedStart(*[FadeIn(dot, scale=0.5) for dot in dots], lag_ratio=0.1)
        )
        self.wait()

        # Staggered transformation using LaggedStart with animate
        self.play(
            LaggedStart(
                *[dot.animate.scale(1.5).set_color(YELLOW) for dot in dots],
                lag_ratio=0.05
            )
        )
        self.wait()

        # Wave effect using AnimationGroup with rate_func
        self.play(
            LaggedStart(
                *[dot.animate(rate_func=there_and_back).shift(UP * 0.5) for dot in dots],
                lag_ratio=0.02,
                run_time=2
            )
        )


class AnimationComposition(Scene):
    """Demonstrates combining multiple animations."""

    def construct(self):
        # Create objects
        circle = Circle(color=BLUE, fill_opacity=0.5)
        label = Text("Circle", font_size=36).next_to(circle, DOWN)

        # Group them
        group = VGroup(circle, label)

        # Animate together
        self.play(
            Create(circle),
            Write(label),
            run_time=2
        )
        self.wait()

        # Sequential animations with Succession
        square = Square(color=RED, fill_opacity=0.5).shift(RIGHT * 3)
        square_label = Text("Square", font_size=36).next_to(square, DOWN)

        self.play(
            Succession(
                group.animate.shift(LEFT * 2),
                Create(square),
                Write(square_label),
                lag_ratio=0.5
            )
        )
        self.wait()


class PathAnimations(Scene):
    """Demonstrates movement along paths."""

    def construct(self):
        # Create a path
        path = VMobject()
        path.set_points_smoothly([
            LEFT * 3,
            LEFT * 2 + UP * 2,
            ORIGIN + UP,
            RIGHT * 2 + UP * 2,
            RIGHT * 3,
        ])
        path.set_color(GREY)

        # Create moving object
        dot = Dot(color=RED, radius=0.2)
        dot.move_to(path.get_start())

        self.add(path)
        self.play(Create(path))

        # Move along path
        self.play(MoveAlongPath(dot, path), run_time=3, rate_func=smooth)

        self.wait()


class ColorTransitions(Scene):
    """Demonstrates color manipulation and gradients."""

    def construct(self):
        # Color gradient on shapes
        squares = VGroup(*[
            Square(side_length=0.8, fill_opacity=0.8)
            for _ in range(7)
        ]).arrange(RIGHT, buff=0.2)

        # Apply gradient colors
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK]
        for square, color in zip(squares, colors):
            square.set_fill(color)
            square.set_stroke(WHITE, width=2)

        self.play(LaggedStartMap(GrowFromCenter, squares, lag_ratio=0.1))
        self.wait()

        # Animate color change
        self.play(
            *[square.animate.set_fill(interpolate_color(BLUE, RED, i / 6))
              for i, square in enumerate(squares)],
            run_time=2
        )
        self.wait()


class GroupOperations(Scene):
    """Demonstrates VGroup operations and arrangements."""

    def construct(self):
        # Create VGroup
        shapes = VGroup(
            Circle(color=RED),
            Square(color=GREEN),
            Triangle(color=BLUE),
        )

        # Arrange horizontally
        shapes.arrange(RIGHT, buff=1)
        self.play(Create(shapes))
        self.wait()

        # Scale entire group
        self.play(shapes.animate.scale(0.5))
        self.wait()

        # Arrange vertically
        self.play(shapes.animate.arrange(DOWN, buff=0.5))
        self.wait()

        # Apply operation to all
        self.play(shapes.animate.set_fill(YELLOW, opacity=0.5))

        self.wait()
