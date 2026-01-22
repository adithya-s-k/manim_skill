"""
Value Matrix Transformation Visualization
Shows how the Value matrix transforms embeddings and how the weighted sum
of value vectors produces the output.
"""

from manimlib import *
import numpy as np


def value_to_color(
    value,
    low_positive_color=BLUE_E,
    high_positive_color=BLUE_B,
    low_negative_color=RED_E,
    high_negative_color=RED_B,
    min_value=0.0,
    max_value=10.0
):
    """Map a value to a color based on sign and magnitude."""
    alpha = clip(float(inverse_interpolate(min_value, max_value, abs(value))), 0, 1)
    if value >= 0:
        return interpolate_color(low_positive_color, high_positive_color, alpha)
    else:
        return interpolate_color(low_negative_color, high_negative_color, alpha)


class WeightMatrix(DecimalMatrix):
    """A matrix with color-coded entries based on value."""
    def __init__(
        self,
        values=None,
        shape=(5, 7),
        value_range=(-9.9, 9.9),
        ellipses_row=-2,
        ellipses_col=-2,
        num_decimal_places=1,
        bracket_h_buff=0.1,
        **kwargs
    ):
        if values is None:
            values = np.random.uniform(*value_range, size=shape)
        self.shape = shape
        self.value_range = value_range
        self.ellipses_row = ellipses_row

        super().__init__(
            values,
            num_decimal_places=num_decimal_places,
            bracket_h_buff=bracket_h_buff,
            decimal_config=dict(include_sign=True),
            ellipses_row=ellipses_row,
            ellipses_col=ellipses_col,
        )
        self.reset_entry_colors()

    def reset_entry_colors(self):
        for entry in self.get_entries():
            entry.set_fill(color=value_to_color(
                entry.get_value(),
                min_value=0,
                max_value=max(self.value_range),
            ))
        return self


