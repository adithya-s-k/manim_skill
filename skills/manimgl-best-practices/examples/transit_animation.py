"""
Transit Animation

Simple but elegant animations showing objects crossing
in front of others. Useful for astronomical transits,
loading animations, or timing demonstrations.

Run: manimgl transit_animation.py TransitOfVenus -w
Preview: manimgl transit_animation.py TransitOfVenus -p

Source: Adapted from 3b1b's cosmic_distance video (2025)
"""
from manimlib import *


class TransitOfVenus(InteractiveScene):
    """
    Venus (small dot) transiting across the Sun.
    Shows how astronomers measured distances historically.
    """

    def construct(self):
        # Create the Sun (large yellow circle)
        sun = Circle(radius=2.5)
        sun.set_fill(YELLOW, opacity=0.8)
        sun.set_stroke(ORANGE, width=3)

        # Add some texture with a glow
        sun_glow = Circle(radius=2.7)
        sun_glow.set_fill(YELLOW, opacity=0.2)
        sun_glow.set_stroke(width=0)

        self.add(sun_glow, sun)

        # Path for Venus transit
        path = Line(3 * LEFT, 3 * RIGHT)
        path.set_y(-0.5)  # Slightly below center

        # Venus as small black dot
        venus = Dot(radius=0.08, color=BLACK)
        venus.move_to(path.get_start())
        venus.set_fill(BLACK, opacity=1)

        self.add(venus)

        # Show transit with periodic snapshots
        velocity = 0.3
        venus.add_updater(lambda m, dt: m.shift(dt * velocity * RIGHT))

        # Collect snapshots
        copies = VGroup()
        self.add(copies)

        wait_time = 0.8
        n_snapshots = int(path.get_length() / velocity / wait_time)

        for _ in range(n_snapshots):
            self.wait(wait_time)
            copy = venus.copy().clear_updaters()
            copy.set_fill(BLACK, opacity=0.5)
            copies.add(copy)

        # Remove venus, show path
        self.remove(venus)
        path.set_stroke(BLACK, 2)
        self.play(Transform(copies, VGroup(path)))
        self.wait()


class OrbitalTransit(InteractiveScene):
    """
    Shows a planet orbiting and periodically transiting
    in front of its star from the viewer's perspective.
    """

    def construct(self):
        # Star
        star = Circle(radius=1)
        star.set_fill(YELLOW_E, opacity=1)
        star.set_stroke(YELLOW, width=2)

        # Orbit path (ellipse viewed at an angle)
        orbit = Ellipse(width=5, height=1)
        orbit.set_stroke(WHITE, 1, opacity=0.3)

        self.add(orbit, star)

        # Planet
        planet = Dot(radius=0.15, color=BLUE)
        planet.move_to(orbit.get_right())

        # Orbit animation using angle tracker
        angle = ValueTracker(0)

        def update_planet(p):
            a = angle.get_value()
            x = 2.5 * np.cos(a)
            y = 0.5 * np.sin(a)
            p.move_to([x, y, 0])
            # Depth effect: size changes based on y position
            scale = 0.12 + 0.06 * np.sin(a)
            p.set_width(2 * scale)

        planet.add_updater(update_planet)

        self.add(planet)

        # Multiple orbits
        self.play(
            angle.animate.set_value(4 * TAU),
            run_time=12,
            rate_func=linear
        )


class LoadingDots(InteractiveScene):
    """
    Classic loading animation with dots.
    Demonstrates phase-shifted periodic motion.
    """

    def construct(self):
        # Create three dots
        n_dots = 3
        dots = VGroup(*[
            Dot(radius=0.15, color=BLUE)
            for _ in range(n_dots)
        ])
        dots.arrange(RIGHT, buff=0.5)
        dots.center()

        time = ValueTracker(0)

        # Each dot oscillates with a phase shift
        for i, dot in enumerate(dots):
            phase = i * TAU / n_dots
            original_y = dot.get_y()
            dot.add_updater(
                lambda m, o=original_y, p=phase: m.set_y(
                    o + 0.3 * np.sin(3 * time.get_value() + p)
                )
            )

        self.add(dots)

        # Animate
        time.add_updater(lambda m, dt: m.increment_value(dt))
        self.wait(5)


class WaveTransit(InteractiveScene):
    """
    A wave propagating across the screen.
    Good for demonstrating wave motion or signal propagation.
    """

    def construct(self):
        # Create axes
        axes = Axes(
            x_range=(-5, 5, 1),
            y_range=(-2, 2, 1),
            width=12,
            height=4,
        )

        self.add(axes)

        # Time tracker
        t = ValueTracker(0)

        # Wave function
        def wave(x):
            return np.sin(2 * x - 3 * t.get_value()) * np.exp(-0.1 * (x + 5 - t.get_value())**2)

        # Wave curve
        wave_curve = always_redraw(
            lambda: axes.get_graph(wave, color=BLUE, stroke_width=3)
        )

        self.add(wave_curve)

        # Propagate wave
        self.play(
            t.animate.set_value(10),
            run_time=5,
            rate_func=linear
        )
        self.wait()


class PendulumSwing(InteractiveScene):
    """
    Simple pendulum animation.
    Classic physics visualization.
    """

    def construct(self):
        # Pivot point
        pivot = Dot(ORIGIN, color=WHITE)

        # Pendulum parameters
        length = 3
        g = 10
        omega = np.sqrt(g / length)

        # Angle tracker (start displaced)
        theta = ValueTracker(PI / 4)

        # Bob
        bob = Dot(radius=0.2, color=BLUE)
        bob.add_updater(lambda m: m.move_to(
            pivot.get_center() + length * np.array([
                np.sin(theta.get_value()),
                -np.cos(theta.get_value()),
                0
            ])
        ))

        # Rod
        rod = Line(ORIGIN, DOWN)
        rod.set_stroke(WHITE, 3)
        rod.add_updater(lambda m: m.put_start_and_end_on(
            pivot.get_center(),
            bob.get_center()
        ))

        # Trail
        trail = TracedPath(
            bob.get_center,
            stroke_color=YELLOW,
            stroke_width=1,
            stroke_opacity=0.5
        )

        self.add(pivot, rod, bob, trail)

        # Simple harmonic motion approximation
        time = ValueTracker(0)
        amplitude = PI / 4

        def update_theta(m):
            t = time.get_value()
            m.set_value(amplitude * np.cos(omega * t) * np.exp(-0.05 * t))

        theta.add_updater(update_theta)
        time.add_updater(lambda m, dt: m.increment_value(dt))

        self.wait(10)
