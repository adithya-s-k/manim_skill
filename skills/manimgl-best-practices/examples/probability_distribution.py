"""
Probability Distribution Visualization
======================================
Visualizes how a quantum state vector maps to a probability distribution
through the Born rule (amplitude squared = probability).

Key concepts demonstrated:
- DecimalMatrix for state vector display
- Rectangle bars for probability visualization
- always_redraw for reactive updates
- LaggedStartMap for sequential animations
"""
from manimlib import *


class ProbabilityDistribution(InteractiveScene):
    """Shows how state vector amplitudes become probabilities."""

    def construct(self):
        # Title
        title = Text("State Vector to Probability", font_size=48)
        title.to_edge(UP)
        self.add(title)

        # Create a simple 4-state vector (2 qubit system)
        state = normalize(np.array([1, 2, 0.5, 1.5]))

        # State vector display
        state_vector = DecimalMatrix(
            state.reshape((4, 1)),
            decimal_config=dict(include_sign=True, num_decimal_places=2)
        )
        state_vector.scale(0.8)
        state_vector.shift(3 * LEFT)

        vector_label = Text("State Vector", font_size=30)
        vector_label.next_to(state_vector, UP)

        # Bit string labels
        bit_labels = VGroup(
            Tex(R"|00\rangle", font_size=30),
            Tex(R"|01\rangle", font_size=30),
            Tex(R"|10\rangle", font_size=30),
            Tex(R"|11\rangle", font_size=30),
        )
        bit_labels.set_color(GREY_B)
        for bits, entry in zip(bit_labels, state_vector.get_entries()):
            bits.next_to(state_vector, LEFT, buff=0.3)
            bits.match_y(entry)

        self.add(state_vector, vector_label, bit_labels)

        # Arrow with transformation rule
        arrow = Arrow(LEFT, RIGHT, thickness=5)
        arrow.next_to(state_vector, RIGHT, buff=0.5)

        rule = Tex(R"|\alpha|^2", font_size=36)
        rule.next_to(arrow, UP, SMALL_BUFF)

        self.play(GrowArrow(arrow), Write(rule))

        # Probability bars
        probs = state ** 2
        max_bar_width = 3.0

        bar_labels = VGroup(
            Tex(R"|00\rangle", font_size=30),
            Tex(R"|01\rangle", font_size=30),
            Tex(R"|10\rangle", font_size=30),
            Tex(R"|11\rangle", font_size=30),
        )
        bar_labels.arrange(DOWN, buff=0.5)
        bar_labels.next_to(arrow, RIGHT, buff=1.0)

        bars = VGroup()
        prob_labels = VGroup()

        for i, (label, prob) in enumerate(zip(bar_labels, probs)):
            bar = Rectangle(
                width=prob * max_bar_width,
                height=0.4
            )
            bar.next_to(label, RIGHT, buff=0.2)
            bar.set_fill(
                interpolate_color(BLUE_D, GREEN, prob),
                opacity=1
            )
            bar.set_stroke(WHITE, 1)

            pct = Integer(int(100 * prob), unit=R"\%", font_size=24)
            pct.next_to(bar, RIGHT, SMALL_BUFF)

            bars.add(bar)
            prob_labels.add(pct)

        # Animate bars appearing
        self.play(
            FadeIn(bar_labels),
            LaggedStart(
                (GrowFromEdge(bar, LEFT)
                 for bar in bars),
                lag_ratio=0.2
            ),
            LaggedStartMap(FadeIn, prob_labels, lag_ratio=0.2),
            run_time=2
        )

        # Add sum constraint
        sum_eq = Tex(
            R"\sum_i |\alpha_i|^2 = 1",
            font_size=30
        )
        sum_eq.to_edge(DOWN, buff=1.0)
        sum_eq.set_color(YELLOW)

        self.play(Write(sum_eq))
        self.wait(2)