class ValueMatrixTransform(InteractiveScene):
    def construct(self):
        # Title
        title = Text("Value Matrix: Creating Contextual Updates", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))

        # Create words with embeddings
        words = ["fluffy", "blue", "creature"]
        word_mobs = VGroup(Text(word, font_size=36) for word in words)
        word_mobs.arrange(DOWN, buff=1.5)
        word_mobs.shift(4 * LEFT + 0.5 * DOWN)

        # Color code words
        word_mobs[0].set_color(TEAL)
        word_mobs[1].set_color(BLUE)
        word_mobs[2].set_color(ORANGE)

        # Embedding symbols
        e_template = Tex(R"\vec{\textbf{E}}_0", font_size=36)
        e_substr = e_template.make_number_changeable("0")

        e_syms = VGroup()
        e_arrows = VGroup()
        for i, word in enumerate(word_mobs, start=1):
            e_substr.set_value(i)
            e_sym = e_template.copy()
            e_sym.set_color(word.get_color())
            arrow = Arrow(word.get_right(), word.get_right() + 0.8 * RIGHT, buff=0.1)
            e_sym.next_to(arrow, RIGHT, buff=0.1)
            e_syms.add(e_sym)
            e_arrows.add(arrow)

        self.play(
            LaggedStartMap(FadeIn, word_mobs, shift=0.5 * RIGHT, lag_ratio=0.2),
        )
        self.play(
            LaggedStartMap(GrowArrow, e_arrows, lag_ratio=0.2),
            LaggedStartMap(FadeIn, e_syms, shift=0.5 * RIGHT, lag_ratio=0.2),
        )
        self.wait()

        # Value matrix
        np.random.seed(42)
        matrix = WeightMatrix(shape=(5, 7))
        matrix.set_height(2.5)
        matrix.move_to(0.5 * DOWN)

        mat_label = Tex("W_V", font_size=48)
        mat_label.set_color(RED)
        mat_label.next_to(matrix, UP)

        # Value vectors
        v_template = Tex(R"\vec{\textbf{V}}_0", font_size=36)
        v_template.set_color(RED)
        v_substr = v_template.make_number_changeable("0")

        v_syms = VGroup()
        v_arrows = VGroup()
        for i, e_sym in enumerate(e_syms, start=1):
            v_substr.set_value(i)
            v_arrow = Arrow(ORIGIN, 0.8 * RIGHT, buff=0)
            v_arrow.next_to(matrix, RIGHT, buff=0.3)
            v_arrow.match_y(e_sym)
            v_sym = v_template.copy()
            v_sym.next_to(v_arrow, RIGHT, buff=0.1)
            v_syms.add(v_sym)
            v_arrows.add(v_arrow)

        # Show transformation
        self.play(
            FadeIn(matrix, lag_ratio=0.01),
            FadeIn(mat_label, shift=0.25 * UP),
        )
        self.wait()

        # Transform each E to V
        for e_sym, v_arrow, v_sym in zip(e_syms, v_arrows, v_syms):
            self.play(
                TransformFromCopy(e_sym, v_sym, path_arc=-30 * DEGREES),
                GrowArrow(v_arrow),
                run_time=0.7
            )

        self.wait()

        # Show weighted sum
        weighted_label = Text("Weighted Sum of Values", font_size=36)
        weighted_label.to_edge(RIGHT)
        weighted_label.shift(UP)

        # Attention weights
        weights = [0.6, 0.3, 0.1]
        weight_labels = VGroup()
        for w, v_sym in zip(weights, v_syms):
            w_label = DecimalNumber(w, num_decimal_places=1, font_size=30)
            w_label.next_to(v_sym, RIGHT, buff=0.3)
            w_label.set_color(YELLOW)
            weight_labels.add(w_label)

        times_syms = VGroup(
            Tex(R"\times", font_size=30).next_to(wl, LEFT, buff=0.1)
            for wl in weight_labels
        )

        self.play(
            Write(weighted_label),
            LaggedStartMap(FadeIn, weight_labels, shift=0.2 * LEFT, lag_ratio=0.1),
            LaggedStartMap(FadeIn, times_syms, lag_ratio=0.1),
        )
        self.wait()

        # Show result
        result_label = Tex(R"\Delta \vec{\textbf{E}}_3", font_size=42)
        result_label.set_color(YELLOW)
        result_label.next_to(weighted_label, DOWN, buff=1.0)

        plus_syms = VGroup(Tex("+", font_size=30) for _ in range(2))
        weighted_v = VGroup()
        for i, (w, v_sym) in enumerate(zip(weight_labels, v_syms)):
            term = VGroup(w.copy(), v_sym.copy())
            weighted_v.add(term)

        weighted_v.arrange(RIGHT, buff=0.3)
        for plus, term in zip(plus_syms, weighted_v[1:]):
            plus.next_to(term, LEFT, buff=0.1)

        weighted_sum = VGroup(weighted_v[0], plus_syms[0], weighted_v[1], plus_syms[1], weighted_v[2])
        weighted_sum.scale(0.8)
        weighted_sum.next_to(result_label, UP, buff=0.5)

        eq_sign = Tex("=", font_size=36)
        eq_sign.next_to(result_label, LEFT, buff=0.2)

        self.play(
            LaggedStart(
                (TransformFromCopy(VGroup(wl, vs), wv)
                for wl, vs, wv in zip(weight_labels, v_syms, weighted_v)),
                lag_ratio=0.2
            ),
            LaggedStartMap(FadeIn, plus_syms, lag_ratio=0.3),
        )
        self.play(
            FadeIn(eq_sign),
            FadeIn(result_label, shift=0.2 * DOWN),
        )
        self.wait()

        # Explanation
        explanation = Text(
            "This update adds context\nfrom attended tokens",
            font_size=30
        )
        explanation.to_edge(DOWN)
        self.play(Write(explanation))
        self.wait(2)
