"""
Bloch Sphere 3D Visualization
=============================
Displays a quantum state vector in 3D space with a surrounding Bloch sphere.
The vector rotates and can be observed from different angles with ambient
camera rotation.

Key concepts demonstrated:
- ThreeDAxes for 3D coordinate system
- Sphere and SurfaceMesh for Bloch sphere visualization
- frame.add_ambient_rotation for continuous camera movement
- Vector with set_perpendicular_to_camera for billboard effect
"""
from manimlib import *


class BlochSphere3D(InteractiveScene):
    """Visualize a quantum state as a vector on the Bloch sphere."""

    def construct(self):
        frame = self.frame

        # Set up 3D axes
        axes = ThreeDAxes((-1, 1), (-1, 1), (-1, 1))
        axes.scale(2.0)

        # Add a subtle reference plane
        plane = NumberPlane(
            (-1, 1 - 1e-5),
            (-1, 1 - 1e-5),
            faded_line_ratio=5
        )
        plane.scale(2.0)
        plane.background_lines.set_stroke(opacity=0.5)
        plane.faded_lines.set_stroke(opacity=0.25)
        plane.axes.set_stroke(opacity=0.25)

        # Set up camera orientation and ambient rotation
        frame.reorient(14, 76, 0)
        frame.add_ambient_rotation(3 * DEG)

        self.add(plane, axes)

        # Create the state vector
        vector = Vector(
            2 * normalize([1, 1, 2]),
            thickness=5,
            fill_color=TEAL
        )
        vector.set_fill(border_width=2)
        vector.always.set_perpendicular_to_camera(frame)

        self.play(GrowArrow(vector))
        self.wait(6)

        # Rotate the vector randomly
        for _ in range(3):
            axis = normalize(np.random.uniform(-1, 1, 3))
            angle = np.random.uniform(PI / 4, PI)
            self.play(
                Rotate(vector, angle, axis=axis, about_point=ORIGIN),
                run_time=2
            )
            self.wait()

        # Show the Bloch sphere
        sphere = Sphere(radius=2)
        sphere.always_sort_to_camera(self.camera)
        sphere.set_color(BLUE, 0.25)

        sphere_mesh = SurfaceMesh(sphere, resolution=(41, 21))
        sphere_mesh.set_stroke(WHITE, 0.5, 0.5)

        self.play(
            ShowCreation(sphere),
            Write(sphere_mesh, lag_ratio=1e-3),
            run_time=3
        )

        # Add axis labels
        labels = VGroup(
            Tex(R"|0\rangle"),
            Tex(R"|1\rangle"),
            Tex(R"|+\rangle"),
        )
        labels.scale(0.6)
        labels.set_backstroke(BLACK, 3)

        # Position labels at key points
        labels[0].rotate(90 * DEG, RIGHT)
        labels[0].next_to(axes.c2p(0, 0, 1), OUT + RIGHT, buff=0.1)

        labels[1].rotate(90 * DEG, RIGHT)
        labels[1].next_to(axes.c2p(0, 0, -1), OUT + RIGHT, buff=0.1)

        labels[2].rotate(90 * DEG, RIGHT)
        labels[2].next_to(axes.c2p(1, 0, 0), RIGHT, buff=0.1)

        self.play(LaggedStartMap(FadeIn, labels, lag_ratio=0.3))

        # Let it rotate for observation
        self.wait(10)


class StateVectorEvolution(InteractiveScene):
    """Shows a state vector evolving on the Bloch sphere with a tracing tail."""

    def construct(self):
        frame = self.frame

        # Set up 3D environment
        axes = ThreeDAxes((-1, 1), (-1, 1), (-1, 1))
        axes.scale(2.0)

        sphere = Sphere(radius=2)
        sphere.always_sort_to_camera(self.camera)
        sphere.set_color(BLUE, 0.15)

        sphere_mesh = SurfaceMesh(sphere, resolution=(21, 11))
        sphere_mesh.set_stroke(WHITE, 0.25, 0.25)

        frame.reorient(20, 70, 0)
        frame.add_ambient_rotation(2 * DEG)

        self.add(axes, sphere, sphere_mesh)

        # Create evolving vector
        theta_tracker = ValueTracker(0)
        phi_tracker = ValueTracker(PI / 4)

        def get_vector_end():
            theta = theta_tracker.get_value()
            phi = phi_tracker.get_value()
            return 2 * np.array([
                np.sin(phi) * np.cos(theta),
                np.sin(phi) * np.sin(theta),
                np.cos(phi)
            ])

        vector = Vector(get_vector_end(), thickness=5, fill_color=YELLOW)
        vector.always.set_perpendicular_to_camera(frame)
        vector.add_updater(
            lambda m: m.put_start_and_end_on(ORIGIN, get_vector_end())
        )

        # Add tracing tail
        tail = TracingTail(
            lambda: vector.get_end(),
            stroke_color=YELLOW,
            stroke_width=2,
            time_traced=5
        )

        self.add(vector, tail)
        self.wait()

        # Evolve the state
        self.play(
            theta_tracker.animate.set_value(2 * TAU),
            phi_tracker.animate.set_value(3 * PI / 4),
            run_time=10,
            rate_func=linear
        )

        self.wait(3)


class QuantumStateCollapse(InteractiveScene):
    """Demonstrates the concept of quantum state collapse upon measurement."""

    def construct(self):
        frame = self.frame

        # Simple 2D representation for clarity
        plane = NumberPlane((-2, 2), (-2, 2), faded_line_ratio=5)
        plane.scale(1.5)

        # Basis state labels
        zero_label = Tex(R"|0\rangle").scale(0.8)
        zero_label.next_to(plane.c2p(1, 0), DR, SMALL_BUFF)

        one_label = Tex(R"|1\rangle").scale(0.8)
        one_label.next_to(plane.c2p(0, 1), UL, SMALL_BUFF)

        # Unit circle
        circle = Circle(radius=plane.c2p(1, 0)[0])
        circle.set_stroke(GREY, 1, 0.5)

        self.add(plane, circle, zero_label, one_label)

        # Superposition state vector
        theta = 45 * DEG
        vector = Arrow(
            plane.c2p(0, 0),
            plane.c2p(np.cos(theta), np.sin(theta)),
            buff=0,
            thickness=5,
            fill_color=TEAL
        )

        state_label = Tex(
            R"\frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)",
            font_size=36
        )
        state_label.next_to(vector.get_end(), UR, SMALL_BUFF)
        state_label.set_backstroke(BLACK, 3)

        self.play(GrowArrow(vector), FadeIn(state_label))
        self.wait()

        # Measurement indicator
        measurement_text = Text("Measurement", font_size=36, color=RED)
        measurement_text.to_edge(UP)

        self.play(Write(measurement_text))

        # Flash effect
        self.play(
            Flash(vector.get_end(), color=WHITE, flash_radius=0.5),
            run_time=0.5
        )

        # Collapse to |0> (50% case)
        collapsed_vector = Arrow(
            plane.c2p(0, 0),
            plane.c2p(1, 0),
            buff=0,
            thickness=5,
            fill_color=BLUE
        )

        result_label = Tex(R"|0\rangle", font_size=48, color=BLUE)
        result_label.next_to(collapsed_vector.get_end(), RIGHT, MED_SMALL_BUFF)

        self.play(
            Transform(vector, collapsed_vector),
            FadeOut(state_label),
            FadeIn(result_label),
            run_time=0.3
        )
        self.wait(2)


if __name__ == "__main__":
    # To run: manimgl bloch_sphere_3d.py BlochSphere3D
    pass
