"""
Quantum Gates Visualization
===========================
Demonstrates quantum gate operations (H, X, Z) as reflections/rotations
of the state vector on the qubit plane.

Key concepts demonstrated:
- DashedLine for reflection axes
- Rotate animation with custom axis
- Gate labels and transitions
- Multiple gate applications
"""
from manimlib import *


class QuantumGatesVisualization(InteractiveScene):
    """Shows how quantum gates transform qubit states."""

    def construct(self):
        # Title
        title = Text("Quantum Gates", font_size=60)
        title.to_edge(UP)
        self.add(title)

        # Set up the qubit plane
        plane = NumberPlane((-2, 2), (-2, 2), faded_line_ratio=5)
        plane.set_height(5)
        plane.center().shift(0.5 * DOWN)

        # Qubit labels
        zero_label = Tex(R"|0\rangle").scale(0.7)
        zero_label.next_to(plane.c2p(1, 0), DR, SMALL_BUFF)

        one_label = Tex(R"|1\rangle").scale(0.7)
        one_label.next_to(plane.c2p(0, 1), UL, SMALL_BUFF)

        # Unit circle
        circle = Circle(radius=plane.c2p(1, 0)[0] - plane.c2p(0, 0)[0])
        circle.move_to(plane.c2p(0, 0))
        circle.set_stroke(GREY, 1, 0.5)

        self.add(plane, circle, zero_label, one_label)

        # Create the state vector
        vector = Arrow(
            plane.c2p(0, 0),
            plane.c2p(1, 0),
            buff=0,
            thickness=5,
            fill_color=TEAL
        )

        self.add(vector)

        # Define gate reflection axes
        # Z gate: reflection about x-axis (horizontal)
        # H gate: reflection about 22.5 degree line
        # X gate: reflection about 45 degree line (diagonal)
        gate_info = [
            ("Z", 0, BLUE),
            ("H", PI / 8, YELLOW),
            ("X", PI / 4, RED),
        ]

        gate_lines = VGroup()
        gate_labels = VGroup()

        for name, angle, color in gate_info:
            line = DashedLine(2 * LEFT, 2 * RIGHT)
            line.rotate(angle)
            line.move_to(plane.c2p(0, 0))
            line.set_stroke(color, 2)

            label = Text(name + " gate", font_size=24, color=color)
            label.next_to(plane.c2p(1, 1), DR)

            gate_lines.add(line)
            gate_labels.add(label)

        # Apply gates in sequence
        gate_sequence = [1, 0, 2, 1, 2, 1, 0, 1]  # H, Z, X, H, X, H, Z, H

        for i in gate_sequence:
            name, angle, color = gate_info[i]
            line = gate_lines[i]
            label = gate_labels[i]

            # Show the gate axis and label
            self.play(
                FadeIn(line),
                FadeIn(label),
                run_time=0.5
            )

            # Rotate vector by 180 degrees about the axis
            axis = rotate_vector(RIGHT, angle)
            axis_3d = np.array([axis[0], axis[1], 0])

            self.play(
                Rotate(
                    vector,
                    PI,
                    axis=axis_3d,
                    about_point=plane.c2p(0, 0)
                ),
                run_time=1.5
            )

            # Hide the gate visualization
            self.play(
                FadeOut(line),
                FadeOut(label),
                run_time=0.3
            )

        self.wait()


