"""
Mathematical Visualization Patterns for Manim Community

Demonstrates LaTeX rendering, equation animations, and color-coded math.
Adapted from 3b1b patterns for ManimCE compatibility.

Run with: manim -pql math_visualization.py SceneName
"""

from manim import *


class ColorCodedEquation(Scene):
    """Demonstrates color-coding for syntax highlighting in equations."""

    def construct(self):
        # Method 1: Use set_color_by_tex after creation (safer approach)
        equation = MathTex(
            r"\vec{v}_1", r"=", r"\begin{bmatrix} 1 \\ \lambda_1 \end{bmatrix}"
        )
        equation.scale(1.5)

        # Color specific parts
        equation[0].set_color(TEAL)  # \vec{v}_1

        self.play(Write(equation))
        self.wait()

        # Second equation with multiple colored parts
        equation2 = MathTex(r"A", r"\vec{v}_1", r"=", r"\lambda_1", r"\vec{v}_1")
        equation2.scale(1.5)
        equation2[0].set_color(RED)      # A
        equation2[1].set_color(TEAL)     # first \vec{v}_1
        equation2[3].set_color(YELLOW)   # \lambda_1
        equation2[4].set_color(TEAL)     # second \vec{v}_1

        self.play(TransformMatchingTex(equation, equation2))
        self.wait()


class EquationDerivation(Scene):
    """Shows step-by-step equation derivation with highlighting."""

    def construct(self):
        # Starting equation
        eq1 = MathTex(r"x^2 + 5x + 6 = 0")
        eq1.to_edge(UP)

        self.play(Write(eq1))
        self.wait()

        # Factor step
        eq2 = MathTex(r"(x + 2)(x + 3) = 0")
        eq2.next_to(eq1, DOWN, buff=0.8)

        self.play(
            TransformFromCopy(eq1, eq2),
            run_time=1.5
        )
        self.wait()

        # Solutions
        eq3 = MathTex(r"x = -2", color=BLUE)
        eq4 = MathTex(r"x = -3", color=GREEN)
        solutions = VGroup(eq3, eq4).arrange(RIGHT, buff=1)
        solutions.next_to(eq2, DOWN, buff=0.8)

        self.play(
            LaggedStart(
                Write(eq3),
                Write(eq4),
                lag_ratio=0.3
            )
        )

        # Highlight solutions
        boxes = VGroup(
            SurroundingRectangle(eq3, color=BLUE),
            SurroundingRectangle(eq4, color=GREEN),
        )
        self.play(Create(boxes))
        self.wait()


class MatrixTransformation(Scene):
    """Demonstrates matrix notation and transformations."""

    def construct(self):
        # Matrix definition
        matrix = MathTex(
            r"A = \begin{bmatrix} 2 & 1 \\ 1 & 3 \end{bmatrix}"
        ).scale(1.2)

        self.play(Write(matrix))
        self.wait()

        # Move to side
        self.play(matrix.animate.to_edge(LEFT))

        # Show transformation
        vector = MathTex(
            r"\vec{x} = \begin{bmatrix} 1 \\ 1 \end{bmatrix}",
            color=YELLOW
        )
        vector.next_to(matrix, RIGHT, buff=1)

        self.play(Write(vector))
        self.wait()

        # Result
        result = MathTex(
            r"A\vec{x} = \begin{bmatrix} 3 \\ 4 \end{bmatrix}",
            tex_to_color_map={r"\vec{x}": YELLOW}
        )
        result.next_to(vector, RIGHT, buff=1)

        arrow = Arrow(vector.get_right(), result.get_left(), buff=0.2)

        self.play(GrowArrow(arrow), Write(result))
        self.wait()


class IntegralVisualization(Scene):
    """Shows integral notation with visual meaning."""

    def construct(self):
        # Integral expression
        integral = MathTex(
            r"\int_0^1 x^2 \, dx = \frac{1}{3}",
            font_size=64
        )
        integral.to_edge(UP)

        self.play(Write(integral))
        self.wait()

        # Create axes
        axes = Axes(
            x_range=[0, 1.2, 0.5],
            y_range=[0, 1.2, 0.5],
            x_length=5,
            y_length=3,
            axis_config={"include_tip": True},
        )
        axes.shift(DOWN)

        # Create graph
        graph = axes.plot(lambda x: x**2, x_range=[0, 1], color=BLUE)

        # Create area under curve
        area = axes.get_area(graph, x_range=[0, 1], color=BLUE, opacity=0.3)

        self.play(Create(axes))
        self.play(Create(graph))
        self.play(FadeIn(area))
        self.wait()


