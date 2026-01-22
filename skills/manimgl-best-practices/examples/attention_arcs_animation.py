"""
Attention Arcs Animation - Simple attention flow visualization

Shows how attention connects different positions with animated arcs.
Based on 3Blue1Brown's transformer visualizations.

Run: manimgl attention_arcs_animation.py AttentionArcsAnimation -o
"""
from manimlib import *
import numpy as np
import random


def random_bright_color(hue_range=(0.0, 1.0)):
    """Generate a random bright color within a hue range."""
    hue = random.uniform(*hue_range)
    return Color(hsl=(hue, 0.7, 0.6))


def value_to_color(
    value,
    low_positive_color=BLUE_E,
    high_positive_color=BLUE_B,
    low_negative_color=RED_E,
    high_negative_color=RED_B,
    min_value=0.0,
    max_value=10.0
):
    """Map a value to a color based on its sign and magnitude."""
    alpha = np.clip(float((abs(value) - min_value) / (max_value - min_value)), 0, 1)
    if value >= 0:
        return interpolate_color(low_positive_color, high_positive_color, alpha)
    else:
        return interpolate_color(low_negative_color, high_negative_color, alpha)


class SimpleEmbedding(VGroup):
    """A simple numeric embedding visualization."""

    def __init__(self, length=7, height=2.0, **kwargs):
        super().__init__(**kwargs)

        # Create rectangles for entries
        entries = VGroup()
        for i in range(length):
            value = random.uniform(-9.9, 9.9)
            rect = Rectangle(width=0.3, height=height / length * 0.8)
            color = value_to_color(value)
            rect.set_fill(color, opacity=0.8)
            rect.set_stroke(WHITE, 1)
            entries.add(rect)

        entries.arrange(DOWN, buff=0.05)
        entries.set_height(height)

        # Add brackets
        lb = Tex(r"\left[", font_size=72)
        rb = Tex(r"\right]", font_size=72)
        lb.stretch_to_fit_height(height * 1.1)
        rb.stretch_to_fit_height(height * 1.1)
        lb.next_to(entries, LEFT, buff=0.05)
        rb.next_to(entries, RIGHT, buff=0.05)

        self.add(lb, entries, rb)
        self.entries = entries
        self.brackets = VGroup(lb, rb)


