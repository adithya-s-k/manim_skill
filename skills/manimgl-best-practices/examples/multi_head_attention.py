"""
Multi-Head Attention Visualization - Native ManimGL

This is the proper ManimGL implementation using native 3D features.
Based on 3b1b's transformer visualization style.

Run with: manimgl multi_head_attention.py MultiHeadedAttention
Interactive: manimgl multi_head_attention.py MultiHeadedAttention -se 30
"""
from manimlib import *
import numpy as np


def softmax(logits, temperature=1.0):
    """Numerically stable softmax."""
    logits = np.array(logits)
    logits = logits - np.max(logits)
    exps = np.exp(logits / max(temperature, 1e-10))
    return exps / np.sum(exps)


class AttentionPatternGrid(VGroup):
    """A grid showing attention pattern with dots."""

    def __init__(self, n_rows=8, seed=None, **kwargs):
        super().__init__(**kwargs)

        if seed is not None:
            np.random.seed(seed)

        cell_size = 0.4

        # Create grid of squares
        self.grid = VGroup()
        for i in range(n_rows):
            for j in range(n_rows):
                cell = Square(side_length=cell_size)
                cell.set_stroke(WHITE, 0.5, opacity=0.3)
                cell.move_to(np.array([j * cell_size, -i * cell_size, 0]))
                self.grid.add(cell)

        self.grid.center()

        # Generate causal attention pattern
        pattern = np.random.normal(0, 1, (n_rows, n_rows))
        for n in range(n_rows):
            pattern[:, n][n + 1:] = -np.inf
            valid = pattern[:, n][pattern[:, n] > -np.inf]
            if len(valid) > 0:
                pattern[:, n][:n + 1] = softmax(valid)
            pattern[:, n][n + 1:] = 0
        pattern = np.nan_to_num(pattern, nan=0.0)

        # Add dots based on weights
        self.dots = VGroup()
        for i in range(n_rows):
            for j in range(n_rows):
                value = pattern[i, j]
                if value > 0.05:
                    dot = Dot(radius=cell_size * 0.4 * value)
                    dot.set_fill(GREY_B, 1)
                    dot.move_to(self.grid[i * n_rows + j].get_center())
                    self.dots.add(dot)

        # Border
        self.border = SurroundingRectangle(self.grid, buff=0.05)
        self.border.set_stroke(WHITE, 2)
        self.border.set_fill(BLACK, 0.9)

        self.add(self.border, self.grid, self.dots)


