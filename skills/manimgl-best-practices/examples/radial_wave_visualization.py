"""
Radial Wave Visualization

A beautiful visualization of a radial wave emanating from a point source,
demonstrating wave propagation and decay. Based on 3Blue1Brown's hologram/diffraction
visualizations.

Run: manimgl radial_wave_visualization.py RadialWaveDemo -w
"""
from manimlib import *
import numpy as np


class RadialWaveDemo(Scene):
    """
    Demonstrates a radial wave visualization using procedural graphics.
    Shows how waves propagate from a point source with decay.
    """

    def construct(self):
        # Setup
        frame = self.camera.frame
        frame.reorient(0, 0, 0)

        # Create point source
        source_point = Dot(ORIGIN, color=WHITE, radius=0.15)
        source_glow = VGroup(
            Circle(radius=r, stroke_color=WHITE, stroke_opacity=0.5 - 0.1 * r, stroke_width=2)
            for r in [0.2, 0.3, 0.4, 0.5]
        )
        source = VGroup(source_point, source_glow)

        # Wave parameters
        wave_number = 2.0
        frequency = 0.5
        decay_factor = 0.3
        max_radius = 8.0

        # Create concentric wave rings that expand
        def get_wave_rings(time):
            rings = VGroup()
            for phase_offset in np.arange(0, 8, 0.5):
                radius = (time * frequency / wave_number + phase_offset) % (max_radius + 1)
                if radius > 0.1 and radius < max_radius:
                    amplitude = np.exp(-decay_factor * radius)
                    ring = Circle(radius=radius)
                    ring.set_stroke(
                        color=BLUE,
                        width=2 + 3 * amplitude,
                        opacity=0.8 * amplitude
                    )
                    rings.add(ring)
            return rings

        # Initial state
        time_tracker = ValueTracker(0)
        wave_rings = always_redraw(lambda: get_wave_rings(time_tracker.get_value()))

        # Add title
        title = Text("Radial Wave Propagation", font_size=48)
        title.to_edge(UP)
        title.set_backstroke(BLACK, 5)

        self.add(title)
        self.add(source)
        self.add(wave_rings)

        # Animate wave propagation
        self.play(
            time_tracker.animate.set_value(20),
            run_time=10,
            rate_func=linear
        )

        # Show label for decay
        decay_label = Text("Amplitude decays with distance", font_size=32)
        decay_label.next_to(title, DOWN)
        decay_label.set_backstroke(BLACK, 3)

        self.play(Write(decay_label))
        self.play(
            time_tracker.animate.set_value(35),
            run_time=8,
            rate_func=linear
        )
        self.wait()


class WaveInterferencePattern(Scene):
    """
    Shows interference pattern from two point sources.
    Demonstrates constructive and destructive interference.
    """

    def construct(self):
        frame = self.camera.frame

        # Two source points
        separation = 3.0
        source1_pos = separation / 2 * LEFT
        source2_pos = separation / 2 * RIGHT

        source1 = Dot(source1_pos, color=RED, radius=0.15)
        source2 = Dot(source2_pos, color=BLUE, radius=0.15)

        # Wave parameters
        wave_number = 1.5
        frequency = 0.5
        max_radius = 10.0

        # Create wave function that shows interference
        def get_interference_field(time):
            # Create a grid of points
            x_range = np.linspace(-7, 7, 70)
            y_range = np.linspace(-4, 4, 40)
            dots = VGroup()

            for x in x_range:
                for y in y_range:
                    point = np.array([x, y, 0])
                    r1 = np.linalg.norm(point - source1_pos)
                    r2 = np.linalg.norm(point - source2_pos)

                    # Wave from source 1
                    phase1 = TAU * (wave_number * r1 - frequency * time)
                    amp1 = np.cos(phase1) / (1 + 0.3 * r1)

                    # Wave from source 2
                    phase2 = TAU * (wave_number * r2 - frequency * time)
                    amp2 = np.cos(phase2) / (1 + 0.3 * r2)

                    # Combined amplitude
                    total_amp = (amp1 + amp2) / 2

                    # Color based on amplitude
                    if total_amp > 0:
                        color = interpolate_color(BLACK, BLUE, min(total_amp, 1))
                    else:
                        color = interpolate_color(BLACK, RED, min(-total_amp, 1))

                    dot = Dot(point, radius=0.05, color=color)
                    dot.set_fill(opacity=0.3 + 0.7 * abs(total_amp))
                    dots.add(dot)

            return dots

        time_tracker = ValueTracker(0)
        field = always_redraw(lambda: get_interference_field(time_tracker.get_value()))

        # Title
        title = Text("Two-Source Interference", font_size=48)
        title.to_edge(UP)
        title.set_backstroke(BLACK, 5)

        # Labels for sources
        label1 = Text("Source 1", font_size=24, color=RED)
        label1.next_to(source1, DOWN)
        label2 = Text("Source 2", font_size=24, color=BLUE)
        label2.next_to(source2, DOWN)

        self.add(title)
        self.add(field)
        self.add(source1, source2)
        self.add(label1, label2)

        # Animate
        self.play(
            time_tracker.animate.set_value(12),
            run_time=12,
            rate_func=linear
        )

        # Show constructive/destructive labels
        constructive = Text("Constructive (bright)", font_size=28, color=BLUE)
        destructive = Text("Destructive (dark)", font_size=28, color=RED)
        labels = VGroup(constructive, destructive)
        labels.arrange(DOWN, buff=0.5)
        labels.to_edge(LEFT)
        labels.set_backstroke(BLACK, 3)

        self.play(Write(labels))
        self.play(
            time_tracker.animate.set_value(20),
            run_time=8,
            rate_func=linear
        )
        self.wait()


class WavePropagation3D(Scene):
    """
    3D visualization of wave propagation from a point source.
    Shows the wave as expanding spherical shells.
    """

    def construct(self):
        frame = self.camera.frame
        frame.reorient(30, 70, 0)

        # Parameters
        wave_number = 1.0
        frequency = 0.4
        max_radius = 6.0

        # Source point
        source = Sphere(radius=0.15, color=WHITE)
        source.move_to(ORIGIN)

        # Create expanding wave shells
        def get_wave_shells(time):
            shells = Group()
            for phase_offset in np.arange(0, 10, 1.0 / wave_number):
                radius = (time * frequency / wave_number + phase_offset)
                if 0.3 < radius < max_radius:
                    amplitude = np.exp(-0.2 * radius)
                    shell = Sphere(radius=radius)
                    shell.set_color(BLUE)
                    shell.set_opacity(0.15 * amplitude)
                    shells.add(shell)
            return shells

        time_tracker = ValueTracker(0)
        shells = always_redraw(lambda: get_wave_shells(time_tracker.get_value()))

        # Add axes for reference
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-5, 5, 1],
        )
        axes.set_opacity(0.3)

        self.add(axes)
        self.add(shells)
        self.add(source)

        # Animate with camera rotation
        self.play(
            time_tracker.animate.set_value(15),
            frame.animate.increment_theta(60 * DEGREES),
            run_time=15,
            rate_func=linear
        )

        self.play(
            time_tracker.animate.set_value(25),
            frame.animate.increment_theta(30 * DEGREES).set_phi(50 * DEGREES),
            run_time=10,
            rate_func=linear
        )
        self.wait()
