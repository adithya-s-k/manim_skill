"""
Weight Matrix Visualization for MLPs
Shows a color-coded weight matrix with values mapped to colors.
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
    """Maps a numeric value to a color based on sign and magnitude."""
    alpha = clip(float(inverse_interpolate(min_value, max_value, abs(value))), 0, 1)
    if value >= 0:
        colors = (low_positive_color, high_positive_color)
    else:
        colors = (low_negative_color, high_negative_color)
    return interpolate_color_by_hsl(*colors, alpha)


class WeightMatrixVisualization(InteractiveScene):
    """
    Visualizes a weight matrix with color-coded entries.
    Blue = positive values, Red = negative values.
    Brighter = larger magnitude.

    Demonstrates: DecimalMatrix, color mapping, matrix operations
    """

    def construct(self):
        # Create weight matrix with random values
        np.random.seed(42)
        n_rows, n_cols = 6, 8
        values = np.random.uniform(-9.9, 9.9, size=(n_rows, n_cols))

        # Build the matrix display
        matrix = self.create_weight_matrix(values)
        matrix.set_height(4)
        matrix.to_edge(LEFT, buff=1)

        # Title
        title = Text("Weight Matrix", font_size=48)
        title.to_edge(UP)

        # Legend
        legend = self.create_color_legend()
        legend.to_edge(RIGHT, buff=1)

        # Animate
        self.play(Write(title))
        self.play(FadeIn(matrix, lag_ratio=0.02, run_time=2))
        self.play(FadeIn(legend))
        self.wait(2)

        # Highlight a single row
        row_idx = 2
        row = matrix[row_idx]
        row_rect = SurroundingRectangle(row, buff=0.1)
        row_rect.set_stroke(YELLOW, 3)

        row_label = Text(f"Row {row_idx}: one neuron's weights", font_size=24)
        row_label.next_to(row_rect, DOWN)

        self.play(ShowCreation(row_rect))
        self.play(Write(row_label))
        self.wait(2)

        # Show dot product concept
        self.play(FadeOut(row_rect), FadeOut(row_label))
        self.wait()

    def create_weight_matrix(self, values):
        """Creates a VGroup of DecimalNumbers arranged as a matrix."""
        n_rows, n_cols = values.shape
        entries = VGroup()
        rows = VGroup()

        for i in range(n_rows):
            row = VGroup()
            for j in range(n_cols):
                val = values[i, j]
                entry = DecimalNumber(
                    val,
                    num_decimal_places=1,
                    include_sign=True,
                    font_size=24
                )
                entry.set_color(value_to_color(val, max_value=9.9))
                row.add(entry)
                entries.add(entry)
            row.arrange(RIGHT, buff=0.3)
            rows.add(row)

        rows.arrange(DOWN, buff=0.2)

        # Add brackets
        left_bracket = Tex(R"\left[", font_size=72)
        right_bracket = Tex(R"\right]", font_size=72)
        left_bracket.stretch_to_fit_height(rows.get_height() * 1.1)
        right_bracket.stretch_to_fit_height(rows.get_height() * 1.1)
        left_bracket.next_to(rows, LEFT, buff=0.1)
        right_bracket.next_to(rows, RIGHT, buff=0.1)

        return VGroup(*rows, left_bracket, right_bracket)

    def create_color_legend(self):
        """Creates a color legend showing value-to-color mapping."""
        legend = VGroup()

        # Title
        title = Text("Color Legend", font_size=24)
        legend.add(title)

        # Positive values
        pos_example = DecimalNumber(5.0, include_sign=True, font_size=24)
        pos_example.set_color(value_to_color(5.0))
        pos_label = Text("Positive", font_size=20)
        pos_row = VGroup(pos_example, pos_label).arrange(RIGHT, buff=0.3)
        legend.add(pos_row)

        # Negative values
        neg_example = DecimalNumber(-5.0, include_sign=True, font_size=24)
        neg_example.set_color(value_to_color(-5.0))
        neg_label = Text("Negative", font_size=20)
        neg_row = VGroup(neg_example, neg_label).arrange(RIGHT, buff=0.3)
        legend.add(neg_row)

        # Arrange vertically
        legend.arrange(DOWN, buff=0.4, aligned_edge=LEFT)

        return legend


class MatrixVectorProduct(InteractiveScene):
    """
    Shows how a weight matrix multiplies with an input vector.

    Demonstrates: Matrix-vector multiplication visualization
    """

    def construct(self):
        # Create a simple 4x3 matrix and 3x1 vector
        np.random.seed(123)
        matrix_values = np.random.uniform(-5, 5, size=(4, 3))
        vector_values = np.random.uniform(-5, 5, size=(3,))

        # Build matrix display
        matrix_entries = VGroup()
        for i in range(4):
            row = VGroup()
            for j in range(3):
                val = matrix_values[i, j]
                entry = DecimalNumber(val, num_decimal_places=1, include_sign=True, font_size=28)
                entry.set_color(value_to_color(val, max_value=5))
                row.add(entry)
            row.arrange(RIGHT, buff=0.4)
            matrix_entries.add(row)
        matrix_entries.arrange(DOWN, buff=0.3)

        # Add brackets
        m_left = Tex("[").stretch_to_fit_height(matrix_entries.get_height() * 1.1)
        m_right = Tex("]").stretch_to_fit_height(matrix_entries.get_height() * 1.1)
        m_left.next_to(matrix_entries, LEFT, buff=0.05)
        m_right.next_to(matrix_entries, RIGHT, buff=0.05)
        matrix = VGroup(matrix_entries, m_left, m_right)

        # Build vector display
        vector_entries = VGroup()
        for val in vector_values:
            entry = DecimalNumber(val, num_decimal_places=1, include_sign=True, font_size=28)
            entry.set_color(YELLOW)
            vector_entries.add(entry)
        vector_entries.arrange(DOWN, buff=0.3)

        v_left = Tex("[").stretch_to_fit_height(vector_entries.get_height() * 1.1)
        v_right = Tex("]").stretch_to_fit_height(vector_entries.get_height() * 1.1)
        v_left.next_to(vector_entries, LEFT, buff=0.05)
        v_right.next_to(vector_entries, RIGHT, buff=0.05)
        vector = VGroup(vector_entries, v_left, v_right)

        # Position matrix and vector
        matrix.move_to(2.5 * LEFT)
        vector.next_to(matrix, RIGHT, buff=0.5)

        # Labels
        matrix_label = Tex("W", font_size=48)
        matrix_label.next_to(matrix, UP)
        vector_label = Tex(R"\vec{x}", font_size=48).set_color(YELLOW)
        vector_label.next_to(vector, UP)

        # Title
        title = Text("Matrix-Vector Product", font_size=42)
        title.to_edge(UP)

        # Show initial setup
        self.play(Write(title))
        self.play(
            FadeIn(matrix),
            FadeIn(vector),
            Write(matrix_label),
            Write(vector_label)
        )
        self.wait()

        # Equals and result placeholder
        equals = Tex("=", font_size=48)
        equals.next_to(vector, RIGHT, buff=0.5)

        # Compute result
        result_values = matrix_values @ vector_values
        result_entries = VGroup()
        for val in result_values:
            entry = DecimalNumber(val, num_decimal_places=1, include_sign=True, font_size=28)
            entry.set_color(GREEN)
            result_entries.add(entry)
        result_entries.arrange(DOWN, buff=0.3)

        r_left = Tex("[").stretch_to_fit_height(result_entries.get_height() * 1.1)
        r_right = Tex("]").stretch_to_fit_height(result_entries.get_height() * 1.1)
        r_left.next_to(result_entries, LEFT, buff=0.05)
        r_right.next_to(result_entries, RIGHT, buff=0.05)
        result = VGroup(result_entries, r_left, r_right)
        result.next_to(equals, RIGHT, buff=0.5)

        self.play(Write(equals))

        # Animate row-by-row computation
        for row_idx in range(4):
            row = matrix_entries[row_idx]
            row_rect = SurroundingRectangle(row, buff=0.05)
            row_rect.set_stroke(PINK, 2)
            vec_rect = SurroundingRectangle(vector_entries, buff=0.05)
            vec_rect.set_stroke(PINK, 2)

            self.play(
                ShowCreation(row_rect),
                ShowCreation(vec_rect),
                run_time=0.5
            )
            self.play(
                Write(result_entries[row_idx]),
                run_time=0.5
            )
            self.play(
                FadeOut(row_rect),
                FadeOut(vec_rect),
                run_time=0.3
            )

        self.play(FadeIn(r_left), FadeIn(r_right))
        self.wait(2)
