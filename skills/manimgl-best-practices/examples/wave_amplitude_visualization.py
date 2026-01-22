"""
Wave Amplitude and Phase Visualization

Demonstrates various ways to visualize electromagnetic waves,
including vector field representations and amplitude graphs.

Based on 3Blue1Brown's wave visualization techniques.

Run: manimgl wave_amplitude_visualization.py WaveAmplitudeDemo -w
"""
from manimlib import *
import numpy as np


class WaveAmplitudeDemo(Scene):
    """
    Shows wave amplitude with oscillating vectors along a propagation line.
    """

    def construct(self):
        frame = self.camera.frame

        # Title
        title = Text("Wave Amplitude Visualization", font_size=42)
        title.to_edge(UP)
        title.set_backstroke(BLACK, 5)
        self.add(title)

        # Wave parameters
        wave_number = 1.5
        frequency = 0.5
        amplitude = 1.0

        # Create a line of points along which the wave propagates
        n_points = 40
        x_range = np.linspace(-6, 6, n_points)

        # Wave function
        def wave_value(x, time):
            return amplitude * np.sin(TAU * (wave_number * x - frequency * time))

        # Create oscillating vectors
        def get_wave_vectors(time):
            vectors = VGroup()
            for x in x_range:
                y_val = wave_value(x, time)

                # Create vector from baseline
                start = np.array([x, -2, 0])
                end = np.array([x, -2 + y_val, 0])

                vec = Arrow(start, end, buff=0, stroke_width=2, max_tip_length_to_length_ratio=0.15)

                # Color based on displacement
                if y_val > 0:
                    vec.set_color(interpolate_color(WHITE, BLUE, min(y_val / amplitude, 1)))
                else:
                    vec.set_color(interpolate_color(WHITE, RED, min(-y_val / amplitude, 1)))

                vectors.add(vec)
            return vectors

        # Create wave curve
        def get_wave_curve(time):
            curve = FunctionGraph(
                lambda x: -2 + wave_value(x, time),
                x_range=[-6, 6, 0.1],
                color=TEAL
            )
            curve.set_stroke(width=3)
            return curve

        time_tracker = ValueTracker(0)
        vectors = always_redraw(lambda: get_wave_vectors(time_tracker.get_value()))
        curve = always_redraw(lambda: get_wave_curve(time_tracker.get_value()))

        # Baseline
        baseline = Line([-6, -2, 0], [6, -2, 0])
        baseline.set_stroke(WHITE, 1, opacity=0.5)

        # Labels
        wavelength_brace = Brace(
            Line([-2, -2 - 1.2, 0], [-2 + 1/wave_number, -2 - 1.2, 0]),
            DOWN
        )
        lambda_label = Tex(R"\lambda", font_size=36)
        lambda_label.next_to(wavelength_brace, DOWN)

        amp_line = VGroup(
            Arrow([-6.5, -2, 0], [-6.5, -2 + amplitude, 0], buff=0),
            Arrow([-6.5, -2 + amplitude, 0], [-6.5, -2, 0], buff=0),
        )
        amp_line.set_color(YELLOW)
        amp_label = Text("Amplitude", font_size=20, color=YELLOW)
        amp_label.next_to(amp_line, LEFT)

        self.add(baseline)
        self.add(vectors)
        self.add(curve)

        # Animate wave motion
        self.play(
            time_tracker.animate.set_value(8),
            run_time=8,
            rate_func=linear
        )

        # Add labels
        self.add(amp_line, amp_label)
        self.play(
            time_tracker.animate.set_value(12),
            FadeIn(wavelength_brace),
            FadeIn(lambda_label),
            run_time=4,
            rate_func=linear
        )
        self.wait()


