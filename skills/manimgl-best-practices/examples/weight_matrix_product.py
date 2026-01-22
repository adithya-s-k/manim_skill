"""
Weight Matrix Product Visualization
Shows how a weight matrix transforms an embedding vector step by step,
demonstrating the row-by-vector dot product pattern.
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


class NumericEmbedding(WeightMatrix):
    """A column vector (embedding) with color-coded entries."""
    def __init__(
        self,
        values=None,
        length=7,
        value_range=(-9.9, 9.9),
        ellipses_row=-2,
        **kwargs
    ):
        if values is None:
            shape = (length, 1)
        else:
            if len(values.shape) == 1:
                values = values.reshape((values.shape[0], 1))
            shape = values.shape

        super().__init__(
            values=values,
            shape=shape,
            value_range=value_range,
            ellipses_row=ellipses_row,
            ellipses_col=None,
            **kwargs
        )


class WeightMatrixProduct(InteractiveScene):
    def construct(self):
        # Create the weight matrix
        np.random.seed(42)
        matrix = WeightMatrix(shape=(5, 7))
        matrix.set_height(3.5)
        matrix.to_edge(LEFT, buff=1)

        # Create input vector
        in_vect = NumericEmbedding(length=7)
        in_vect.match_height(matrix)
        in_vect.next_to(matrix, RIGHT, buff=0.3)

        # Labels
        mat_brace = Brace(matrix, UP)
        mat_label = Tex("W_Q", font_size=48)
        mat_label.set_color(YELLOW)
        mat_label.next_to(mat_brace, UP, SMALL_BUFF)

        vect_label = Tex(R"\vec{E}", font_size=48)
        vect_label.set_color(TEAL)
        vect_label.next_to(in_vect, UP, buff=0.5)

        self.play(
            FadeIn(matrix, lag_ratio=0.01),
            FadeIn(in_vect),
            GrowFromCenter(mat_brace),
            FadeIn(mat_label, shift=0.25 * UP),
            FadeIn(vect_label, shift=0.25 * DOWN),
        )
        self.wait()

        # Create result vector
        eq = Tex("=", font_size=60)
        eq.next_to(in_vect, RIGHT, buff=0.4)

        result = NumericEmbedding(length=5)
        result.match_height(matrix)
        result.next_to(eq, RIGHT, buff=0.4)

        result_label = Tex(R"\vec{Q}", font_size=48)
        result_label.set_color(YELLOW)
        result_label.next_to(result, UP, buff=0.5)

        self.play(
            FadeIn(eq),
            FadeIn(result.get_brackets()),
        )

        # Animate row-by-vector products
        rows = matrix.get_rows()
        result_entries = result.get_entries()
        vect_entries = in_vect.get_entries()

        last_rects = VGroup()
        for n, (row, entry) in enumerate(zip(rows, result_entries)):
            if n == len(rows) - 2:  # Skip ellipses row
                self.add(entry)
                continue

            # Highlight current row and vector
            row_rects = VGroup(SurroundingRectangle(r, buff=0.05) for r in row)
            vect_rects = VGroup(SurroundingRectangle(v, buff=0.05) for v in vect_entries[:-2])
            row_rects.set_stroke(YELLOW, 2)
            vect_rects.set_stroke(YELLOW, 2)

            # Compute actual dot product
            row_vals = [r.get_value() for r in row if isinstance(r, DecimalNumber)]
            vect_vals = [v.get_value() for v in vect_entries[:-2] if isinstance(v, DecimalNumber)]
            dot_product = sum(a * b for a, b in zip(row_vals, vect_vals))

            self.play(
                ShowIncreasingSubsets(row_rects),
                ShowIncreasingSubsets(vect_rects),
                UpdateFromAlphaFunc(
                    entry,
                    lambda m, a, target=dot_product: m.set_value(target * a)
                ),
                FadeOut(last_rects),
                rate_func=linear,
                run_time=0.8,
            )
            last_rects = VGroup(row_rects, vect_rects)

        self.play(FadeOut(last_rects))

        # Show result label
        self.play(FadeIn(result_label, shift=0.25 * DOWN))
        self.wait()

        # Add explanation
        explanation = Text(
            "Each row produces one\nentry of the output",
            font_size=36
        )
        explanation.to_edge(DOWN)
        self.play(Write(explanation))
        self.wait(2)
