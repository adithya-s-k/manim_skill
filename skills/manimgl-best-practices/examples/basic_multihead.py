"""
Basic Multi-Head Attention - ManimGL (using Scene, not InteractiveScene)

Run with: manimgl basic_multihead.py MultiHeadBasic -w -l
"""
from manimlib import *
import numpy as np


def softmax(logits):
    logits = np.array(logits)
    logits = logits - np.max(logits)
    exps = np.exp(logits)
    return exps / np.sum(exps)


class AttentionGrid(VGroup):
    """Attention pattern grid."""

    def __init__(self, n=6, seed=0, **kwargs):
        super().__init__(**kwargs)
        np.random.seed(seed)

        cell = 0.35
        grid = VGroup()
        for i in range(n):
            for j in range(n):
                sq = Square(side_length=cell)
                sq.set_stroke(WHITE, 0.5, 0.3)
                sq.move_to([j * cell, -i * cell, 0])
                grid.add(sq)
        grid.center()

        # Causal pattern
        pattern = np.random.randn(n, n)
        for col in range(n):
            pattern[:, col][col + 1:] = -np.inf
            valid = pattern[:, col][:col + 1]
            pattern[:, col][:col + 1] = softmax(valid)
            pattern[:, col][col + 1:] = 0

        dots = VGroup()
        for i in range(n):
            for j in range(n):
                v = pattern[i, j]
                if v > 0.05:
                    d = Dot(radius=cell * 0.4 * v)
                    d.set_fill(GREY_B)
                    d.move_to(grid[i * n + j])
                    dots.add(d)

        border = SurroundingRectangle(grid, buff=0.03)
        border.set_stroke(WHITE, 2)
        border.set_fill(BLACK, 0.9)

        self.add(border, grid, dots)


class MultiHeadBasic(Scene):
    """Basic multi-head attention visualization."""

    def construct(self):
        # Title
        title = Text("Multi-Head Attention")
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Create multiple attention heads
        heads = VGroup()
        for i in range(6):
            head = AttentionGrid(n=5, seed=i * 10)
            head.set_height(1.5)
            heads.add(head)

        heads.arrange_in_grid(n_rows=2, n_cols=3, buff=0.5)
        heads.next_to(title, DOWN, buff=0.5)

        # Labels (using Text to avoid LaTeX dependency issues)
        labels = VGroup()
        for i, head in enumerate(heads):
            label = Text(f"Head {i+1}", font_size=18)
            label.set_color(YELLOW)
            label.next_to(head, UP, buff=0.1)
            labels.add(label)

        # Show heads one by one
        self.play(
            LaggedStart(
                *[FadeIn(h, scale=0.8) for h in heads],
                lag_ratio=0.2
            ),
            run_time=3
        )
        self.play(
            LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.1)
        )
        self.wait()

        # Explanation
        explanation = VGroup(
            Text("Each head learns different patterns:", font_size=24),
            Text("• Subject-verb relationships", font_size=20, color=BLUE),
            Text("• Adjective-noun connections", font_size=20, color=GREEN),
            Text("• Positional patterns", font_size=20, color=YELLOW),
        )
        explanation.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        explanation.to_edge(DOWN, buff=0.5)

        self.play(
            LaggedStart(*[Write(e) for e in explanation], lag_ratio=0.3)
        )
        self.wait(2)


class MultiHead3D(Scene):
    """3D multi-head visualization using Scene (simpler)."""

    def construct(self):
        frame = self.camera.frame

        # Title (fixed in frame)
        title = Text("Multi-Head Attention in 3D")
        title.to_edge(UP)
        title.fix_in_frame()
        self.add(title)

        # Create heads
        heads = Group()
        for i in range(8):
            head = AttentionGrid(n=5, seed=i * 7)
            head.set_height(2)
            heads.add(head)

        # Arrange in depth
        heads.arrange(OUT, buff=0.7)
        heads.center()

        # Start with one head
        self.add(heads[-1])
        self.wait()

        # Rotate camera
        self.play(
            frame.animate.set_euler_angles(
                phi=70 * DEGREES,
                theta=-45 * DEGREES
            ),
            run_time=2
        )

        # Show all heads
        self.play(
            LaggedStart(
                *[FadeIn(h, shift=OUT * 0.3) for h in heads[:-1]],
                lag_ratio=0.15
            ),
            run_time=3
        )
        self.wait()

        # Add labels (using Text to avoid LaTeX dependency)
        wq_labels = VGroup()
        for i, head in enumerate(list(heads)[::-1][:4]):
            label = Text(f"H{i+1}", font_size=24, color=YELLOW)
            label.next_to(head, UP, buff=0.2)
            label.rotate(70 * DEGREES, RIGHT)
            label.rotate(-45 * DEGREES, OUT)
            wq_labels.add(label)

        self.play(
            LaggedStart(*[FadeIn(l, shift=UP * 0.2) for l in wq_labels], lag_ratio=0.2)
        )
        self.wait()

        # Rotate around
        self.play(
            frame.animate.increment_theta(60 * DEGREES),
            run_time=4
        )
        self.wait()