class PhaseVisualization(Scene):
    """
    Visualizes the phase of a wave using rotating phasors.
    """

    def construct(self):
        # Title
        title = Text("Wave Phase as Rotating Phasor", font_size=42)
        title.to_edge(UP)
        title.set_backstroke(BLACK, 5)
        self.add(title)

        # Parameters
        frequency = 0.3

        # Phasor circle
        circle = Circle(radius=1.5, color=GREY)
        circle.move_to(LEFT * 3)

        circle_center = circle.get_center()

        # Phasor arrow
        def get_phasor(time):
            angle = TAU * frequency * time
            end_point = circle_center + 1.5 * np.array([np.cos(angle), np.sin(angle), 0])
            arrow = Arrow(circle_center, end_point, buff=0, color=BLUE)
            return arrow

        # Projection on vertical axis (wave value)
        def get_projection_line(time):
            angle = TAU * frequency * time
            y_val = 1.5 * np.sin(angle)
            line = DashedLine(
                circle_center + 1.5 * np.array([np.cos(angle), np.sin(angle), 0]),
                circle_center + np.array([0, y_val, 0]),
                dash_length=0.1
            )
            line.set_stroke(YELLOW, 2)
            return line

        # Wave trace
        def get_wave_trace(time, length=8):
            wave = VGroup()
            x_start = 0
            for i in range(int(length * 30)):
                x = x_start + i / 30
                t = time - (x - x_start) / 2
                y = 1.5 * np.sin(TAU * frequency * t)
                dot = Dot([x, y, 0], radius=0.02, color=TEAL)
                wave.add(dot)
            return wave

        time_tracker = ValueTracker(0)
        phasor = always_redraw(lambda: get_phasor(time_tracker.get_value()))
        projection = always_redraw(lambda: get_projection_line(time_tracker.get_value()))
        wave_trace = always_redraw(lambda: get_wave_trace(time_tracker.get_value()))

        # Center dot
        center_dot = Dot(circle_center, color=WHITE, radius=0.08)

        # Phase angle arc
        def get_phase_arc(time):
            angle = TAU * frequency * time % TAU
            if angle > 0.1:
                arc = Arc(0, angle, radius=0.5, arc_center=circle_center)
                arc.set_stroke(GREEN, 2)
                return arc
            return VGroup()

        phase_arc = always_redraw(lambda: get_phase_arc(time_tracker.get_value()))

        # Labels
        phasor_label = Text("Phasor", font_size=24)
        phasor_label.next_to(circle, DOWN)

        wave_label = Text("Wave amplitude = vertical projection", font_size=24)
        wave_label.to_edge(DOWN)

        self.add(circle, center_dot)
        self.add(phasor)
        self.add(projection)
        self.add(phase_arc)
        self.add(wave_trace)
        self.add(phasor_label, wave_label)

        # Animate
        self.play(
            time_tracker.animate.set_value(15),
            run_time=15,
            rate_func=linear
        )
        self.wait()


class TwoWaveSuperposition(Scene):
    """
    Shows superposition of two waves with different phases.
    """

    def construct(self):
        # Title
        title = Text("Wave Superposition", font_size=42)
        title.to_edge(UP)
        title.set_backstroke(BLACK, 5)
        self.add(title)

        # Parameters
        wave_number = 1.0
        frequency = 0.4
        amplitude = 0.8

        # Phase difference
        phase_diff_tracker = ValueTracker(0)

        # Wave functions
        def wave1_value(x, time):
            return amplitude * np.sin(TAU * (wave_number * x - frequency * time))

        def wave2_value(x, time, phase_diff):
            return amplitude * np.sin(TAU * (wave_number * x - frequency * time) + phase_diff)

        def combined_value(x, time, phase_diff):
            return wave1_value(x, time) + wave2_value(x, time, phase_diff)

        # Wave curves
        def get_wave1(time):
            curve = FunctionGraph(
                lambda x: 2 + wave1_value(x, time),
                x_range=[-6, 6, 0.1],
                color=RED
            )
            curve.set_stroke(width=2)
            return curve

        def get_wave2(time, phase_diff):
            curve = FunctionGraph(
                lambda x: wave2_value(x, time, phase_diff),
                x_range=[-6, 6, 0.1],
                color=BLUE
            )
            curve.set_stroke(width=2)
            return curve

        def get_combined(time, phase_diff):
            curve = FunctionGraph(
                lambda x: -2 + combined_value(x, time, phase_diff),
                x_range=[-6, 6, 0.1],
                color=GREEN
            )
            curve.set_stroke(width=3)
            return curve

        time_tracker = ValueTracker(0)

        wave1 = always_redraw(lambda: get_wave1(time_tracker.get_value()))
        wave2 = always_redraw(lambda: get_wave2(time_tracker.get_value(),
                                                 phase_diff_tracker.get_value()))
        combined = always_redraw(lambda: get_combined(time_tracker.get_value(),
                                                       phase_diff_tracker.get_value()))

        # Baselines
        baseline1 = Line([-6, 2, 0], [6, 2, 0]).set_stroke(WHITE, 1, opacity=0.3)
        baseline2 = Line([-6, 0, 0], [6, 0, 0]).set_stroke(WHITE, 1, opacity=0.3)
        baseline3 = Line([-6, -2, 0], [6, -2, 0]).set_stroke(WHITE, 1, opacity=0.3)

        # Labels
        label1 = Text("Wave 1", font_size=24, color=RED).to_corner(UL).shift(DOWN)
        label2 = Text("Wave 2", font_size=24, color=BLUE).next_to(label1, DOWN)
        label_sum = Text("Sum", font_size=24, color=GREEN).next_to(label2, DOWN)

        # Phase difference display
        phase_display = always_redraw(lambda: Text(
            f"Phase diff: {phase_diff_tracker.get_value() / PI:.2f}π",
            font_size=28
        ).to_corner(DR))

        self.add(baseline1, baseline2, baseline3)
        self.add(wave1, wave2, combined)
        self.add(label1, label2, label_sum)
        self.add(phase_display)

        # Show in-phase waves
        self.play(
            time_tracker.animate.set_value(6),
            run_time=6,
            rate_func=linear
        )

        # Transition to out-of-phase
        in_phase_label = Text("In phase: Constructive", font_size=28, color=GREEN)
        in_phase_label.to_edge(DOWN)
        self.play(Write(in_phase_label))

        self.play(
            phase_diff_tracker.animate.set_value(PI),
            time_tracker.animate.set_value(12),
            run_time=6,
            rate_func=linear
        )

        out_phase_label = Text("Out of phase: Destructive", font_size=28, color=PINK)
        out_phase_label.next_to(in_phase_label, UP)
        self.play(
            Write(out_phase_label),
            time_tracker.animate.set_value(18),
            run_time=6,
            rate_func=linear
        )
        self.wait()