class AttentionArcsAnimation(Scene):
    """
    Demonstrates attention mechanism through animated arcs connecting positions.

    This visualization shows how each position attends to other positions,
    with arc colors and widths representing attention weights.
    """

    def construct(self):
        # Create a row of embeddings
        n_embeddings = 6
        embeddings = VGroup(*(
            SimpleEmbedding(length=8, height=3.0)
            for _ in range(n_embeddings)
        ))
        embeddings.arrange(RIGHT, buff=0.8)
        embeddings.set_width(FRAME_WIDTH - 2)
        embeddings.to_edge(DOWN, buff=1.5)

        # Add position labels
        labels = VGroup(*(
            Text(f"Pos {i}", font_size=24)
            for i in range(n_embeddings)
        ))
        for label, emb in zip(labels, embeddings):
            label.next_to(emb, DOWN, buff=0.2)

        # Title
        title = Text("Attention: How positions communicate", font_size=48)
        title.to_edge(UP)

        # Show initial setup
        self.play(
            Write(title),
            LaggedStartMap(FadeIn, embeddings, shift=0.5 * UP, lag_ratio=0.1),
            run_time=2
        )
        self.play(LaggedStartMap(FadeIn, labels, shift=0.2 * DOWN, lag_ratio=0.1))
        self.wait()

        # Create attention arcs for each position
        self.play_attention_animation(embeddings, run_time=4)
        self.wait()

        # Show focused attention on one position
        focus_label = Text("Each position gathers context from others", font_size=36)
        focus_label.next_to(title, DOWN, buff=0.5)

        self.play(FadeIn(focus_label, shift=DOWN))
        self.play_focused_attention(embeddings, focus_index=3, run_time=3)
        self.wait()

        # Cleanup
        self.play(
            FadeOut(focus_label),
            FadeOut(title),
            FadeOut(labels),
            FadeOut(embeddings),
        )

    def play_attention_animation(self, embeddings, run_time=5):
        """Play attention arcs between all positions."""
        arc_groups = VGroup()

        for _ in range(2):  # Multiple rounds
            for n, e1 in enumerate(embeddings):
                arc_group = VGroup()
                for e2 in embeddings[n + 1:]:
                    sign = (-1) ** int(e2.get_x() > e1.get_x())
                    arc = Line(
                        e1.get_top(), e2.get_top(),
                        path_arc=sign * PI / 3,
                    )
                    arc.set_stroke(
                        color=random_bright_color(hue_range=(0.1, 0.3)),
                        width=5 * random.random() ** 3,
                    )
                    arc_group.add(arc)
                arc_group.shuffle()
                if len(arc_group) > 0:
                    arc_groups.add(arc_group)

        self.play(
            LaggedStart(*(
                AnimationGroup(
                    LaggedStartMap(VShowPassingFlash, arc_group.copy(), time_width=2, lag_ratio=0.15),
                    LaggedStartMap(ShowCreationThenFadeOut, arc_group, lag_ratio=0.15),
                )
                for arc_group in arc_groups
            ), lag_ratio=0.0),
            run_time=run_time
        )

    def play_focused_attention(self, embeddings, focus_index=3, run_time=3):
        """Show attention arcs focused on one position."""
        target = embeddings[focus_index]

        # Highlight target
        rect = SurroundingRectangle(target, buff=0.1)
        rect.set_stroke(YELLOW, 3)

        arcs = VGroup()
        for i, emb in enumerate(embeddings):
            if i == focus_index:
                continue
            sign = 1 if i < focus_index else -1
            arc = Line(
                emb.get_top(), target.get_top(),
                path_arc=sign * PI / 3,
            )
            weight = random.random() ** 2
            arc.set_stroke(
                color=interpolate_color(BLUE_E, YELLOW, weight),
                width=2 + 4 * weight,
            )
            arcs.add(arc)

        self.play(ShowCreation(rect))
        self.play(
            LaggedStart(*(
                ShowCreationThenFadeOut(arc, run_time=1.5)
                for arc in arcs
            ), lag_ratio=0.2),
            run_time=run_time
        )
        self.play(FadeOut(rect))


class AttentionArcs3D(Scene):
    """
    3D version of attention arcs with camera movement.
    """

    def construct(self):
        frame = self.camera.frame

        # Create 3D embeddings as colored columns
        n_embeddings = 5
        columns = Group()

        for i in range(n_embeddings):
            column = Group()
            for j in range(8):
                box = Cube(side_length=0.3)
                box.set_color(value_to_color(random.uniform(-10, 10)))
                box.set_opacity(0.8)
                column.add(box)
            column.arrange(OUT, buff=0.05)
            columns.add(column)

        columns.arrange(RIGHT, buff=1.0)
        columns.center()

        # Set up 3D camera
        frame.set_euler_angles(phi=60 * DEGREES, theta=-30 * DEGREES)
        self.add(columns)

        # Create arcs in 3D
        arcs = VGroup()
        for i, c1 in enumerate(columns):
            for c2 in columns[i + 1:]:
                start = c1.get_top() + 0.2 * UP
                end = c2.get_top() + 0.2 * UP
                mid = (start + end) / 2 + UP

                arc = VMobject()
                arc.set_points_smoothly([start, mid, end])
                arc.set_stroke(
                    random_bright_color(hue_range=(0.1, 0.4)),
                    width=2 + 3 * random.random()
                )
                arcs.add(arc)

        # Animate
        self.play(
            frame.animate.set_euler_angles(phi=70 * DEGREES, theta=-45 * DEGREES),
            run_time=2
        )

        self.play(
            LaggedStartMap(ShowCreation, arcs, lag_ratio=0.1),
            run_time=3
        )

        self.play(
            frame.animate.increment_theta(60 * DEGREES),
            LaggedStartMap(VShowPassingFlash, arcs, time_width=1.5, lag_ratio=0.05),
            run_time=4
        )

        self.play(
            FadeOut(arcs),
            FadeOut(columns),
        )