class SummationNotation(Scene):
    """Demonstrates summation and series notation."""

    def construct(self):
        # Summation formula
        formula = MathTex(
            r"\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}",
            font_size=64
        )

        self.play(Write(formula))
        self.wait()

        # Show first few terms
        terms = MathTex(
            r"= 1 + \frac{1}{4} + \frac{1}{9} + \frac{1}{16} + \cdots",
            font_size=48
        )
        terms.next_to(formula, DOWN, buff=0.8)

        self.play(Write(terms))
        self.wait()

        # Create surrounding box around result
        box = SurroundingRectangle(formula, color=YELLOW, buff=0.2)
        self.play(Create(box))
        self.wait()


class FunctionNotation(Scene):
    """Shows function definition and evaluation."""

    def construct(self):
        # Function definition
        f_def = MathTex(r"f(x) = x^2 + 2x + 1", font_size=56)
        f_def.to_edge(UP)

        self.play(Write(f_def))
        self.wait()

        # Evaluation at x=3
        eval_step1 = MathTex(r"f(3) = 3^2 + 2(3) + 1", font_size=48)
        eval_step2 = MathTex(r"f(3) = 9 + 6 + 1", font_size=48)
        eval_step3 = MathTex(r"f(3) = 16", font_size=48, color=GREEN)

        steps = VGroup(eval_step1, eval_step2, eval_step3)
        steps.arrange(DOWN, buff=0.5)
        steps.next_to(f_def, DOWN, buff=1)

        for step in steps:
            self.play(Write(step))
            self.wait(0.5)

        # Box the answer
        box = SurroundingRectangle(eval_step3, color=GREEN)
        self.play(Create(box))
        self.wait()


class LimitNotation(Scene):
    """Demonstrates limit notation and evaluation."""

    def construct(self):
        # Limit expression
        limit = MathTex(
            r"\lim_{x \to 0} \frac{\sin x}{x} = 1",
            font_size=64
        )

        self.play(Write(limit))
        self.wait()

        # Show approaching behavior
        approaching = MathTex(
            r"x \to 0: \quad",
            r"\frac{\sin(0.1)}{0.1} \approx 0.998",
            font_size=40
        )
        approaching.next_to(limit, DOWN, buff=1)

        self.play(Write(approaching))
        self.wait()


class DerivativeChainRule(Scene):
    """Shows the chain rule for derivatives."""

    def construct(self):
        title = Text("Chain Rule", font_size=48, color=BLUE)
        title.to_edge(UP)

        # Chain rule formula
        rule = MathTex(
            r"\frac{d}{dx}[f(g(x))] = f'(g(x)) \cdot g'(x)",
            font_size=48
        )

        # Example
        example_title = Text("Example:", font_size=36)
        example = MathTex(
            r"\frac{d}{dx}[\sin(x^2)] = \cos(x^2) \cdot 2x",
            tex_to_color_map={
                r"\sin": BLUE,
                r"\cos": BLUE,
                r"x^2": YELLOW,
                r"2x": YELLOW,
            },
            font_size=44
        )

        content = VGroup(rule, example_title, example)
        content.arrange(DOWN, buff=0.8)

        self.play(Write(title))
        self.play(Write(rule))
        self.wait()
        self.play(Write(example_title))
        self.play(Write(example))
        self.wait()


class TexHighlighting(Scene):
    """Advanced tex highlighting techniques."""

    def construct(self):
        # Create equation with substrings to highlight
        equation = MathTex(
            r"E", r"=", r"m", r"c^2",
            font_size=96
        )

        self.play(Write(equation))
        self.wait()

        # Highlight individual parts
        self.play(equation[0].animate.set_color(YELLOW))  # E
        self.wait(0.3)
        self.play(equation[2].animate.set_color(BLUE))    # m
        self.wait(0.3)
        self.play(equation[3].animate.set_color(RED))     # c^2
        self.wait()

        # Add labels
        e_label = Text("Energy", font_size=24, color=YELLOW)
        m_label = Text("Mass", font_size=24, color=BLUE)
        c_label = Text("Speed of Light", font_size=24, color=RED)

        e_label.next_to(equation[0], UP)
        m_label.next_to(equation[2], DOWN)
        c_label.next_to(equation[3], UP)

        self.play(
            FadeIn(e_label, shift=DOWN * 0.3),
            FadeIn(m_label, shift=UP * 0.3),
            FadeIn(c_label, shift=DOWN * 0.3),
        )
        self.wait()
