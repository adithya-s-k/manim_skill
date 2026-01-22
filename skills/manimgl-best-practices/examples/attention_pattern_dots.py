"""
Attention Pattern Dots Visualization
Shows the attention pattern as a grid of varying-sized dots,
where dot size represents attention weight.
"""

from manimlib import *
import numpy as np


def softmax(logits, temperature=1.0):
    """Compute softmax of logits array."""
    logits = np.array(logits, dtype=float)
    # Mask future tokens (causal attention)
    logits = logits - np.max(logits)
    exps = np.exp(logits / temperature)
    return exps / np.sum(exps)


class AttentionPatternDots(InteractiveScene):
    def construct(self):
        # Parameters
        N = 8
        np.random.seed(42)

        # Create grid
        grid = Square(side_length=0.8).get_grid(N, N, buff=0)
        grid.set_stroke(GREY_A, 1)
        grid.stretch(0.95, 0)
        grid.stretch(0.85, 1)
        grid.move_to(0.5 * DOWN)

        self.add(grid)

        # Create query/key labels
        q_template = Tex(R"\vec{\textbf{Q}}_0", font_size=36).set_color(YELLOW)
        k_template = Tex(R"\vec{\textbf{K}}_0", font_size=36).set_color(TEAL)

        q_substr = q_template.make_number_changeable("0")
        k_substr = k_template.make_number_changeable("0")

        qs = VGroup()
        ks = VGroup()
        for n, square in enumerate(grid[:N], start=1):
            q_substr.set_value(n)
            q_template.next_to(square, UP, buff=SMALL_BUFF)
            qs.add(q_template.copy())

        for k, square in enumerate(grid[::N], start=1):
            k_substr.set_value(k)
            k_template.next_to(square, LEFT, buff=SMALL_BUFF)
            ks.add(k_template.copy())

        self.play(
            LaggedStartMap(FadeIn, qs, shift=0.2 * DOWN, lag_ratio=0.05),
            LaggedStartMap(FadeIn, ks, shift=0.2 * RIGHT, lag_ratio=0.05),
        )

        # Generate attention pattern (causal masking)
        values = np.random.normal(0, 1, (N, N))
        # Apply causal mask
        for n, row in enumerate(values):
            row[:n] = -np.inf

        # Softmax each column
        attention_pattern = np.zeros_like(values)
        for k in range(N):
            attention_pattern[:, k] = softmax(values[:, k])

        # Create dots based on attention weights
        dots = VGroup()
        for n in range(N):  # row (key)
            row_dots = VGroup()
            for k in range(N):  # column (query)
                weight = attention_pattern[n, k]
                dot = Dot(radius=0.35 * weight**0.5)
                dot.move_to(grid[n * N + k])

                # Color based on whether it's diagonal or not
                if n == k:
                    dot.set_fill(YELLOW, 0.9)
                elif n < k:
                    dot.set_fill(GREY_C, 0.8)
                else:  # Masked (should be zero)
                    dot.set_fill(RED, 0.2)

                row_dots.add(dot)
            dots.add(row_dots)

        flat_dots = VGroup(*it.chain(*dots))

        self.play(
            LaggedStartMap(GrowFromCenter, flat_dots, lag_ratio=0.01),
            run_time=2
        )
        self.wait()

        # Add title
        title = Text("Attention Pattern", font_size=60)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Highlight causal structure - masked region
        mask_label = Text("Masked\n(future tokens)", font_size=30)
        mask_label.set_color(RED)
        mask_label.to_corner(DL)

        masked_region = VGroup()
        for n in range(N):
            for k in range(n):
                square = grid[n * N + k].copy()
                square.set_fill(RED, 0.15)
                square.set_stroke(RED, 1)
                masked_region.add(square)

        self.play(
            FadeIn(masked_region, lag_ratio=0.02),
            FadeIn(mask_label),
        )
        self.wait()

        # Highlight self-attention (diagonal)
        diag_label = Text("Self-attention\n(diagonal)", font_size=30)
        diag_label.set_color(YELLOW)
        diag_label.to_corner(DR)

        diag_dots = VGroup(dots[i][i] for i in range(N))

        self.play(
            FadeIn(diag_label),
            LaggedStart(
                (dot.animate.scale(1.3).set_fill(YELLOW) for dot in diag_dots),
                lag_ratio=0.1,
            ),
        )
        self.play(
            LaggedStart(
                (dot.animate.scale(1/1.3) for dot in diag_dots),
                lag_ratio=0.1,
            ),
        )
        self.wait(2)