class StandingWave(Scene):
    """
    Visualization of a standing wave from two counter-propagating waves.
    """

    def construct(self):
        # Title
        title = Text("Standing Wave", font_size=42)
        title.to_edge(UP)
        title.set_backstroke(BLACK, 5)
        self.add(title)

        # Parameters
        wave_number = 2.0
        frequency = 0.5
        amplitude = 1.2

        # Standing wave = 2A * sin(kx) * cos(wt)
        def standing_wave_value(x, time):
            return 2 * amplitude * np.sin(TAU * wave_number * x) * np.cos(TAU * frequency * time)

        # Envelope
        def envelope_upper(x):
            return 2 * amplitude * abs(np.sin(TAU * wave_number * x))

        def envelope_lower(x):
            return -2 * amplitude * abs(np.sin(TAU * wave_number * x))

        # Create wave and envelopes
        def get_standing_wave(time):
            curve = FunctionGraph(
                lambda x: standing_wave_value(x, time),
                x_range=[-5, 5, 0.1],
                color=TEAL
            )
            curve.set_stroke(width=3)
            return curve

        upper_env = FunctionGraph(envelope_upper, x_range=[-5, 5, 0.1], color=YELLOW)
        lower_env = FunctionGraph(envelope_lower, x_range=[-5, 5, 0.1], color=YELLOW)
        upper_env.set_stroke(width=1, opacity=0.5)
        lower_env.set_stroke(width=1, opacity=0.5)

        time_tracker = ValueTracker(0)
        wave = always_redraw(lambda: get_standing_wave(time_tracker.get_value()))

        # Baseline
        baseline = Line([-5, 0, 0], [5, 0, 0]).set_stroke(WHITE, 1, opacity=0.3)

        # Node and antinode markers
        nodes = VGroup()
        antinodes = VGroup()
        for i in range(-4, 5):
            x = i / (2 * wave_number)
            if i % 2 == 0:
                node = Dot([x, 0, 0], color=RED, radius=0.08)
                nodes.add(node)
            else:
                antinode = Dot([x, 0, 0], color=GREEN, radius=0.08)
                antinodes.add(antinode)

        # Labels
        node_label = Text("Nodes (no motion)", font_size=24, color=RED)
        node_label.to_corner(DL)
        antinode_label = Text("Antinodes (max motion)", font_size=24, color=GREEN)
        antinode_label.next_to(node_label, UP)

        self.add(baseline)
        self.add(upper_env, lower_env)
        self.add(wave)
        self.add(nodes, antinodes)
        self.add(node_label, antinode_label)

        # Animate
        self.play(
            time_tracker.animate.set_value(15),
            run_time=15,
            rate_func=linear
        )
        self.wait()
