"""
Graph and Function Plotting Patterns for Manim Community

Demonstrates Axes, NumberPlane, function plotting, and coordinate systems.
Adapted from 3b1b patterns for ManimCE.

Run with: manim -pql graph_plotting.py SceneName
"""

from manim import *
import numpy as np


class BasicAxes(Scene):
    """Basic axes setup and labeling."""

    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=8,
            y_length=5,
            axis_config={
                "include_tip": True,
                "include_numbers": True,
            },
        )

        # Labels
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait()


class FunctionPlotting(Scene):
    """Plotting functions on axes."""

    def construct(self):
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 9, 2],
            x_length=8,
            y_length=5,
            axis_config={"include_numbers": True},
        )

        # Plot y = x^2
        parabola = axes.plot(
            lambda x: x ** 2,
            color=BLUE,
            x_range=[-3, 3]
        )

        # Label
        label = MathTex(r"y = x^2", color=BLUE)
        label.next_to(parabola, UR)

        self.play(Create(axes))
        self.play(Create(parabola), Write(label))
        self.wait()


class MultipleFunctions(Scene):
    """Multiple functions on same axes."""

    def construct(self):
        axes = Axes(
            x_range=[-2 * PI, 2 * PI, PI / 2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=4,
        )

        # Plot sine and cosine
        sine = axes.plot(np.sin, color=BLUE, x_range=[-2 * PI, 2 * PI])
        cosine = axes.plot(np.cos, color=RED, x_range=[-2 * PI, 2 * PI])

        # Labels
        sin_label = MathTex(r"\sin(x)", color=BLUE).to_corner(UR)
        cos_label = MathTex(r"\cos(x)", color=RED).next_to(sin_label, DOWN)

        self.play(Create(axes))
        self.play(Create(sine), Write(sin_label))
        self.play(Create(cosine), Write(cos_label))
        self.wait()


class AreaUnderCurve(Scene):
    """Visualizing area under a curve (integration)."""

    def construct(self):
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 10, 2],
            x_length=8,
            y_length=5,
        )

        # Function
        func = axes.plot(lambda x: 0.5 * x ** 2, color=BLUE, x_range=[0, 4])

        # Area under curve from x=1 to x=3
        area = axes.get_area(
            func,
            x_range=[1, 3],
            color=BLUE,
            opacity=0.3
        )

        # Integral notation
        integral = MathTex(
            r"\int_1^3 \frac{x^2}{2} \, dx",
            font_size=48
        ).to_corner(UR)

        self.play(Create(axes))
        self.play(Create(func))
        self.play(FadeIn(area))
        self.play(Write(integral))
        self.wait()


class NumberPlaneExample(Scene):
    """Using NumberPlane for coordinate grid."""

    def construct(self):
        # Create number plane
        plane = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            }
        )

        # Plot a point
        point = Dot(plane.c2p(2, 3), color=RED, radius=0.15)
        point_label = MathTex("(2, 3)", color=RED).next_to(point, UR, buff=0.1)

        # Vector from origin to point
        vector = Arrow(
            plane.c2p(0, 0),
            plane.c2p(2, 3),
            buff=0,
            color=YELLOW
        )

        self.play(Create(plane))
        self.play(GrowArrow(vector))
        self.play(FadeIn(point), Write(point_label))
        self.wait()


class ParametricCurve(Scene):
    """Plotting parametric curves."""

    def construct(self):
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=7,
            y_length=7,
        )

        # Parametric curve (circle)
        circle = axes.plot_parametric_curve(
            lambda t: np.array([2 * np.cos(t), 2 * np.sin(t), 0]),
            t_range=[0, 2 * PI],
            color=BLUE
        )

        # Lissajous curve
        lissajous = axes.plot_parametric_curve(
            lambda t: np.array([2 * np.sin(3 * t), 2 * np.sin(2 * t), 0]),
            t_range=[0, 2 * PI],
            color=RED
        )

        self.play(Create(axes))
        self.play(Create(circle))
        self.wait()
        self.play(Transform(circle, lissajous))
        self.wait()


class TangentLine(Scene):
    """Showing tangent line to a curve."""

    def construct(self):
        axes = Axes(
            x_range=[-1, 4, 1],
            y_range=[-1, 10, 2],
            x_length=8,
            y_length=5,
        )

        # Function y = x^2
        func = axes.plot(lambda x: x ** 2, color=BLUE, x_range=[0, 3])

        # Point of tangency at x = 2
        x_val = 2
        point = Dot(axes.c2p(x_val, x_val ** 2), color=RED)

        # Tangent line: derivative of x^2 is 2x, at x=2 slope is 4
        tangent = axes.plot(
            lambda x: 4 * (x - 2) + 4,  # Point-slope form
            color=YELLOW,
            x_range=[0.5, 3.5]
        )

        # Label
        slope_label = MathTex(r"m = 2x = 4", color=YELLOW).to_corner(UR)

        self.play(Create(axes))
        self.play(Create(func))
        self.play(FadeIn(point))
        self.play(Create(tangent), Write(slope_label))
        self.wait()


