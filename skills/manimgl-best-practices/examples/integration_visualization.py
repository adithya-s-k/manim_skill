"""
Integration Visualization

Shows integration as accumulating area under a curve,
with animated filling and Riemann sum approximations.

Run: manimgl integration_visualization.py AreaUnderCurve -w
Preview: manimgl integration_visualization.py AreaUnderCurve -p

Source: Adapted from 3b1b's Laplace transform video (2025)
"""
from manimlib import *
import numpy as np


class AreaUnderCurve(InteractiveScene):
    """
    Basic visualization of definite integral as area under curve.
    Shows smooth accumulation of area from left to right.
    """

    def construct(self):
        # Create axes
        axes = Axes(
            x_range=(0, 5, 1),
            y_range=(0, 3, 1),
            width=10,
            height=5,
            axis_config={"include_tip": True}
        )
        axes.to_edge(DOWN, buff=1)

        x_label = Tex("x", font_size=30)
        x_label.next_to(axes.x_axis, RIGHT)
        y_label = Tex("f(x)", font_size=30)
        y_label.next_to(axes.y_axis, UP)

        self.play(
            ShowCreation(axes),
            Write(x_label),
            Write(y_label),
        )

        # Define a nice function
        def f(x):
            return 0.3 * x**2 - 0.5 * x + 1.5

        # Draw the curve
        curve = axes.get_graph(f, x_range=[0, 4.5], color=BLUE, stroke_width=3)
        curve_label = Tex("f(x) = 0.3x^2 - 0.5x + 1.5", font_size=24)
        curve_label.next_to(curve.get_end(), UR, buff=0.1)

        self.play(ShowCreation(curve, run_time=2))
        self.play(Write(curve_label))
        self.wait()

        # Show area accumulating
        t_tracker = ValueTracker(0.1)

        # Filled area using Polygon
        def get_area_polygon():
            t = max(0.1, t_tracker.get_value())
            xs = np.linspace(0, t, 50)
            points = [axes.c2p(x, f(x)) for x in xs]
            points.append(axes.c2p(t, 0))
            points.append(axes.c2p(0, 0))
            poly = Polygon(*points)
            poly.set_fill(BLUE_E, opacity=0.5)
            poly.set_stroke(width=0)
            return poly

        area = always_redraw(get_area_polygon)

        # Vertical line at current x
        def get_v_line():
            t = t_tracker.get_value()
            return Line(
                axes.c2p(t, 0),
                axes.c2p(t, f(t)),
                color=YELLOW,
                stroke_width=2
            )
        v_line = always_redraw(get_v_line)

        # Integral notation
        integral = Tex(
            r"\int_0^{x} f(t) \, dt",
            font_size=48
        )
        integral.to_corner(UL)

        self.play(
            FadeIn(area),
            FadeIn(v_line),
            Write(integral),
        )

        # Animate accumulation
        self.play(
            t_tracker.animate.set_value(4),
            run_time=5,
            rate_func=linear
        )
        self.wait()


class RiemannSums(InteractiveScene):
    """
    Shows Riemann sum approximation converging to true integral.
    Rectangles get thinner and better approximate the area.
    """

    def construct(self):
        # Create axes
        axes = Axes(
            x_range=(0, 4, 1),
            y_range=(0, 3, 1),
            width=8,
            height=4,
        )
        axes.center()

        def f(x):
            return 0.5 * np.sin(x) + 1.5

        curve = axes.get_graph(f, x_range=[0.5, 3.5], color=BLUE, stroke_width=3)

        self.play(ShowCreation(axes), ShowCreation(curve))

        # Create rectangles for different n values
        n_values = [4, 8, 16, 32]
        current_rects = None
        current_label = None

        for n in n_values:
            dx = 3 / n
            rects = VGroup()

            for i in range(n):
                x = 0.5 + i * dx
                height = f(x)
                rect = Rectangle(
                    width=dx * axes.x_axis.get_unit_size(),
                    height=height * axes.y_axis.get_unit_size(),
                    stroke_color=WHITE,
                    stroke_width=1,
                    fill_color=BLUE_E,
                    fill_opacity=0.6,
                )
                rect.move_to(axes.c2p(x + dx/2, height/2))
                rects.add(rect)

            label = Tex(f"n = {n}", font_size=36)
            label.to_corner(UR)

            if current_rects is None:
                self.play(
                    LaggedStartMap(FadeIn, rects, lag_ratio=0.05),
                    Write(label),
                )
            else:
                self.play(
                    ReplacementTransform(current_rects, rects),
                    ReplacementTransform(current_label, label),
                )

            current_rects = rects
            current_label = label
            self.wait(0.5)

        # Final message
        converge_text = Tex(r"\text{As } n \to \infty, \text{ sum } \to \int", font_size=36)
        converge_text.to_corner(UL)
        self.play(Write(converge_text))
        self.wait()


class ExponentialDecay(InteractiveScene):
    """
    Visualize the integral of e^(-x) from 0 to infinity.
    Shows that the total area is exactly 1.
    """

    def construct(self):
        # Create axes
        axes = Axes(
            x_range=(0, 6, 1),
            y_range=(0, 1.2, 0.5),
            width=10,
            height=4,
        )
        axes.to_edge(DOWN, buff=1.5)

        x_label = Tex("x", font_size=30).next_to(axes.x_axis, RIGHT)
        self.play(ShowCreation(axes), Write(x_label))

        # e^(-x) curve
        curve = axes.get_graph(
            lambda x: np.exp(-x),
            x_range=[0, 5.5],
            color=BLUE,
            stroke_width=3
        )
        curve_label = Tex(r"e^{-x}", font_size=36, color=BLUE)
        curve_label.next_to(curve.get_start(), UR)

        self.play(ShowCreation(curve), Write(curve_label))

        # Fill area progressively
        t_tracker = ValueTracker(0.1)

        def get_area():
            t = max(0.1, t_tracker.get_value())
            xs = np.linspace(0, t, 50)
            points = [axes.c2p(x, np.exp(-x)) for x in xs]
            points.append(axes.c2p(t, 0))
            points.append(axes.c2p(0, 0))
            poly = Polygon(*points)
            poly.set_fill(BLUE_E, opacity=0.5)
            poly.set_stroke(width=0)
            return poly

        area = always_redraw(get_area)

        # Show integral formula
        integral = Tex(
            r"\int_0^{\infty} e^{-x} \, dx = 1",
            font_size=48
        )
        integral.to_corner(UL)

        # Current value tracker
        value_label = Tex(r"\text{Area} \approx 0.00", font_size=30)
        value_num = value_label.make_number_changeable("0.00")
        value_num.add_updater(lambda m: m.set_value(1 - np.exp(-t_tracker.get_value())))
        value_label.to_corner(UR)

        self.play(
            FadeIn(area),
            Write(integral),
            Write(value_label),
        )

        # Animate the fill
        self.play(
            t_tracker.animate.set_value(5.5),
            run_time=6,
            rate_func=linear
        )
        self.wait(2)
