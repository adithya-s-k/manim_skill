"""
Light Polarization and Quantum States
=====================================
Visualizes polarized light as a 3D electromagnetic wave, showing
how polarization states map to quantum states on a 2D plane.

Key concepts demonstrated:
- TimeVaryingVectorField for oscillating wave visualization
- 3D camera control with reorient
- Prism and ParametricSurface for 3D objects
- ValueTracker for controlling wave polarization angle
"""
from manimlib import *


class PolarizedLightWave(InteractiveScene):
    """Visualizes polarized light as an electromagnetic wave."""

    def construct(self):
        frame = self.frame

        # Set up 3D view
        frame.reorient(-60, 75, 0)
        frame.add_ambient_rotation(DEG)

        # Create axes
        axes = ThreeDAxes((-1, 10), (-1, 1), (-1, 1))
        axes.set_stroke(WHITE, 1, 0.5)
        self.add(axes)

        # Polarization angle tracker
        theta_tracker = ValueTracker(45 * DEG)

        # Wave parameters
        wave_number = 1.5
        frequency = 0.5
        amplitude = 0.5

        # Create the wave as a VGroup of vectors that update over time
        # Note: TimeVaryingVectorField doesn't work directly with ThreeDAxes
        sample_x = np.arange(0, 8, 0.15)

        def get_wave_vectors(time=0):
            """Generate wave vectors at given time."""
            vectors = VGroup()
            theta = theta_tracker.get_value()
            for x in sample_x:
                phase = wave_number * x - TAU * frequency * time
                magnitude = amplitude * np.cos(phase)
                y_comp = np.cos(theta) * magnitude
                z_comp = np.sin(theta) * magnitude

                start = axes.c2p(x, 0, 0)
                end = axes.c2p(x, y_comp, z_comp)
                vec = Arrow(start, end, buff=0, thickness=2)
                vec.set_color(BLUE)
                vec.set_stroke(opacity=0.7)
                vectors.add(vec)
            return vectors

        wave = get_wave_vectors()

        # Add an updater to animate the wave
        time_tracker = ValueTracker(0)

        def update_wave(w):
            new_wave = get_wave_vectors(time_tracker.get_value())
            w.become(new_wave)

        wave.add_updater(update_wave)

        # Add a beam line
        beam = Line(ORIGIN, 8 * RIGHT)
        beam.set_stroke(GREEN, 2)

        self.add(beam)
        self.play(FadeIn(wave))

        # Animate the wave for a few seconds
        self.play(time_tracker.animate.set_value(3), run_time=3, rate_func=linear)
        wave.clear_updaters()  # Stop wave animation to change polarization

        # Add polarization plane indicator
        plane_indicator = Square(1.5)
        plane_indicator.rotate(90 * DEG, RIGHT)
        plane_indicator.rotate(theta_tracker.get_value(), RIGHT)
        plane_indicator.move_to(4 * RIGHT)
        plane_indicator.set_fill(BLUE, 0.2)
        plane_indicator.set_stroke(BLUE, 1)

        def update_plane(plane):
            plane.rotate(
                theta_tracker.get_value() - plane.get_angle(),
                axis=RIGHT,
                about_point=plane.get_center()
            )

        self.play(FadeIn(plane_indicator))
        self.wait(2)

        # Change polarization angle
        self.play(
            theta_tracker.animate.set_value(0),
            run_time=3
        )
        self.wait(2)

        self.play(
            theta_tracker.animate.set_value(90 * DEG),
            run_time=3
        )
        self.wait(2)

        self.play(
            theta_tracker.animate.set_value(45 * DEG),
            run_time=2
        )
        self.wait(3)


