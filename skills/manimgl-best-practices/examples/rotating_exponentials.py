"""
Rotating Exponentials and Complex Numbers

Visualizes e^(it) as a rotating vector in the complex plane,
showing how cosine emerges from combining two counter-rotating exponentials.

Run: manimgl rotating_exponentials.py RotatingExponential -w
Preview: manimgl rotating_exponentials.py RotatingExponential -p

Source: Adapted from 3b1b's Laplace transform video (2025)
"""
from manimlib import *
import numpy as np


class RotatingExponential(InteractiveScene):
    """
    Shows e^(it) as a rotating vector on the complex plane.
    The fundamental visualization of Euler's formula.
    """

    def construct(self):
        # Create complex plane
        plane = ComplexPlane(
            x_range=(-2, 2, 1),
            y_range=(-2, 2, 1),
            background_line_style={"stroke_opacity": 0.5}
        )
        plane.add_coordinate_labels(font_size=20)

        # Title
        title = Tex(r"e^{it}", font_size=60)
        title.to_corner(UL)

        self.play(FadeIn(plane), Write(title))

        # Create rotating vector
        omega = 1  # Angular frequency
        time_tracker = ValueTracker(0)

        # The vector
        vector = Vector(RIGHT, color=YELLOW)
        vector.add_updater(lambda v: v.put_start_and_end_on(
            ORIGIN,
            plane.n2p(np.exp(1j * time_tracker.get_value()))
        ))

        # Dot at tip
        tip_dot = Dot(color=YELLOW)
        tip_dot.add_updater(lambda d: d.move_to(vector.get_end()))

        # Traced path (the unit circle)
        traced = TracedPath(
            tip_dot.get_center,
            stroke_color=BLUE,
            stroke_width=2,
        )

        # Angle arc
        angle_arc = always_redraw(lambda: Arc(
            start_angle=0,
            angle=time_tracker.get_value() % TAU,
            radius=0.3,
            color=GREEN
        ))

        # Angle label
        angle_label = Tex("t", font_size=30, color=GREEN)
        angle_label.add_updater(lambda m: m.move_to(
            0.5 * (np.cos(time_tracker.get_value() / 2) * RIGHT +
                   np.sin(time_tracker.get_value() / 2) * UP)
        ))

        self.play(
            GrowArrow(vector),
            FadeIn(tip_dot),
            FadeIn(angle_arc),
            FadeIn(angle_label),
        )
        self.add(traced)

        # Rotate through one full cycle
        self.play(
            time_tracker.animate.set_value(TAU),
            run_time=4,
            rate_func=linear
        )

        # Continue rotating
        time_tracker.add_updater(lambda m, dt: m.increment_value(dt))
        self.wait(4)


class CounterRotatingExponentials(InteractiveScene):
    """
    Shows how e^(it) + e^(-it) = 2cos(t).
    Two counter-rotating vectors that sum to give real cosine.
    """

    def construct(self):
        # Create complex plane
        plane = ComplexPlane(
            x_range=(-3, 3, 1),
            y_range=(-2, 2, 1),
            background_line_style={"stroke_opacity": 0.4}
        )
        plane.add_coordinate_labels(font_size=18)

        self.play(FadeIn(plane))

        # Time tracker
        time_tracker = ValueTracker(0)

        # e^(it) vector (counter-clockwise)
        v1 = Vector(RIGHT, color=BLUE)
        v1.add_updater(lambda v: v.put_start_and_end_on(
            ORIGIN,
            plane.n2p(np.exp(1j * time_tracker.get_value()))
        ))

        # e^(-it) vector (clockwise)
        v2 = Vector(RIGHT, color=RED)
        v2.add_updater(lambda v: v.put_start_and_end_on(
            ORIGIN,
            plane.n2p(np.exp(-1j * time_tracker.get_value()))
        ))

        # Sum vector (always real = 2cos(t))
        v_sum = Vector(RIGHT, color=GREEN, stroke_width=6)
        v_sum.add_updater(lambda v: v.put_start_and_end_on(
            ORIGIN,
            plane.n2p(2 * np.cos(time_tracker.get_value()))
        ))

        # Labels
        labels = VGroup(
            Tex(r"e^{it}", color=BLUE, font_size=36),
            Tex(r"e^{-it}", color=RED, font_size=36),
            Tex(r"e^{it} + e^{-it} = 2\cos(t)", color=GREEN, font_size=36),
        )
        labels.arrange(DOWN, aligned_edge=LEFT)
        labels.to_corner(UL)

        # Traced paths
        dot1 = Dot(color=BLUE, radius=0.05)
        dot1.add_updater(lambda d: d.move_to(v1.get_end()))
        trace1 = TracedPath(dot1.get_center, stroke_color=BLUE, stroke_width=1)

        dot2 = Dot(color=RED, radius=0.05)
        dot2.add_updater(lambda d: d.move_to(v2.get_end()))
        trace2 = TracedPath(dot2.get_center, stroke_color=RED, stroke_width=1)

        self.play(
            GrowArrow(v1),
            GrowArrow(v2),
            Write(labels[0]),
            Write(labels[1]),
        )
        self.add(dot1, dot2, trace1, trace2)

        # Rotate to show counter-rotation
        self.play(
            time_tracker.animate.set_value(TAU),
            run_time=4,
            rate_func=linear
        )

        # Now show the sum
        self.play(
            GrowArrow(v_sum),
            Write(labels[2]),
        )

        # Continue rotating to show sum is always real
        time_tracker.add_updater(lambda m, dt: m.increment_value(dt))
        self.wait(6)