class HadamardGateDetail(InteractiveScene):
    """Detailed visualization of the Hadamard gate transformation."""

    def construct(self):
        # Set up two planes: before and after
        plane1 = NumberPlane((-2, 2), (-2, 2), faded_line_ratio=5)
        plane1.set_height(4)

        plane2 = plane1.copy()

        planes = VGroup(plane1, plane2)
        planes.arrange(RIGHT, buff=3)
        planes.center()

        # Labels
        before_label = Text("Before H", font_size=36)
        before_label.next_to(plane1, UP)

        after_label = Text("After H", font_size=36)
        after_label.next_to(plane2, UP)

        # Arrow between planes
        arrow = Arrow(plane1.get_right(), plane2.get_left(), thickness=5)
        h_label = Text("H", font_size=48, color=YELLOW)
        h_label.next_to(arrow, UP, SMALL_BUFF)

        # Hadamard matrix
        matrix_tex = Tex(
            R"\frac{1}{\sqrt{2}} \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}",
            font_size=30
        )
        matrix_tex.set_fill(GREY_B)
        matrix_tex.next_to(arrow, DOWN, SMALL_BUFF)

        self.add(planes, before_label, after_label, arrow, h_label, matrix_tex)

        # Add unit circles
        for plane in planes:
            circle = Circle(radius=plane.c2p(1, 0)[0] - plane.c2p(0, 0)[0])
            circle.move_to(plane.c2p(0, 0))
            circle.set_stroke(GREY, 1, 0.5)
            self.add(circle)

        # Create basis vectors
        # |0> state
        zero_vec = Arrow(
            plane1.c2p(0, 0),
            plane1.c2p(1, 0),
            buff=0,
            thickness=4,
            fill_color=BLUE
        )
        zero_label = Tex(R"|0\rangle", font_size=30, color=BLUE)
        zero_label.next_to(zero_vec.get_end(), UR, SMALL_BUFF)

        # |1> state
        one_vec = Arrow(
            plane1.c2p(0, 0),
            plane1.c2p(0, 1),
            buff=0,
            thickness=4,
            fill_color=GREEN
        )
        one_label = Tex(R"|1\rangle", font_size=30, color=GREEN)
        one_label.next_to(one_vec.get_end(), UL, SMALL_BUFF)

        # H|0> = |+> = (|0> + |1>)/sqrt(2)
        h_zero_vec = Arrow(
            plane2.c2p(0, 0),
            plane2.c2p(1, 1) / np.sqrt(2),
            buff=0,
            thickness=4,
            fill_color=BLUE
        )
        h_zero_label = Tex(R"H|0\rangle = |+\rangle", font_size=24, color=BLUE)
        h_zero_label.next_to(h_zero_vec.get_end(), UR, SMALL_BUFF)

        # H|1> = |-> = (|0> - |1>)/sqrt(2)
        h_one_vec = Arrow(
            plane2.c2p(0, 0),
            plane2.c2p(1, -1) / np.sqrt(2),
            buff=0,
            thickness=4,
            fill_color=GREEN
        )
        h_one_label = Tex(R"H|1\rangle = |-\rangle", font_size=24, color=GREEN)
        h_one_label.next_to(h_one_vec.get_end(), DR, SMALL_BUFF)

        # Animate
        self.play(
            GrowArrow(zero_vec),
            FadeIn(zero_label)
        )
        self.play(
            TransformFromCopy(zero_vec, h_zero_vec, path_arc=-30 * DEG),
            FadeIn(h_zero_label),
            run_time=2
        )
        self.wait()

        self.play(
            GrowArrow(one_vec),
            FadeIn(one_label)
        )
        self.play(
            TransformFromCopy(one_vec, h_one_vec, path_arc=-30 * DEG),
            FadeIn(h_one_label),
            run_time=2
        )
        self.wait(2)


class GateComposition(InteractiveScene):
    """Shows how multiple gates compose to create quantum circuits."""

    def construct(self):
        # Create a simple quantum circuit visualization
        wire = Line(4 * LEFT, 4 * RIGHT)
        wire.set_stroke(WHITE, 2)

        # Gate boxes
        gates = VGroup()
        gate_names = ["H", "X", "Z", "H"]
        colors = [YELLOW, RED, BLUE, YELLOW]

        for i, (name, color) in enumerate(zip(gate_names, colors)):
            box = Square(0.8)
            box.set_stroke(WHITE, 2)
            box.set_fill(BLACK, 1)
            box.move_to(wire.pfp((i + 1) / (len(gate_names) + 1)))

            label = Text(name, font_size=36, color=color)
            label.move_to(box)

            gates.add(VGroup(box, label))

        # Input and output labels
        input_label = Tex(R"|0\rangle", font_size=48)
        input_label.next_to(wire, LEFT)

        output_label = Tex(R"|\psi\rangle", font_size=48)
        output_label.next_to(wire, RIGHT)

        circuit = VGroup(wire, gates, input_label, output_label)
        circuit.center().shift(UP)

        # Title
        title = Text("Quantum Circuit", font_size=48)
        title.to_edge(UP)

        self.add(title)
        self.play(
            ShowCreation(wire),
            FadeIn(input_label),
            FadeIn(output_label)
        )

        # Show gates appearing one by one
        for gate in gates:
            self.play(FadeIn(gate, scale=1.2))

        self.wait()

        # Animate a "quantum state" passing through
        glow = GlowDot(wire.get_start(), color=TEAL, radius=0.3)
        glow.set_z_index(1)

        self.play(
            glow.animate.move_to(wire.get_end()),
            rate_func=linear,
            run_time=3
        )

        # Show final state
        final_state = Tex(
            R"|\psi\rangle = -|1\rangle",
            font_size=36
        )
        final_state.next_to(circuit, DOWN, buff=1.0)

        self.play(
            FadeOut(glow),
            FadeIn(final_state, shift=UP)
        )
        self.wait(2)


if __name__ == "__main__":
    # To run: manimgl quantum_gates.py QuantumGatesVisualization
    pass
