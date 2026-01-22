"""
Attention Softmax with Masking Visualization
Shows how masking works in transformer attention - lower triangle gets -infinity
before softmax, producing zeros in the attention pattern.
"""

from manimlib import *
import numpy as np


def softmax(logits, temperature=1.0):
    """Compute softmax of logits array."""
    logits = np.array(logits)
    logits = logits - np.max(logits)  # For numerical stability
    exps = np.exp(logits / temperature)
    if np.isinf(exps).any() or np.isnan(exps).any():
        result = np.zeros_like(logits)
        result[np.argmax(logits)] = 1
        return result
    return exps / np.sum(exps)


class AttentionSoftmaxMasking(InteractiveScene):
    def construct(self):
        # Set up two grids: raw scores and normalized
        shape = (6, 6)
        left_grid = Square().get_grid(*shape, buff=0)
        left_grid.set_shape(5.5, 5)
        left_grid.to_edge(LEFT)
        left_grid.set_y(-0.5)
        left_grid.set_stroke(GREY_B, 1)

        right_grid = left_grid.copy()
        right_grid.to_edge(RIGHT)

        grids = VGroup(left_grid, right_grid)
        arrow = Arrow(left_grid, right_grid)
        sm_label = Text("softmax")
        sm_label.next_to(arrow, UP)

        titles = VGroup(
            Text("Unnormalized\nAttention Pattern"),
            Text("Normalized\nAttention Pattern"),
        )
        for title, grid in zip(titles, grids):
            title.next_to(grid, UP, buff=MED_LARGE_BUFF)

        # Create random values for attention scores
        values_array = np.random.normal(0, 2, shape)
        font_size = 30
        raw_values = VGroup(
            DecimalNumber(
                value,
                include_sign=True,
                font_size=font_size,
            ).move_to(square)
            for square, value in zip(left_grid, values_array.flatten())
        )

        self.add(left_grid)
        self.add(right_grid)
        self.add(titles)
        self.add(arrow)
        self.add(sm_label)
        self.add(raw_values)

        self.wait()

        # Highlight lower triangle (future tokens - to be masked)
        changers = VGroup()
        for n, dec in enumerate(raw_values):
            i = n // shape[1]
            j = n % shape[1]
            if i > j:  # Below diagonal - future tokens
                changers.add(dec)
                neg_inf = Tex(R"-\infty", font_size=36)
                neg_inf.move_to(dec)
                neg_inf.set_fill(RED, border_width=1.5)
                dec.target = neg_inf
                values_array[i, j] = -np.inf

        rects = VGroup(map(SurroundingRectangle, changers))
        rects.set_stroke(RED, 3)

        self.play(LaggedStartMap(ShowCreation, rects))
        self.play(
            LaggedStartMap(FadeOut, rects),
            LaggedStartMap(MoveToTarget, changers)
        )
        self.wait()

        # Compute and show normalized values
        normalized_array = np.array([
            softmax(col)
            for col in values_array.T
        ]).T

        normalized_values = VGroup(
            DecimalNumber(value, font_size=font_size).move_to(square)
            for square, value in zip(right_grid, normalized_array.flatten())
        )

        # Color by value and mark zeros
        for n, value in enumerate(normalized_values):
            val = value.get_value()
            value.set_fill(opacity=interpolate(0.5, 1, min(val * 3, 1)))
            if (n // shape[1]) > (n % shape[1]):
                value.set_fill(RED, 0.75)

        self.play(
            LaggedStart(
                (FadeTransform(v1.copy(), v2)
                for v1, v2 in zip(raw_values, normalized_values)),
                lag_ratio=0.05,
                group_type=Group
            )
        )
        self.wait(2)
