"""
Qubit State Vector Visualization
================================
Shows a 2D plane representing a single qubit's state as a unit vector.
The vector rotates through different states while displaying probability
distribution for measuring |0> or |1>.

Key concepts demonstrated:
- NumberPlane for 2D visualization
- Vector with updaters tracking angle
- DecimalMatrix for live coordinate display
- Distribution bars showing measurement probabilities
"""
from manimlib import *


class QubitStateVector(InteractiveScene):
    def construct(self):
        # Set up the 2D plane for qubit visualization
        plane = NumberPlane((-2, 2), (-2, 2), faded_line_ratio=5)
        plane.set_height(6)
        plane.to_edge(LEFT, buff=1.0)

        # Create qubit labels |0> and |1>
        zero_label = VGroup(Tex(R"|"), Integer(0), Tex(R"\rangle"))
        zero_label.arrange(RIGHT, buff=0.05)
        one_label = VGroup(Tex(R"|"), Integer(1), Tex(R"\rangle"))
        one_label.arrange(RIGHT, buff=0.05)

        qubit_labels = VGroup(zero_label, one_label)
        qubit_labels.scale(0.6)
        zero_label.next_to(plane.c2p(1, 0), DR, SMALL_BUFF)
        one_label.next_to(plane.c2p(0, 1), DR, SMALL_BUFF)

        self.add(plane, qubit_labels)

        # Create the state vector
        theta_tracker = ValueTracker(30 * DEG)

        vector = Arrow(
            plane.c2p(0, 0),
            plane.c2p(1, 0),
            buff=0,
            thickness=6,
            fill_color=TEAL
        )
        vector.add_updater(lambda m: m.set_angle(theta_tracker.get_value()))
        vector.add_updater(lambda m: m.shift(plane.c2p(0, 0) - m.get_start()))

        # Coordinate display
        coord_display = DecimalMatrix(
            [[1.0], [0.0]],
            bracket_h_buff=0.1,
            decimal_config=dict(include_sign=True, num_decimal_places=2)
        )
        coord_display.scale(0.6)
        coord_display.add_background_rectangle()
        coord_display.set_backstroke(BLACK, 5)

        def get_state():
            theta = theta_tracker.get_value()
            return np.array([math.cos(theta), math.sin(theta)])

        def update_coordinates(matrix):
            for element, value in zip(matrix.elements, get_state()):
                element.set_value(value)

        def position_label(matrix):
            x, y = get_state()
            buff = SMALL_BUFF + 0.4 * interpolate(
                matrix.get_width(), matrix.get_height(), x**2
            )
            vect = normalize(vector.get_vector())
            matrix.move_to(vector.get_end() + buff * vect)

        coord_display.add_updater(update_coordinates)
        coord_display.add_updater(position_label)

        self.add(vector, coord_display)

        # Add probability display on the right
        prob_title = Text("Measurement Probabilities", font_size=36)
        prob_title.to_edge(RIGHT, buff=1.0)
        prob_title.to_edge(UP, buff=1.0)

        qubits = VGroup(
            VGroup(Tex(R"|0\rangle"), Tex("")),
            VGroup(Tex(R"|1\rangle"), Tex("")),
        )
        qubits.arrange(DOWN, buff=1.0)
        qubits.next_to(prob_title, DOWN, buff=1.0)

        # Probability bars
        def get_prob_bars():
            probs = get_state()**2
            bars = VGroup()
            for i, (qubit, prob) in enumerate(zip(qubits, probs)):
                bar = Rectangle(
                    width=prob * 3,
                    height=0.4
                )
                bar.next_to(qubit[0], RIGHT, buff=0.3)
                bar.set_fill(
                    interpolate_color(BLUE_D, GREEN, prob),
                    opacity=1
                )
                bar.set_stroke(WHITE, 1)

                label = Integer(int(100 * prob), unit=R"\%", font_size=24)
                label.next_to(bar, RIGHT, SMALL_BUFF)

                bars.add(VGroup(bar, label))
            return bars

        prob_bars = always_redraw(get_prob_bars)

        self.add(prob_title, qubits, prob_bars)

        # Add unit circle
        circle = Circle(radius=plane.c2p(1, 0)[0] - plane.c2p(0, 0)[0])
        circle.move_to(plane.c2p(0, 0))
        circle.set_stroke(YELLOW, 1, 0.5)

        self.play(ShowCreation(circle))

        # Animate the vector rotation
        self.play(theta_tracker.animate.set_value(60 * DEG), run_time=2)
        self.wait()

        self.play(theta_tracker.animate.set_value(90 * DEG), run_time=2)
        self.wait()

        self.play(theta_tracker.animate.set_value(45 * DEG), run_time=2)
        self.wait()

        # Show the constraint x^2 + y^2 = 1
        constraint = Tex(R"x^2 + y^2 = 1", font_size=48)
        constraint.to_corner(UR, buff=1.0)
        constraint.set_color(YELLOW)

        self.play(Write(constraint))
        self.wait()

        # Full rotation
        self.play(
            theta_tracker.animate.set_value(theta_tracker.get_value() + TAU),
            run_time=6
        )
        self.wait()


class QubitKetNotation(InteractiveScene):
    """Shows the relationship between vector coordinates and ket notation."""

    def construct(self):
        # Title
        title = Text("Qubit State Representation", font_size=48)
        title.to_edge(UP)
        self.add(title)

        # Vector form
        vector_form = Tex(
            R"\begin{bmatrix} x \\ y \end{bmatrix}",
            font_size=72
        )
        vector_form.shift(2 * LEFT)

        # Ket form
        ket_form = Tex(
            R"x|0\rangle + y|1\rangle",
            font_size=72
        )
        ket_form.shift(2 * RIGHT)

        # Equals sign
        equals = Tex(R"\Leftrightarrow", font_size=72)

        self.play(Write(vector_form))
        self.wait()

        self.play(Write(equals))
        self.play(Write(ket_form))
        self.wait()

        # Constraint
        constraint = Tex(
            R"\text{where } x^2 + y^2 = 1",
            font_size=36
        )
        constraint.next_to(VGroup(vector_form, equals, ket_form), DOWN, buff=1.0)
        constraint.set_color(YELLOW)

        self.play(FadeIn(constraint, shift=UP))
        self.wait(2)


if __name__ == "__main__":
    # To run: manimgl qubit_state_vector.py QubitStateVector
    pass
