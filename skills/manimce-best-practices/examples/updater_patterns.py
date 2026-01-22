"""
Updater and ValueTracker Patterns for Manim Community

Demonstrates dynamic animations using updaters and ValueTracker.
Adapted from 3b1b's animation patterns for ManimCE.

Run with: manim -pql updater_patterns.py SceneName
"""

from manim import *
import numpy as np


class BasicUpdater(Scene):
    """Simple updater that makes an object follow another."""

    def construct(self):
        # Leader dot
        leader = Dot(color=RED, radius=0.2)
        leader_label = Text("Leader", font_size=24).next_to(leader, UP)

        # Follower that always stays next to leader
        follower = Dot(color=BLUE, radius=0.15)
        follower.add_updater(lambda m: m.next_to(leader, RIGHT, buff=0.5))

        follower_label = Text("Follower", font_size=24, color=BLUE)
        follower_label.add_updater(lambda m: m.next_to(follower, DOWN))

        self.add(leader, leader_label, follower, follower_label)

        # Move the leader - follower automatically follows
        self.play(leader.animate.shift(RIGHT * 3), run_time=2)
        self.play(leader.animate.shift(UP * 2), run_time=2)
        self.play(leader.animate.shift(LEFT * 4 + DOWN), run_time=2)
        self.wait()


class ValueTrackerBasics(Scene):
    """Demonstrates ValueTracker for animating numeric values."""

    def construct(self):
        # Create a ValueTracker
        tracker = ValueTracker(0)

        # DecimalNumber that displays the tracker value
        number = DecimalNumber(
            0,
            num_decimal_places=2,
            font_size=72,
            include_sign=True
        )
        number.add_updater(lambda m: m.set_value(tracker.get_value()))

        # Label
        label = Text("Value: ", font_size=48)
        label.next_to(number, LEFT)

        self.add(label, number)

        # Animate the tracker
        self.play(tracker.animate.set_value(10), run_time=2)
        self.wait(0.5)
        self.play(tracker.animate.set_value(-5), run_time=2)
        self.wait(0.5)
        self.play(tracker.animate.set_value(0), run_time=1)
        self.wait()


class CircleRadiusTracker(Scene):
    """Circle that grows/shrinks with a ValueTracker."""

    def construct(self):
        tracker = ValueTracker(1)

        # Circle with radius controlled by tracker
        circle = always_redraw(
            lambda: Circle(
                radius=tracker.get_value(),
                color=BLUE,
                fill_opacity=0.3
            )
        )

        # Radius label
        radius_text = always_redraw(
            lambda: MathTex(
                f"r = {tracker.get_value():.2f}"
            ).to_edge(UP)
        )

        self.add(circle, radius_text)

        # Animate radius changes
        self.play(tracker.animate.set_value(2.5), run_time=2)
        self.play(tracker.animate.set_value(0.5), run_time=2)
        self.play(tracker.animate.set_value(1.5), run_time=1)
        self.wait()


class RotatingUpdater(Scene):
    """Object that rotates continuously using dt (delta time)."""

    def construct(self):
        # Create rotating group
        square = Square(side_length=2, color=BLUE, fill_opacity=0.5)
        dot = Dot(color=RED).move_to(square.get_corner(UR))

        group = VGroup(square, dot)

        # Add rotation updater with dt for smooth rotation
        group.add_updater(lambda m, dt: m.rotate(dt * PI / 2))

        self.add(group)
        self.wait(4)  # Watch it rotate

        # Remove updater
        group.clear_updaters()
        self.wait()


class TracedPathExample(Scene):
    """Demonstrates TracedPath for drawing motion trails."""

    def construct(self):
        # Moving dot
        dot = Dot(color=RED, radius=0.15)
        dot.move_to(LEFT * 3)

        # Traced path follows the dot
        traced_path = TracedPath(
            dot.get_center,
            stroke_color=YELLOW,
            stroke_width=3
        )

        self.add(traced_path, dot)

        # Move dot in a pattern
        self.play(
            dot.animate.shift(RIGHT * 3 + UP * 2),
            run_time=1.5
        )
        self.play(
            dot.animate.shift(RIGHT * 2 + DOWN * 3),
            run_time=1.5
        )
        self.play(
            dot.animate.shift(LEFT * 2 + UP * 1),
            run_time=1.5
        )
        self.wait()