class DynamicStateVector(InteractiveScene):
    """Shows state vector evolving and probabilities updating in real-time."""

    def construct(self):
        # Set up state tracker
        n_states = 8
        phase_trackers = [ValueTracker(np.random.uniform(0, TAU)) for _ in range(n_states)]

        def get_state():
            """Generate a normalized state from phases."""
            raw = np.array([
                np.sin(tracker.get_value())
                for tracker in phase_trackers
            ])
            return normalize(raw + 0.1)

        # Create layout
        # Left: Quantum computer symbol
        qc_symbol = VGroup(
            Square(1.5).set_stroke(TEAL, 2).set_fill(GREY_E, 1),
            Tex(R"|Q\rangle", color=TEAL).scale(0.8)
        )
        qc_symbol[1].move_to(qc_symbol[0])
        qc_symbol.shift(4 * LEFT)

        # Middle: State vector
        state_vector = DecimalMatrix(
            np.zeros((n_states, 1)),
            decimal_config=dict(include_sign=True, num_decimal_places=2)
        )
        state_vector.scale(0.5)
        state_vector.center()

        def update_state_vector(matrix):
            state = get_state()
            for elem, val in zip(matrix.elements, state):
                elem.set_value(val)

        state_vector.add_updater(update_state_vector)

        # Bit labels
        bit_labels = VGroup(
            Tex(R"|" + bin(n)[2:].zfill(3) + R"\rangle", font_size=20)
            for n in range(n_states)
        )
        bit_labels.set_color(GREY_C)

        def update_bit_labels(labels):
            for bits, entry in zip(labels, state_vector.get_entries()):
                bits.next_to(state_vector, LEFT, buff=0.15)
                bits.match_y(entry)

        bit_labels.add_updater(update_bit_labels)

        # Right: Probability bars
        qubit_labels = VGroup(
            Tex(R"|" + bin(n)[2:].zfill(3) + R"\rangle", font_size=24)
            for n in range(n_states)
        )
        qubit_labels.arrange(DOWN, buff=0.25)
        qubit_labels.shift(2.5 * RIGHT)

        def get_prob_bars():
            probs = get_state() ** 2
            bars = VGroup()
            for qubit, prob in zip(qubit_labels, probs):
                bar = Rectangle(
                    width=prob * 4,
                    height=qubit.get_height() * 0.8
                )
                bar.next_to(qubit, RIGHT, buff=0.15)
                bar.set_fill(
                    interpolate_color(BLUE_D, GREEN, prob * 1.5),
                    opacity=1
                )
                bar.set_stroke(WHITE, 1)
                bars.add(bar)
            return bars

        prob_bars = always_redraw(get_prob_bars)

        # Arrow connecting state vector to probabilities
        arrow = Arrow(state_vector.get_right() + 0.3 * RIGHT,
                      qubit_labels.get_left() + 0.3 * LEFT,
                      thickness=4)
        arrow_label = Tex(R"|\cdot|^2", font_size=24)
        arrow_label.next_to(arrow, UP, SMALL_BUFF)

        # Add all elements
        self.add(qc_symbol, state_vector, bit_labels)
        self.add(arrow, arrow_label)
        self.add(qubit_labels, prob_bars)

        # Animate state evolution
        animations = [
            tracker.animate.set_value(tracker.get_value() + np.random.uniform(2, 5) * TAU)
            for tracker in phase_trackers
        ]

        self.play(
            *animations,
            run_time=10,
            rate_func=linear
        )

        self.wait()


class BornRuleExplanation(InteractiveScene):
    """Explains the Born rule for quantum measurement."""

    def construct(self):
        # Title
        title = Text("The Born Rule", font_size=60)
        title.to_edge(UP)
        self.add(title)

        # The rule
        rule = Tex(
            R"P(i) = |\langle i | \psi \rangle|^2 = |\alpha_i|^2",
            font_size=48
        )
        rule.next_to(title, DOWN, buff=1.0)

        self.play(Write(rule))
        self.wait()

        # Explanation
        explanation = VGroup(
            Tex(R"\alpha_i \text{ = amplitude for state } |i\rangle", font_size=30),
            Tex(R"|\alpha_i|^2 \text{ = probability of measuring } |i\rangle", font_size=30),
            Tex(R"\sum_i |\alpha_i|^2 = 1 \text{ (normalization)}", font_size=30),
        )
        explanation.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        explanation.next_to(rule, DOWN, buff=1.0)

        for line in explanation:
            self.play(FadeIn(line, shift=RIGHT))
            self.wait(0.5)

        self.wait()

        # Visual example
        example_title = Text("Example:", font_size=36)
        example_title.next_to(explanation, DOWN, buff=1.0)
        example_title.to_edge(LEFT, buff=1.0)

        state = Tex(
            R"|\psi\rangle = \frac{1}{\sqrt{2}}|0\rangle + \frac{1}{\sqrt{2}}|1\rangle",
            font_size=36
        )
        state.next_to(example_title, RIGHT, buff=0.5)

        probs = VGroup(
            Tex(R"P(0) = \left|\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{2}", font_size=30),
            Tex(R"P(1) = \left|\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{2}", font_size=30),
        )
        probs.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        probs.next_to(state, DOWN, buff=0.5)

        self.play(Write(example_title), Write(state))
        self.wait()
        self.play(LaggedStartMap(FadeIn, probs, lag_ratio=0.3))
        self.wait(2)