class AnimatedGraph(Scene):
    """Animating a function parameter change."""

    def construct(self):
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=8,
            y_length=5,
        )

        # Amplitude tracker
        amplitude = ValueTracker(1)

        # Graph that updates with amplitude
        graph = always_redraw(
            lambda: axes.plot(
                lambda x: amplitude.get_value() * np.sin(x),
                color=BLUE,
                x_range=[-3, 3]
            )
        )

        # Amplitude display
        amp_text = always_redraw(
            lambda: MathTex(
                f"A = {amplitude.get_value():.1f}"
            ).to_corner(UR)
        )

        self.add(axes, graph, amp_text)

        # Animate amplitude change
        self.play(amplitude.animate.set_value(2), run_time=2)
        self.play(amplitude.animate.set_value(0.5), run_time=2)
        self.play(amplitude.animate.set_value(1.5), run_time=1)
        self.wait()


class RiemannSum(Scene):
    """Visualizing Riemann sums for integration."""

    def construct(self):
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            x_length=8,
            y_length=5,
        )

        # Function
        func = axes.plot(lambda x: 0.2 * x ** 2, color=BLUE, x_range=[0, 4])

        self.play(Create(axes), Create(func))
        self.wait()

        # Riemann rectangles
        dx_values = [1, 0.5, 0.25]

        for dx in dx_values:
            rects = axes.get_riemann_rectangles(
                func,
                x_range=[1, 3],
                dx=dx,
                color=BLUE,
                fill_opacity=0.5,
                stroke_width=1,
            )

            if dx == 1:
                self.play(Create(rects))
            else:
                self.play(Transform(rects, rects))

            self.wait()


class ImplicitFunction(Scene):
    """Plotting implicit functions (level curves)."""

    def construct(self):
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=7,
            y_length=7,
        )

        # Circle x^2 + y^2 = 4 as parametric
        circle = axes.plot_parametric_curve(
            lambda t: np.array([2 * np.cos(t), 2 * np.sin(t), 0]),
            t_range=[0, 2 * PI],
            color=BLUE
        )

        # Equation label
        equation = MathTex(r"x^2 + y^2 = 4", color=BLUE).to_corner(UR)

        self.play(Create(axes))
        self.play(Create(circle), Write(equation))
        self.wait()


class CoordinateLabeling(Scene):
    """Advanced coordinate labeling techniques."""

    def construct(self):
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 5, 1],
            x_length=7,
            y_length=7,
            axis_config={"include_numbers": True},
        )

        # Function
        func = axes.plot(lambda x: np.sqrt(x), color=BLUE, x_range=[0, 4])

        # Highlight a specific point
        x_val = 2
        y_val = np.sqrt(2)

        point = Dot(axes.c2p(x_val, y_val), color=RED)

        # Dashed lines to axes
        h_line = DashedLine(
            axes.c2p(0, y_val),
            axes.c2p(x_val, y_val),
            color=GREY
        )
        v_line = DashedLine(
            axes.c2p(x_val, 0),
            axes.c2p(x_val, y_val),
            color=GREY
        )

        # Labels
        x_label = MathTex("2").next_to(axes.c2p(x_val, 0), DOWN)
        y_label = MathTex(r"\sqrt{2}").next_to(axes.c2p(0, y_val), LEFT)

        self.play(Create(axes))
        self.play(Create(func))
        self.play(Create(v_line), Create(h_line))
        self.play(FadeIn(point), Write(x_label), Write(y_label))
        self.wait()


class PolarPlot(Scene):
    """Plotting in polar coordinates."""

    def construct(self):
        # Polar axes
        polar_plane = PolarPlane(
            radius_max=3,
            size=6,
        )

        # Polar curve: r = 1 + sin(theta) (cardioid)
        cardioid = polar_plane.plot_polar_graph(
            lambda theta: 1 + np.sin(theta),
            theta_range=[0, 2 * PI],
            color=BLUE
        )

        # Rose curve: r = 2*cos(3*theta)
        rose = polar_plane.plot_polar_graph(
            lambda theta: 2 * np.cos(3 * theta),
            theta_range=[0, PI],
            color=RED
        )

        self.play(Create(polar_plane))
        self.play(Create(cardioid))
        self.wait()
        self.play(Transform(cardioid, rose))
        self.wait()
