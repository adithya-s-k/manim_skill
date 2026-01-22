"""
Superposition Effect Visualization
==================================
Creates a visual "superposition" effect where multiple quantum states
appear to exist simultaneously with a glowing, oscillating appearance.

Key concepts demonstrated:
- Custom Group subclass with updaters
- ValueTracker for controlling animation parameters
- Glow effects using replicated objects with varying stroke widths
- Continuous animation with add_updater
"""
from manimlib import *


class Superposition(Group):
    """
    A visual effect that makes multiple pieces appear to be in superposition.

    The pieces jitter/oscillate around their center positions with a glowing
    effect, simulating the uncertainty of a quantum superposition.
    """

    def __init__(
        self,
        pieces,
        offset_multiple=0.2,
        max_rot_vel=3,
        glow_color=TEAL,
        glow_stroke_range=(1, 22, 4),
        glow_stroke_opacity=0.05
    ):
        self.pieces = pieces
        self.center_points = Group(
            Point(piece.get_center())
            for piece in pieces
        )
        self.offset_multiplier = ValueTracker(offset_multiple)

        # Initialize each piece with random offset and rotation velocity
        for piece, point_mob in zip(pieces, self.center_points):
            piece.center_point = point_mob
            piece.offset_vect = rotate_vector(RIGHT, np.random.uniform(0, TAU))
            piece.offset_vect_rot_vel = np.random.uniform(-max_rot_vel, max_rot_vel)

        # Create glow layers with varying stroke widths
        glow_strokes = np.arange(*glow_stroke_range)
        glows = pieces.replicate(len(glow_strokes))
        glows.set_fill(opacity=0)
        glows.set_joint_type('no_joint')

        for glow, sw in zip(glows, glow_strokes):
            glow.set_stroke(glow_color, width=float(sw), opacity=glow_stroke_opacity)

        self.glows = glows

        super().__init__(glows, pieces, self.center_points, self.offset_multiplier)
        self.add_updater(lambda m, dt: m.update_piece_positions(dt))

    def update_piece_positions(self, dt):
        """Update positions with oscillating motion."""
        offset_multiple = self.offset_multiplier.get_value()

        for piece in self.pieces:
            piece.offset_vect = rotate_vector(
                piece.offset_vect,
                dt * piece.offset_vect_rot_vel
            )
            piece.offset_radius = offset_multiple
            piece.move_to(
                piece.center_point.get_center() +
                piece.offset_radius * piece.offset_vect
            )

        # Update glow positions to match pieces
        for glow in self.glows:
            for sm1, sm2 in zip(
                glow.family_members_with_points(),
                self.pieces.family_members_with_points()
            ):
                sm1.match_points(sm2)

    def set_offset_multiple(self, value):
        """Control the amount of jitter."""
        self.offset_multiplier.set_value(value)
        return self

    def set_glow_opacity(self, opacity=0.1):
        """Control the glow intensity."""
        self.glows.set_stroke(opacity=opacity)
        return self


class SuperpositionDemo(InteractiveScene):
    """Demonstrates the superposition visual effect."""

    def construct(self):
        # Title
        title = Text("Quantum Superposition", font_size=60)
        title.to_edge(UP)
        self.add(title)

        # Create bit strings representing possible quantum states
        def create_bit_string(value, length=4):
            """Create a visual bit string like |0101>"""
            bits = bin(value)[2:].zfill(length)
            bit_mobs = VGroup(
                Integer(int(b)) for b in bits
            )
            bit_mobs.arrange(RIGHT, buff=0.1)
            return bit_mobs

        # Create ket notation
        def create_ket(value, length=4):
            bits = create_bit_string(value, length)
            ket = VGroup(
                Tex(R"|"),
                bits,
                Tex(R"\rangle")
            )
            ket[0].next_to(bits, LEFT, buff=0.05)
            ket[2].next_to(bits, RIGHT, buff=0.05)
            return ket

        # Create multiple states
        states = VGroup(
            create_ket(n, 4)
            for n in range(16)
        )
        states.arrange(DOWN, buff=0.2)
        states.set_height(5)
        states.center()

        # Create superposition effect
        superposition = Superposition(states, offset_multiple=0, glow_stroke_opacity=0)
        superposition.update()

        self.add(superposition)

        # Animate the superposition emerging
        self.play(
            superposition.animate.set_offset_multiple(0.15).set_glow_opacity(0.08),
            run_time=2
        )

        # Let it oscillate
        self.wait(5)

        # Collapse to a single state (measurement)
        measurement_label = Text("Measurement", font_size=36, color=RED)
        measurement_label.next_to(superposition, RIGHT, buff=1.0)

        self.play(Write(measurement_label))
        self.play(
            Flash(states[7].get_center(), color=WHITE),
            run_time=0.3
        )

        # Collapse effect
        self.play(
            superposition.animate.set_offset_multiple(0).set_glow_opacity(0),
            run_time=0.5
        )

        # Highlight the measured state
        rect = SurroundingRectangle(states[7], buff=0.1, color=YELLOW)
        result_label = Text("Result: |0111>", font_size=36, color=YELLOW)
        result_label.next_to(superposition, DOWN, buff=0.5)

        self.play(
            ShowCreation(rect),
            FadeIn(result_label)
        )
        self.wait(2)