class GroverAmplification(InteractiveScene):
    """Visualizes amplitude amplification in Grover's algorithm."""

    def construct(self):
        # Title
        title = Text("Grover's Amplitude Amplification", font_size=48)
        title.to_edge(UP)
        self.add(title)

        # Create bar chart for amplitudes
        n_states = 8
        target = 5  # The "marked" state

        # Initial uniform state
        initial_amps = np.ones(n_states) / np.sqrt(n_states)

        def create_bars(amps, highlighted=None):
            bars = VGroup()
            labels = VGroup()
            for i, amp in enumerate(amps):
                bar = Rectangle(
                    width=0.5,
                    height=amp * 4
                )
                bar.set_fill(
                    YELLOW if i == highlighted else BLUE_D,
                    opacity=1
                )
                bar.set_stroke(WHITE, 1)
                bars.add(bar)

                label = Tex(R"|" + bin(i)[2:].zfill(3) + R"\rangle", font_size=16)
                labels.add(label)

            bars.arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
            bars.center().shift(DOWN)

            for bar, label in zip(bars, labels):
                label.next_to(bar, DOWN, SMALL_BUFF)

            return VGroup(bars, labels)

        # Show initial state
        bar_chart = create_bars(initial_amps)
        step_label = Text("Initial: Uniform Superposition", font_size=30)
        step_label.next_to(bar_chart, UP, buff=0.5)

        self.play(
            LaggedStartMap(GrowFromEdge, bar_chart[0], edge=DOWN, lag_ratio=0.1),
            FadeIn(bar_chart[1]),
            Write(step_label)
        )
        self.wait()

        # Grover iterations
        amps = initial_amps.copy()
        for iteration in range(3):
            # Oracle: flip amplitude of target
            amps[target] *= -1

            # Show oracle step
            new_bars = create_bars(np.abs(amps), target)
            new_bars[0][target].set_fill(RED)

            oracle_label = Text(f"Step {iteration * 2 + 1}: Oracle (flip target)", font_size=30)
            oracle_label.next_to(bar_chart, UP, buff=0.5)

            self.play(
                Transform(bar_chart[0], new_bars[0]),
                Transform(step_label, oracle_label)
            )
            self.wait()

            # Diffusion: reflect about mean
            mean = np.mean(amps)
            amps = 2 * mean - amps

            new_bars = create_bars(amps, target)

            diffusion_label = Text(f"Step {iteration * 2 + 2}: Diffusion (amplify)", font_size=30)
            diffusion_label.next_to(bar_chart, UP, buff=0.5)

            self.play(
                Transform(bar_chart[0], new_bars[0]),
                Transform(step_label, diffusion_label)
            )
            self.wait()

        # Final result
        final_label = Text("Result: High probability for target state!", font_size=30, color=GREEN)
        final_label.next_to(bar_chart, UP, buff=0.5)

        self.play(Transform(step_label, final_label))

        # Highlight target
        rect = SurroundingRectangle(
            VGroup(bar_chart[0][target], bar_chart[1][target]),
            buff=0.1,
            color=YELLOW
        )
        self.play(ShowCreation(rect))
        self.wait(2)


if __name__ == "__main__":
    # To run: manimgl probability_distribution.py ProbabilityDistribution
    pass