class MultiHeadedAttention(InteractiveScene):
    """
    Multi-Head Attention visualization in native ManimGL.
    Shows multiple attention heads in 3D space with camera movement.
    """

    def construct(self):
        # Background
        background = FullScreenRectangle()
        background.set_fill(GREY_E, 1)
        background.fix_in_frame()
        self.add(background)

        # Title animation: Single head -> Multi-headed
        single_title = Text("Single head of attention")
        multiple_title = Text("Multi-headed attention")

        for title in [single_title, multiple_title]:
            title.scale(1.25)
            title.to_edge(UP)

        self.add(single_title)
        self.wait()

        # Flash around "head"
        head = single_title["head"][0]
        self.play(
            FlashAround(head, run_time=2),
            head.animate.set_color(YELLOW),
        )
        self.wait()

        # Transform title
        kw = dict(path_arc=45 * DEGREES)
        self.play(
            FadeTransform(single_title["Single"], multiple_title["Multi-"], **kw),
            FadeTransform(single_title["head"], multiple_title["head"], **kw),
            FadeIn(multiple_title["ed"], 0.25 * RIGHT),
            FadeTransform(single_title["attention"], multiple_title["attention"], **kw),
            FadeOut(single_title["of"])
        )
        self.add(multiple_title)
        self.wait()

        # Create attention pattern heads
        n_heads = 15
        heads = Group()

        for n in range(n_heads):
            pattern = AttentionPatternGrid(n_rows=6, seed=n * 42)
            pattern.set_height(4)
            heads.add(pattern)

        # Arrange in 3D depth
        self.set_floor_plane("xz")
        frame = self.camera.frame
        multiple_title.fix_in_frame()

        heads.arrange(OUT, buff=1.0)
        heads.move_to(DOWN)

        # Show initial pattern
        pre_head = heads[-1].copy()
        pre_head.move_to(DOWN)

        self.add(pre_head)
        self.wait()

        # Rotate camera to reveal 3D
        self.play(
            frame.animate.reorient(41, -12, 0, (-1.0, -1.42, 1.09), 12.90).set_anim_args(run_time=2),
            background.animate.set_fill(opacity=0.75),
            FadeTransform(pre_head, heads[-1], time_span=(1, 2)),
        )

        # Fan out all heads
        self.play(
            frame.animate.reorient(48, -11, 0, (-1.0, -1.42, 1.09), 12.90),
            LaggedStart(
                *(FadeTransform(heads[-1].copy(), image) for image in heads),
                lag_ratio=0.1,
                group_type=Group,
            ),
            run_time=4,
        )
        self.add(heads)
        self.wait()

        # Add matrix labels W_Q, W_K, W_V for visible heads
        colors = [YELLOW, TEAL, RED, PINK]
        tex_labels = ["W_Q", "W_K", R"\downarrow W_V", R"\uparrow W_V"]
        n_shown = 9

        sym_groups = VGroup()
        for tex, color in zip(tex_labels[:2], colors[:2]):  # Just W_Q and W_K for now
            syms = VGroup()
            for n, image in enumerate(list(heads)[:-n_shown - 1:-1], start=1):
                sym = Tex(tex + f"^{{({n})}}", font_size=36)
                sym.next_to(image, UP, MED_SMALL_BUFF)
                sym.set_color(color)
                sym.set_backstroke(BLACK, 5)
                syms.add(sym)
            sym_groups.add(syms)

        # Rotate labels to face camera
        sym_rot_angle = 70 * DEGREES
        for syms in sym_groups:
            syms.align_to(heads, LEFT)
            for sym in syms:
                sym.rotate(sym_rot_angle, UP)

        # Show W_Q labels
        self.play(
            LaggedStartMap(FadeIn, sym_groups[0], shift=0.2 * UP, lag_ratio=0.25),
            frame.animate.reorient(59, -7, 0, (-1.62, 0.25, 1.29), 14.18),
            run_time=2,
        )

        # Show W_K labels
        self.play(
            LaggedStartMap(FadeIn, sym_groups[1], shift=0.2 * UP, lag_ratio=0.1),
            sym_groups[0].animate.shift(0.75 * UP),
            run_time=1,
        )
        self.wait()

        # Add brace showing "96 heads"
        depth = heads.get_depth()
        brace = Brace(Line(LEFT, RIGHT).set_width(0.5 * depth), UP).scale(2)
        brace_label = brace.get_text("96", font_size=96, buff=MED_SMALL_BUFF)
        brace_group = VGroup(brace, brace_label)
        brace_group.rotate(PI / 2, UP)
        brace_group.next_to(heads, UP, buff=MED_LARGE_BUFF)

        self.add(brace, brace_label, sym_groups)
        self.play(
            frame.animate.reorient(62, -6, 0, (-0.92, -0.08, -0.51), 14.18).set_anim_args(run_time=5),
            GrowFromCenter(brace),
            sym_groups.animate.set_fill(opacity=0.5).set_stroke(width=0),
            FadeIn(brace_label, 0.5 * UP, time_span=(0.5, 1.5)),
        )
        self.wait()

        # Return to front view
        self.play(
            frame.animate.reorient(0, 0, 0, ORIGIN, FRAME_HEIGHT).set_anim_args(run_time=2),
            FadeOut(multiple_title, UP),
            FadeOut(brace_group),
            FadeOut(sym_groups),
        )
        self.wait()


class SimpleMultiHead(InteractiveScene):
    """Simpler version for quick testing."""

    def construct(self):
        # Title
        title = Text("Multi-Head Attention", font_size=48)
        title.to_edge(UP)
        title.fix_in_frame()
        self.add(title)

        # Create heads
        heads = Group()
        for i in range(8):
            pattern = AttentionPatternGrid(n_rows=5, seed=i * 10)
            pattern.set_height(2)
            heads.add(pattern)

        # Arrange in 3D
        heads.arrange(OUT, buff=0.5)
        heads.move_to(ORIGIN)

        frame = self.camera.frame

        # Show one, then fan out
        self.add(heads[-1])
        self.wait()

        self.play(
            frame.animate.reorient(50, -20, 0),
            run_time=2
        )

        self.play(
            LaggedStart(
                *[FadeIn(h, shift=OUT * 0.3) for h in heads[:-1]],
                lag_ratio=0.2
            ),
            run_time=2
        )
        self.wait()

        # Rotate around
        self.play(
            frame.animate.reorient(50, 60, 0),
            run_time=4
        )
        self.wait()