class BitStringVisualization(InteractiveScene):
    """Shows bit strings with ket notation."""

    def construct(self):
        # Create a grid of possible 4-qubit states
        def create_ket(value, length=4):
            bits_str = bin(value)[2:].zfill(length)
            tex = Tex(
                R"|" + bits_str + R"\rangle",
                font_size=36
            )
            return tex

        # Create grid
        states = VGroup(
            create_ket(n, 4)
            for n in range(16)
        )
        states.arrange_in_grid(4, 4, buff=0.5)
        states.center()

        # Title
        title = Text("4-Qubit Computational Basis States", font_size=48)
        title.to_edge(UP)

        self.add(title)
        self.play(
            LaggedStartMap(FadeIn, states, lag_ratio=0.1),
            run_time=3
        )
        self.wait()

        # Highlight the pattern: powers of 2
        # |0000> = 0, |0001> = 1, |0010> = 2, etc.
        decimal_labels = VGroup()
        for i, state in enumerate(states):
            label = Integer(i, font_size=24, color=YELLOW)
            label.next_to(state, DOWN, SMALL_BUFF)
            decimal_labels.add(label)

        self.play(
            LaggedStartMap(FadeIn, decimal_labels, lag_ratio=0.05),
            run_time=2
        )
        self.wait(2)


class QuantumParallelism(InteractiveScene):
    """Visualizes the concept of quantum parallelism."""

    def construct(self):
        # Classical vs Quantum comparison
        classical_title = Text("Classical", font_size=36)
        quantum_title = Text("Quantum", font_size=36)

        titles = VGroup(classical_title, quantum_title)
        titles.arrange(RIGHT, buff=4)
        titles.to_edge(UP, buff=1.0)

        v_line = Line(UP, DOWN).set_height(5)
        v_line.set_stroke(WHITE, 1)

        self.add(titles, v_line)

        # Classical: one input at a time
        classical_inputs = VGroup(
            Tex(R"|" + bin(n)[2:].zfill(4) + R"\rangle", font_size=30)
            for n in range(8)
        )
        classical_inputs.arrange(DOWN, buff=0.2)
        classical_inputs.next_to(classical_title, DOWN, buff=0.5)

        # Quantum: superposition of all inputs
        quantum_pieces = VGroup(
            Tex(R"|" + bin(n)[2:].zfill(4) + R"\rangle", font_size=30)
            for n in range(8)
        )
        quantum_pieces.arrange(DOWN, buff=0.2)
        quantum_pieces.next_to(quantum_title, DOWN, buff=0.5)

        # Create superposition effect for quantum side
        superposition = Superposition(
            quantum_pieces.copy(),
            offset_multiple=0.1,
            glow_color=TEAL
        )
        superposition.move_to(quantum_pieces)

        # Classical: process one at a time
        self.play(FadeIn(classical_inputs[0]))
        for i in range(1, 4):
            self.play(
                classical_inputs[i - 1].animate.set_opacity(0.3),
                FadeIn(classical_inputs[i])
            )

        # Show dots to indicate continuation
        dots = Tex(R"\vdots", font_size=48)
        dots.next_to(classical_inputs[3], DOWN)
        self.play(FadeIn(dots))

        # Quantum: all at once
        quantum_label = Text("All states\nsimultaneously!", font_size=24, color=TEAL)
        quantum_label.next_to(superposition, DOWN, buff=0.3)

        self.play(FadeIn(superposition))
        self.play(Write(quantum_label))

        self.wait(5)


if __name__ == "__main__":
    # To run: manimgl superposition_effect.py SuperpositionDemo
    pass
