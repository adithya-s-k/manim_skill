"""
Vector Fields and Flow Visualization

Demonstrates vector field rendering using arrows,
streamlines, and particle flow animations.

Run: manimgl vector_fields.py SimpleVectorField -w
Preview: manimgl vector_fields.py SimpleVectorField -p

Source: Inspired by 3b1b's vector field visualizations
"""
from manimlib import *
import numpy as np


class SimpleVectorField(InteractiveScene):
    """
    Basic 2D vector field visualization using arrows.
    Shows rotation field around origin.
    """

    def construct(self):
        # Create plane
        plane = NumberPlane(
            x_range=(-4, 4, 1),
            y_range=(-3, 3, 1),
            background_line_style={"stroke_opacity": 0.3}
        )
        self.add(plane)

        # Create arrows manually for vector field
        arrows = VGroup()
        for x in np.arange(-3.5, 4, 0.7):
            for y in np.arange(-2.5, 3, 0.7):
                # Rotation field: F = (-y, x)
                vx, vy = -y * 0.15, x * 0.15
                if abs(vx) < 0.01 and abs(vy) < 0.01:
                    continue

                arrow = Arrow(
                    start=[x, y, 0],
                    end=[x + vx, y + vy, 0],
                    buff=0,
                    stroke_width=2,
                    max_tip_length_to_length_ratio=0.3,
                )
                # Color by magnitude
                mag = np.sqrt(vx**2 + vy**2)
                arrow.set_color(interpolate_color(BLUE, YELLOW, mag / 0.5))
                arrows.add(arrow)

        self.play(LaggedStartMap(GrowArrow, arrows, lag_ratio=0.02, run_time=2))
        self.wait()

        # Add a particle that follows the field
        dot = Dot(color=RED, radius=0.1)
        dot.move_to(2 * RIGHT + UP)

        def follow_field(mob, dt):
            x, y = mob.get_center()[:2]
            vx, vy = -y * 0.5, x * 0.5
            mob.shift(np.array([vx, vy, 0]) * dt)

        dot.add_updater(follow_field)
        trail = TracedPath(dot.get_center, stroke_color=RED, stroke_width=2)

        self.add(trail, dot)
        self.wait(8)


class GradientFieldDemo(InteractiveScene):
    """
    Shows gradient of a scalar field.
    Arrows point toward steepest ascent.
    """

    def construct(self):
        # Create colored background showing scalar field
        plane = NumberPlane(
            x_range=(-4, 4, 1),
            y_range=(-3, 3, 1),
            background_line_style={"stroke_opacity": 0.2}
        )
        self.add(plane)

        # Scalar field: f(x,y) = -(x^2 + y^2) (peak at origin)
        # Gradient: (-2x, -2y) pointing toward origin

        # Create dots colored by height
        dots = VGroup()
        for x in np.arange(-3.5, 4, 0.3):
            for y in np.arange(-2.5, 3, 0.3):
                val = -(x**2 + y**2)
                t = (val + 25) / 25  # Normalize
                color = interpolate_color(BLUE_E, RED, t)
                dot = Dot([x, y, 0], radius=0.08, color=color)
                dots.add(dot)

        self.play(FadeIn(dots))

        # Gradient vectors (pointing toward origin = uphill)
        arrows = VGroup()
        for x in np.arange(-3, 3.5, 0.8):
            for y in np.arange(-2, 2.5, 0.8):
                if abs(x) < 0.3 and abs(y) < 0.3:
                    continue
                # Gradient direction (toward origin for this function)
                gx, gy = -2*x, -2*y
                length = np.sqrt(gx**2 + gy**2)
                # Normalize and scale
                scale = 0.3
                gx, gy = gx/length * scale, gy/length * scale

                arrow = Arrow(
                    start=[x, y, 0],
                    end=[x + gx, y + gy, 0],
                    buff=0,
                    stroke_width=2,
                    stroke_color=WHITE,
                )
                arrows.add(arrow)

        self.play(LaggedStartMap(GrowArrow, arrows, lag_ratio=0.02, run_time=2))

        # Label
        label = Tex(r"\nabla f = (-2x, -2y)", font_size=36)
        label.to_corner(UL)
        label.set_backstroke(BLACK, 3)
        self.play(Write(label))
        self.wait()


class ParticleFlow(InteractiveScene):
    """
    Multiple particles flowing through a vector field.
    Great for visualizing fluid flow.
    """

    def construct(self):
        # Vortex field visualization
        plane = NumberPlane(
            x_range=(-5, 5, 1),
            y_range=(-4, 4, 1),
            background_line_style={"stroke_opacity": 0.2}
        )
        self.add(plane)

        # Create particles
        n_particles = 15
        particles = VGroup()
        trails = VGroup()

        for i in range(n_particles):
            # Start in a circle
            angle = i * TAU / n_particles
            start_pos = 2 * np.array([np.cos(angle), np.sin(angle), 0])

            dot = Dot(start_pos, radius=0.1, color=YELLOW)

            def make_updater():
                def update(mob, dt):
                    x, y = mob.get_center()[:2]
                    r = np.sqrt(x**2 + y**2) + 0.1
                    vx, vy = -y/r, x/r
                    mob.shift(np.array([vx, vy, 0]) * dt * 0.8)
                return update

            dot.add_updater(make_updater())

            trail = TracedPath(
                dot.get_center,
                stroke_color=BLUE,
                stroke_width=1.5,
                stroke_opacity=0.7,
            )

            particles.add(dot)
            trails.add(trail)

        self.add(trails, particles)
        self.wait(10)


class ElectricDipole(InteractiveScene):
    """
    Electric field from two point charges (dipole).
    """

    def construct(self):
        # Charge positions
        q1_pos = np.array([-2, 0, 0])
        q2_pos = np.array([2, 0, 0])

        # Draw charges
        q_plus = Dot(q1_pos, radius=0.25, color=RED)
        q_plus_label = Tex("+", font_size=36, color=WHITE)
        q_plus_label.move_to(q1_pos)

        q_minus = Dot(q2_pos, radius=0.25, color=BLUE)
        q_minus_label = Tex("-", font_size=36, color=WHITE)
        q_minus_label.move_to(q2_pos)

        self.add(q_plus, q_plus_label, q_minus, q_minus_label)

        # Create field arrows
        arrows = VGroup()
        for x in np.arange(-4, 4.5, 0.6):
            for y in np.arange(-3, 3.5, 0.6):
                pos = np.array([x, y, 0])

                # Skip near charges
                if np.linalg.norm(pos - q1_pos) < 0.5:
                    continue
                if np.linalg.norm(pos - q2_pos) < 0.5:
                    continue

                # Electric field from both charges
                r1 = pos - q1_pos
                r2 = pos - q2_pos
                d1 = np.linalg.norm(r1) + 0.1
                d2 = np.linalg.norm(r2) + 0.1

                # E = kq/r^2 in direction of r (positive) or -r (negative)
                E1 = r1 / d1**3  # From positive charge
                E2 = -r2 / d2**3  # From negative charge
                E = E1 + E2

                mag = np.linalg.norm(E)
                if mag < 0.001:
                    continue

                # Normalize and scale
                E_norm = E / mag
                length = min(0.4, mag * 2)

                arrow = Arrow(
                    start=pos,
                    end=pos + E_norm * length,
                    buff=0,
                    stroke_width=2,
                )
                # Color by magnitude
                color = interpolate_color(BLUE_E, YELLOW, min(mag * 5, 1))
                arrow.set_color(color)
                arrows.add(arrow)

        self.play(LaggedStartMap(GrowArrow, arrows, lag_ratio=0.01, run_time=3))
        self.wait()