class SineWaveTracker(Scene):
    """Animated sine wave using ValueTracker."""

    def construct(self):
        # Phase tracker
        phase = ValueTracker(0)

        # Axes
        axes = Axes(
            x_range=[0, 2 * PI, PI / 2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=4,
        )

        # Sine wave that updates with phase
        sine_wave = always_redraw(
            lambda: axes.plot(
                lambda x: np.sin(x + phase.get_value()),
                color=BLUE,
                x_range=[0, 2 * PI]
            )
        )

        # Dot that follows the wave
        dot = always_redraw(
            lambda: Dot(color=RED).move_to(
                axes.c2p(PI, np.sin(PI + phase.get_value()))
            )
        )

        self.add(axes, sine_wave, dot)

        # Animate phase change (wave shifts)
        self.play(
            phase.animate.set_value(2 * PI),
            run_time=4,
            rate_func=linear
        )


class ArrowUpdater(Scene):
    """Arrow that always points from one object to another."""

    def construct(self):
        # Two dots
        dot1 = Dot(color=BLUE, radius=0.2).shift(LEFT * 2)
        dot2 = Dot(color=RED, radius=0.2).shift(RIGHT * 2)

        # Arrow that always connects them
        arrow = always_redraw(
            lambda: Arrow(
                dot1.get_center(),
                dot2.get_center(),
                buff=0.3,
                color=YELLOW
            )
        )

        # Distance label
        distance = always_redraw(
            lambda: DecimalNumber(
                np.linalg.norm(dot2.get_center() - dot1.get_center()),
                num_decimal_places=2,
                font_size=36
            ).next_to(arrow, UP)
        )

        self.add(dot1, dot2, arrow, distance)

        # Move dots around
        self.play(dot1.animate.shift(UP * 2), run_time=1.5)
        self.play(dot2.animate.shift(DOWN + LEFT * 2), run_time=1.5)
        self.play(
            dot1.animate.shift(RIGHT * 3),
            dot2.animate.shift(UP * 2),
            run_time=2
        )
        self.wait()


class ParametricCurveTracer(Scene):
    """Traces a parametric curve using ValueTracker."""

    def construct(self):
        # Parameter t
        t_tracker = ValueTracker(0)

        # Parametric curve (Lissajous)
        def parametric_func(t):
            return np.array([
                2 * np.sin(2 * t),
                2 * np.sin(3 * t),
                0
            ])

        # Dot at current position
        dot = always_redraw(
            lambda: Dot(color=RED, radius=0.15).move_to(
                parametric_func(t_tracker.get_value())
            )
        )

        # Traced path
        path = TracedPath(
            dot.get_center,
            stroke_color=BLUE,
            stroke_width=2
        )

        self.add(path, dot)

        # Trace the curve
        self.play(
            t_tracker.animate.set_value(2 * PI),
            run_time=6,
            rate_func=linear
        )
        self.wait()


class MultipleTrackers(Scene):
    """Using multiple ValueTrackers together."""

    def construct(self):
        # Separate trackers for x and y
        x_tracker = ValueTracker(0)
        y_tracker = ValueTracker(0)

        # Dot controlled by both trackers
        dot = always_redraw(
            lambda: Dot(color=RED, radius=0.2).move_to(
                RIGHT * x_tracker.get_value() + UP * y_tracker.get_value()
            )
        )

        # Coordinate display
        coords = always_redraw(
            lambda: MathTex(
                f"({x_tracker.get_value():.1f}, {y_tracker.get_value():.1f})"
            ).to_corner(UL)
        )

        self.add(dot, coords)

        # Animate both trackers
        self.play(x_tracker.animate.set_value(3), run_time=1.5)
        self.play(y_tracker.animate.set_value(2), run_time=1.5)
        self.play(
            x_tracker.animate.set_value(-2),
            y_tracker.animate.set_value(-1),
            run_time=2
        )
        self.wait()


class SpringMassSimulation(Scene):
    """Simple physics simulation with updaters."""

    def construct(self):
        # Physics parameters
        k = 10  # Spring constant
        mass = 1
        damping = 0.5

        # State trackers
        position = ValueTracker(2)  # Initial displacement
        velocity = ValueTracker(0)

        # Ground line
        ground = Line(LEFT * 4, RIGHT * 4, color=WHITE).shift(DOWN * 2)

        # Mass (square)
        mass_obj = always_redraw(
            lambda: Square(
                side_length=0.8,
                color=BLUE,
                fill_opacity=0.8
            ).move_to(UP * position.get_value())
        )

        # Spring (simplified as line)
        spring = always_redraw(
            lambda: Line(
                ground.get_center() + UP * 0.1,
                mass_obj.get_bottom(),
                color=GREY
            )
        )

        self.add(ground, spring, mass_obj)

        # Physics update function
        def physics_update(mob, dt):
            x = position.get_value()
            v = velocity.get_value()

            # F = -kx - damping*v
            acceleration = (-k * x - damping * v) / mass
            new_v = v + acceleration * dt
            new_x = x + new_v * dt

            velocity.set_value(new_v)
            position.set_value(new_x)

        # Add physics updater to a dummy mobject
        physics_driver = Mobject()
        physics_driver.add_updater(physics_update)
        self.add(physics_driver)

        # Let it run
        self.wait(5)

        # Clean up
        physics_driver.clear_updaters()
        self.wait()