class PolarizationTo2DState(InteractiveScene):
    """Shows how polarization maps to a 2D state vector."""

    def construct(self):
        frame = self.frame

        # Title
        title = Text("Polarization as Quantum State", font_size=48)
        title.to_edge(UP)
        self.add(title)

        # Left side: 3D polarization representation
        axes_3d = ThreeDAxes((-1, 1), (-1, 1), (-1, 1))
        axes_3d.scale(1.5)
        axes_3d.shift(3 * LEFT)

        # Polarization vector (in yz plane at x=0)
        theta_tracker = ValueTracker(45 * DEG)

        def get_pol_vector():
            theta = theta_tracker.get_value()
            return Arrow(
                axes_3d.c2p(0, 0, 0),
                axes_3d.c2p(0, np.cos(theta), np.sin(theta)),
                buff=0,
                thickness=5,
                fill_color=BLUE
            )

        pol_vector = always_redraw(get_pol_vector)

        # Circle showing all possible polarizations
        pol_circle = Circle(radius=1.5)
        pol_circle.rotate(90 * DEG, UP)
        pol_circle.move_to(axes_3d.c2p(0, 0, 0))
        pol_circle.set_stroke(GREY, 1, 0.5)

        # Labels
        h_label = Tex("H", font_size=30, color=YELLOW)
        h_label.rotate(90 * DEG, RIGHT)
        h_label.next_to(axes_3d.c2p(0, 1, 0), UP + OUT, SMALL_BUFF)

        v_label = Tex("V", font_size=30, color=GREEN)
        v_label.rotate(90 * DEG, RIGHT)
        v_label.next_to(axes_3d.c2p(0, 0, 1), OUT, SMALL_BUFF)

        frame.reorient(-30, 70, 0, ORIGIN, 8)

        self.add(axes_3d, pol_circle, pol_vector, h_label, v_label)

        # Right side: 2D qubit representation
        plane = NumberPlane((-2, 2), (-2, 2), faded_line_ratio=5)
        plane.set_height(4)
        plane.shift(3 * RIGHT)

        zero_label = Tex(R"|H\rangle", font_size=30, color=YELLOW)
        zero_label.next_to(plane.c2p(1, 0), DR, SMALL_BUFF)

        one_label = Tex(R"|V\rangle", font_size=30, color=GREEN)
        one_label.next_to(plane.c2p(0, 1), UL, SMALL_BUFF)

        def get_state_vector():
            theta = theta_tracker.get_value()
            return Arrow(
                plane.c2p(0, 0),
                plane.c2p(np.cos(theta), np.sin(theta)),
                buff=0,
                thickness=4,
                fill_color=TEAL
            )

        state_vector = always_redraw(get_state_vector)

        # Unit circle on 2D plane
        unit_circle = Circle(radius=plane.c2p(1, 0)[0] - plane.c2p(0, 0)[0])
        unit_circle.move_to(plane.c2p(0, 0))
        unit_circle.set_stroke(GREY, 1, 0.5)

        self.add(plane, unit_circle, state_vector, zero_label, one_label)

        # Arrow connecting the two representations
        connection = Tex(R"\Leftrightarrow", font_size=72)
        connection.move_to(ORIGIN)

        self.play(Write(connection))
        self.wait()

        # Animate through different polarizations
        for target_angle in [0, 90 * DEG, 30 * DEG, 60 * DEG, 45 * DEG]:
            self.play(theta_tracker.animate.set_value(target_angle), run_time=2)
            self.wait()

        self.wait(2)