class EulersFormula(InteractiveScene):
    """
    The famous e^(i*pi) = -1 visualization.
    Shows how rotating by pi radians lands at -1.
    """

    def construct(self):
        # Create plane
        plane = ComplexPlane(
            x_range=(-2, 2, 1),
            y_range=(-1.5, 1.5, 1),
        )
        plane.add_coordinate_labels(font_size=20)

        # Unit circle
        circle = Circle(radius=1, color=BLUE_C, stroke_width=2)

        self.play(FadeIn(plane), ShowCreation(circle))

        # Start at 1
        start_dot = Dot(plane.n2p(1), color=YELLOW)
        start_label = Tex("1", font_size=30)
        start_label.next_to(start_dot, DR, buff=0.1)

        self.play(FadeIn(start_dot), Write(start_label))

        # Show the formula building up
        formula = Tex(r"e^{i\pi}", font_size=72)
        formula.to_corner(UR)

        self.play(Write(formula))

        # Animate rotation from 1 to -1
        rotating_dot = Dot(plane.n2p(1), color=GREEN)
        rotating_vec = Vector(RIGHT, color=GREEN)

        angle_tracker = ValueTracker(0)
        rotating_vec.add_updater(lambda v: v.put_start_and_end_on(
            ORIGIN,
            plane.n2p(np.exp(1j * angle_tracker.get_value()))
        ))
        rotating_dot.add_updater(lambda d: d.move_to(rotating_vec.get_end()))

        # Arc to trace the path
        traced_arc = TracedPath(rotating_dot.get_center, stroke_color=YELLOW, stroke_width=3)

        self.play(GrowArrow(rotating_vec), FadeIn(rotating_dot))
        self.add(traced_arc)

        # Rotate to pi
        self.play(
            angle_tracker.animate.set_value(PI),
            run_time=3,
            rate_func=smooth
        )

        # Show = -1
        end_dot = Dot(plane.n2p(-1), color=RED)
        end_label = Tex("-1", font_size=30, color=RED)
        end_label.next_to(end_dot, DL, buff=0.1)

        equals = Tex(r"= -1", font_size=72)
        equals.next_to(formula, RIGHT)

        self.play(
            FadeIn(end_dot),
            Write(end_label),
            Write(equals),
        )
        self.wait()

        # Rearrange to famous form
        famous = Tex(r"e^{i\pi} + 1 = 0", font_size=72)
        famous.move_to(formula.get_center() + 0.5 * RIGHT)

        self.play(
            FadeOut(equals),
            TransformMatchingTex(formula, famous),
        )
        self.wait(2)


class ComplexExponentialSpiral(InteractiveScene):
    """
    Shows e^((a+bi)t) = e^(at) * e^(bit) as an exponential spiral.
    When a < 0, we get a decaying spiral (damped oscillation).
    """

    def construct(self):
        # Create plane
        plane = ComplexPlane(
            x_range=(-4, 4, 1),
            y_range=(-3, 3, 1),
            background_line_style={"stroke_opacity": 0.3}
        )
        plane.scale(0.8)

        self.play(FadeIn(plane))

        # Parameters
        a = -0.15  # Decay rate
        b = 2      # Angular frequency

        # Title showing the exponent
        title = Tex(r"e^{(-0.15 + 2i)t}", font_size=48)
        title.to_corner(UL)
        self.play(Write(title))

        # Time tracker
        time_tracker = ValueTracker(0)

        def get_position():
            t = time_tracker.get_value()
            return plane.n2p(np.exp((a + 1j * b) * t))

        # Spiral tracer
        dot = Dot(get_position(), color=YELLOW)
        dot.add_updater(lambda d: d.move_to(get_position()))

        spiral = TracedPath(
            dot.get_center,
            stroke_color=BLUE,
            stroke_width=2,
        )

        # Vector from origin
        vec = Vector(RIGHT, color=YELLOW)
        vec.add_updater(lambda v: v.put_start_and_end_on(ORIGIN, get_position()))

        self.play(FadeIn(dot), GrowArrow(vec))
        self.add(spiral)

        # Trace the spiral
        self.play(
            time_tracker.animate.set_value(15),
            run_time=8,
            rate_func=linear
        )
        self.wait()

        # Show components
        explanation = VGroup(
            Tex(r"e^{at}", r"\text{ controls amplitude}", font_size=30),
            Tex(r"e^{ibt}", r"\text{ controls rotation}", font_size=30),
        )
        explanation.arrange(DOWN, aligned_edge=LEFT)
        explanation.to_corner(DR)
        explanation[0][0].set_color(RED)
        explanation[1][0].set_color(BLUE)

        self.play(Write(explanation))
        self.wait(2)
