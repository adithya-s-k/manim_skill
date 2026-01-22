"""
Visualization distinguishing between weights (model parameters) and data.
Demonstrates: DecimalMatrix, VGroup organization, Transform animations
"""
from manimlib import *
import numpy as np
import random


def value_to_color(
    value,
    low_positive_color=BLUE_E,
    high_positive_color=BLUE_B,
    low_negative_color=RED_E,
    high_negative_color=RED_B,
    min_value=0.0,
    max_value=10.0
):
    """Map a numeric value to a color gradient."""
    alpha = clip(float(inverse_interpolate(min_value, max_value, abs(value))), 0, 1)
    if value >= 0:
        colors = (low_positive_color, high_positive_color)
    else:
        colors = (low_negative_color, high_negative_color)
    return interpolate_color_by_hsl(*colors, alpha)


class WeightMatrix(DecimalMatrix):
    """A matrix displaying weight values with color coding."""

    def __init__(
        self,
        values=None,
        shape=(4, 6),
        value_range=(-9.9, 9.9),
        num_decimal_places=1,
        **kwargs
    ):
        if values is None:
            values = np.random.uniform(*value_range, size=shape)
        self.value_range = value_range

        super().__init__(
            values,
            num_decimal_places=num_decimal_places,
            **kwargs
        )
        self.color_entries()

    def color_entries(self):
        for entry in self.get_entries():
            entry.set_fill(color=value_to_color(
                entry.get_value(),
                min_value=0,
                max_value=max(abs(self.value_range[0]), abs(self.value_range[1])),
            ))
        return self


class NumericVector(DecimalMatrix):
    """A column vector displaying numeric values."""

    def __init__(
        self,
        values=None,
        length=6,
        value_range=(-9.9, 9.9),
        num_decimal_places=1,
        **kwargs
    ):
        if values is None:
            values = np.random.uniform(*value_range, size=(length, 1))
        elif len(values.shape) == 1:
            values = values.reshape((-1, 1))

        super().__init__(
            values,
            num_decimal_places=num_decimal_places,
            **kwargs
        )
        # Color entries from dark to light based on value
        for entry in self.get_entries():
            alpha = clip(inverse_interpolate(
                value_range[0], value_range[1], abs(entry.get_value())
            ), 0, 1)
            entry.set_fill(interpolate_color(GREY_C, WHITE, alpha))


class WeightsVsData(Scene):
    def construct(self):
        # Create titles
        weights_title = Text("Weights", font_size=60, color=BLUE)
        data_title = Text("Data", font_size=60, color=GREY_B)

        weights_title.set_x(-FRAME_WIDTH / 4)
        data_title.set_x(FRAME_WIDTH / 4)

        for title in [weights_title, data_title]:
            title.to_edge(UP, buff=0.5)
            underline = Underline(title, stretch_factor=1.5)
            underline.match_color(title)
            title.add(underline)

        # Create vertical divider
        v_line = Line(UP, DOWN).set_height(5)
        v_line.set_stroke(GREY_A, 2)
        v_line.next_to(weights_title, DOWN, buff=0.5)
        v_line.set_x(0)

        # Create weight matrices (model parameters)
        matrices = VGroup(*(
            WeightMatrix(shape=(4, 5))
            for _ in range(2)
        ))
        matrices.arrange(DOWN, buff=0.5)
        matrices.set_height(4)
        matrices.next_to(weights_title, DOWN, buff=0.75)

        # Create data vectors (what flows through the network)
        vectors = VGroup(*(
            NumericVector(length=5)
            for _ in range(4)
        ))
        vectors.arrange(RIGHT, buff=0.3)
        vectors.set_height(3)
        vectors.next_to(data_title, DOWN, buff=0.75)

        # Animation: scatter numbers first, then organize
        all_mat_entries = VGroup(*(
            entry
            for mat in matrices
            for entry in mat.get_entries()
        ))
        all_vec_entries = VGroup(*(
            entry
            for vec in vectors
            for entry in vec.get_entries()
        ))

        # Save final positions
        for entry in [*all_mat_entries, *all_vec_entries]:
            entry.final_pos = entry.get_center().copy()

        # Scatter to random positions
        all_entries = VGroup(*all_mat_entries, *all_vec_entries)
        all_entries.shuffle()
        for entry in all_entries:
            entry.move_to([
                random.uniform(-7, 7),
                random.uniform(-3, 3),
                0
            ])
            entry.set_height(0.15)

        # Start animation
        self.add(all_entries)
        self.wait(0.5)

        # Animate gathering
        self.play(
            LaggedStart(*(
                entry.animate.move_to(entry.final_pos).set_height(0.25)
                for entry in all_mat_entries
            ), lag_ratio=0.02),
            ShowCreation(v_line),
            run_time=2
        )
        self.play(
            Write(weights_title),
            *(FadeIn(mat.get_brackets()) for mat in matrices),
        )

        self.play(
            LaggedStart(*(
                entry.animate.move_to(entry.final_pos).set_height(0.25)
                for entry in all_vec_entries
            ), lag_ratio=0.02),
            run_time=2
        )
        self.play(
            Write(data_title),
            *(FadeIn(vec.get_brackets()) for vec in vectors),
        )
        self.wait()

        # Add subtitles
        weights_sub = Text("Fixed during inference", font_size=30)
        weights_sub.next_to(matrices, DOWN, buff=0.3)

        data_sub = Text("Flows through network", font_size=30)
        data_sub.next_to(vectors, DOWN, buff=0.3)

        self.play(
            FadeIn(weights_sub, shift=UP),
            FadeIn(data_sub, shift=UP),
        )
        self.wait()

        # Show data flowing (animate vectors changing)
        for _ in range(3):
            new_vectors = VGroup(*(
                NumericVector(length=5)
                for _ in range(4)
            ))
            new_vectors.arrange(RIGHT, buff=0.3)
            new_vectors.set_height(3)
            new_vectors.move_to(vectors)

            self.play(
                Transform(vectors, new_vectors),
                run_time=1.5
            )
            self.wait(0.5)

        # Final emphasis
        weights_rect = SurroundingRectangle(matrices, color=BLUE, buff=0.2)
        data_rect = SurroundingRectangle(vectors, color=GREY_B, buff=0.2)

        self.play(
            ShowCreation(weights_rect),
            ShowCreation(data_rect),
        )
        self.wait(2)