class BeamSplitterSimple(InteractiveScene):
    """Simplified beam splitter demonstration."""

    def construct(self):
        frame = self.frame

        # Set up 3D view
        frame.reorient(-70, 70, 0)

        # Create the beam splitter cube
        splitter = Cube()
        splitter.set_color(WHITE)
        splitter.set_opacity(0.3)
        splitter.rotate(45 * DEG)
        splitter.set_height(1)
        splitter.move_to(ORIGIN)

        # Input beam
        input_beam = Line(4 * LEFT, ORIGIN)
        input_beam.set_stroke(GREEN, 3)

        # Output beams
        output_h = Line(ORIGIN, 4 * RIGHT)
        output_h.set_stroke(YELLOW, 3)

        output_v = Line(ORIGIN, 4 * UP)
        output_v.set_stroke(BLUE, 3)

        # Labels
        input_label = Tex(R"|\psi\rangle", font_size=36)
        input_label.next_to(input_beam, UP)
        input_label.rotate(90 * DEG, RIGHT)

        h_label = Tex(R"|H\rangle", font_size=36, color=YELLOW)
        h_label.next_to(output_h.get_end(), DOWN)
        h_label.rotate(90 * DEG, RIGHT)

        v_label = Tex(R"|V\rangle", font_size=36, color=BLUE)
        v_label.next_to(output_v.get_end(), RIGHT)
        v_label.rotate(90 * DEG, RIGHT)

        self.add(splitter)
        self.play(ShowCreation(input_beam), FadeIn(input_label))
        self.wait()

        # Split the beam
        self.play(
            ShowCreation(output_h),
            ShowCreation(output_v),
            FadeIn(h_label),
            FadeIn(v_label),
        )
        self.wait()

        # Add probability labels
        cos_label = Tex(R"\cos(\theta)", font_size=24, color=YELLOW)
        cos_label.next_to(output_h, DOWN, SMALL_BUFF)
        cos_label.rotate(90 * DEG, RIGHT)

        sin_label = Tex(R"\sin(\theta)", font_size=24, color=BLUE)
        sin_label.next_to(output_v, LEFT, SMALL_BUFF)
        sin_label.rotate(90 * DEG, RIGHT)

        self.play(
            FadeIn(cos_label),
            FadeIn(sin_label)
        )

        # Animate the camera
        self.play(
            frame.animate.reorient(-30, 60, 0),
            run_time=4
        )
        self.wait(2)


class WaveVectorComponents(InteractiveScene):
    """Shows decomposition of polarization into H and V components."""

    def construct(self):
        # 2D plane view
        plane = NumberPlane((-2, 2), (-2, 2), faded_line_ratio=5)
        plane.set_height(6)

        # Labels
        h_label = Tex(R"|H\rangle", color=YELLOW)
        h_label.next_to(plane.c2p(1.2, 0), DR, SMALL_BUFF)

        v_label = Tex(R"|V\rangle", color=BLUE)
        v_label.next_to(plane.c2p(0, 1.2), UL, SMALL_BUFF)

        self.add(plane, h_label, v_label)

        # Main polarization vector
        theta = 50 * DEG
        main_vec = Arrow(
            plane.c2p(0, 0),
            plane.c2p(np.cos(theta), np.sin(theta)),
            buff=0,
            thickness=5,
            fill_color=TEAL
        )

        # Component vectors
        h_component = Arrow(
            plane.c2p(0, 0),
            plane.c2p(np.cos(theta), 0),
            buff=0,
            thickness=3,
            fill_color=YELLOW
        )

        v_component = Arrow(
            plane.c2p(np.cos(theta), 0),
            plane.c2p(np.cos(theta), np.sin(theta)),
            buff=0,
            thickness=3,
            fill_color=BLUE
        )

        # Dashed lines for projection
        h_dashed = DashedLine(
            plane.c2p(np.cos(theta), np.sin(theta)),
            plane.c2p(np.cos(theta), 0)
        )
        h_dashed.set_stroke(YELLOW, 1)

        v_dashed = DashedLine(
            plane.c2p(np.cos(theta), np.sin(theta)),
            plane.c2p(0, np.sin(theta))
        )
        v_dashed.set_stroke(BLUE, 1)

        self.play(GrowArrow(main_vec))
        self.wait()

        # Show decomposition
        self.play(
            ShowCreation(h_dashed),
            ShowCreation(v_dashed),
        )
        self.play(
            GrowArrow(h_component),
            GrowArrow(v_component),
        )

        # Equation
        equation = Tex(
            R"|\psi\rangle = \cos(\theta)|H\rangle + \sin(\theta)|V\rangle",
            font_size=36
        )
        equation.to_edge(DOWN, buff=1.0)

        self.play(Write(equation))
        self.wait()

        # Show angle
        arc = Arc(0, theta, radius=0.5)
        arc.move_to(plane.c2p(0, 0), LEFT + DOWN)
        arc.set_stroke(WHITE, 2)

        theta_label = Tex(R"\theta", font_size=36)
        theta_label.next_to(arc.pfp(0.5), RIGHT, SMALL_BUFF)

        self.play(
            ShowCreation(arc),
            Write(theta_label)
        )
        self.wait(2)


if __name__ == "__main__":
    # To run: manimgl light_polarization.py PolarizedLightWave
    pass
