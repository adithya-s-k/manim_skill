"""
Network Block Flow - 3D visualization of data flowing through network blocks

Shows data moving through attention and MLP blocks as 3D cubes.
Based on 3Blue1Brown's transformer visualizations.

Run: manimgl network_block_flow.py NetworkBlockFlow3D -o
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
    """Map a value to a color based on its sign and magnitude."""
    alpha = np.clip(float((abs(value) - min_value) / (max_value - min_value)), 0, 1)
    if value >= 0:
        return interpolate_color(low_positive_color, high_positive_color, alpha)
    else:
        return interpolate_color(low_negative_color, high_negative_color, alpha)


def random_bright_color(hue_range=(0.0, 1.0)):
    """Generate a random bright color within a hue range."""
    hue = random.uniform(*hue_range)
    return Color(hsl=(hue, 0.7, 0.6))


class SimpleEmbeddingColumn(VGroup):
    """A simple 3D-style embedding column."""

    def __init__(self, n_entries=8, height=3.0, width=0.4, **kwargs):
        super().__init__(**kwargs)

        entries = VGroup()
        entry_height = height / n_entries * 0.85

        for _ in range(n_entries):
            value = random.uniform(-10, 10)
            rect = Rectangle(width=width, height=entry_height)
            rect.set_fill(value_to_color(value), opacity=0.9)
            rect.set_stroke(WHITE, 1)
            entries.add(rect)

        entries.arrange(DOWN, buff=0.02)
        self.add(entries)
        self.entries = entries

    def randomize_values(self):
        for entry in self.entries:
            value = random.uniform(-10, 10)
            entry.set_fill(value_to_color(value), opacity=0.9)
        return self


class NetworkBlockFlow3D(Scene):
    """
    3D visualization of data flowing through transformer blocks.

    Shows embeddings passing through attention and MLP blocks,
    represented as 3D cubes that process the data.
    """

    def construct(self):
        frame = self.camera.frame

        # Setup 3D view
        frame.set_euler_angles(phi=65 * DEGREES, theta=-40 * DEGREES)
        frame.set_z(2)

        # Create input embeddings
        n_tokens = 5
        embeddings = VGroup(*(
            SimpleEmbeddingColumn(n_entries=10, height=3.5, width=0.5)
            for _ in range(n_tokens)
        ))
        embeddings.arrange(RIGHT, buff=0.6)
        embeddings.set_z(0)

        # Title
        title = Text("Data Flow Through Network Blocks", font_size=48)
        title.to_edge(UP)
        title.fix_in_frame()

        self.play(
            Write(title),
            LaggedStartMap(FadeIn, embeddings, shift=0.5 * DOWN, lag_ratio=0.1),
            run_time=2
        )
        self.wait()

        # Create and show first block (Attention)
        att_block = self.create_block(embeddings, "Attention", BLUE_E)

        self.play(
            frame.animate.reorient(-50, -15, 0).shift(2 * OUT),
            FadeIn(att_block, scale=0.8),
            run_time=2
        )

        # Flow through attention
        new_embeddings = self.flow_through_block(embeddings, att_block)

        # Create second block (MLP/Feedforward)
        mlp_block = self.create_block(new_embeddings, "Feedforward", GREEN_E)
        mlp_block.shift(3 * OUT)

        self.play(
            frame.animate.shift(2 * OUT),
            FadeIn(mlp_block, scale=0.8),
            run_time=2
        )

        # Flow through MLP
        final_embeddings = self.flow_through_block(new_embeddings, mlp_block)

        # Show "many more" indication
        self.show_repetition_hint(mlp_block, frame)

        # Cleanup
        self.play(
            FadeOut(VGroup(embeddings, new_embeddings, final_embeddings)),
            FadeOut(att_block),
            FadeOut(mlp_block),
            FadeOut(title),
        )

    def create_block(self, layer, title_text, color):
        """Create a processing block (cube) next to the layer."""
        body = Cube(color=color, opacity=0.7)
        body.set_shading(0.5, 0.5, 0.0)

        width = layer.get_width() + 1
        height = layer.get_height() + 0.5
        depth = 2.0

        body.set_shape(width, height, depth)
        body.next_to(layer, OUT, buff=1.0)

        title = Text(title_text, font_size=60)
        title.set_backstroke(BLACK, 3)
        title.rotate(PI / 2, RIGHT)
        title.next_to(body, UP, buff=0.2)

        block = Group(body, title)
        block.body = body
        block.title = title

        return block

    def flow_through_block(self, embeddings, block):
        """Animate embeddings flowing through the block."""
        # Create output embeddings
        new_embeddings = VGroup(*(
            SimpleEmbeddingColumn(n_entries=10, height=3.5, width=0.5)
            for _ in range(len(embeddings))
        ))
        new_embeddings.arrange(RIGHT, buff=0.6)
        new_embeddings.move_to(block.body.get_center())
        new_embeddings.set_z(block.body.get_z(OUT) + 1)

        # Animate transformation
        self.play(
            TransformFromCopy(embeddings, new_embeddings),
            run_time=2
        )

        return new_embeddings

    def show_repetition_hint(self, last_block, frame):
        """Show indication of many more blocks."""
        dots = Text("...", font_size=120)
        dots.rotate(PI / 2, RIGHT)
        dots.next_to(last_block, OUT, buff=1)

        brace = Brace(Line(ORIGIN, 4 * OUT), RIGHT)
        brace.rotate(PI / 2, RIGHT)
        brace.next_to(dots, RIGHT)

        label = Text("Many\nrepetitions", font_size=36)
        label.rotate(PI / 2, RIGHT)
        label.next_to(brace, RIGHT)

        hint_group = VGroup(dots, brace, label)

        self.play(
            frame.animate.shift(2 * OUT),
            FadeIn(dots),
            GrowFromCenter(brace),
            FadeIn(label),
            run_time=2
        )
        self.wait(2)
        self.play(FadeOut(hint_group))


class SimpleBlockTransition(Scene):
    """
    Simpler 2D version showing block transitions.
    """

    def construct(self):
        # Create token representations
        n_tokens = 6
        tokens = VGroup()

        for i in range(n_tokens):
            token = VGroup()
            # Colored rectangle
            rect = Rectangle(width=0.8, height=2.5)
            rect.set_fill(BLUE, opacity=0.3)
            rect.set_stroke(BLUE, 2)

            # Inner value indicators
            for j in range(5):
                small_rect = Rectangle(width=0.6, height=0.35)
                small_rect.set_fill(value_to_color(random.uniform(-10, 10)), opacity=0.8)
                small_rect.set_stroke(WHITE, 0.5)
                token.add(small_rect)
            token.arrange(DOWN, buff=0.05)

            tokens.add(token)

        tokens.arrange(RIGHT, buff=0.5)
        tokens.to_edge(LEFT, buff=1)

        # Block representations
        att_block = self.create_2d_block("Attention", BLUE_D)
        mlp_block = self.create_2d_block("Feedforward", GREEN_D)

        att_block.next_to(tokens, RIGHT, buff=1.5)
        mlp_block.next_to(att_block, RIGHT, buff=2)

        # Arrows
        arrow1 = Arrow(tokens.get_right(), att_block.get_left(), buff=0.2)
        arrow2 = Arrow(att_block.get_right(), mlp_block.get_left(), buff=0.2)

        # Labels
        input_label = Text("Input\nEmbeddings", font_size=24)
        input_label.next_to(tokens, DOWN)

        # Animate
        self.play(LaggedStartMap(FadeIn, tokens, shift=UP, lag_ratio=0.1))
        self.play(FadeIn(input_label))
        self.wait()

        self.play(
            GrowArrow(arrow1),
            FadeIn(att_block, shift=RIGHT),
        )
        self.wait()

        self.play(
            GrowArrow(arrow2),
            FadeIn(mlp_block, shift=RIGHT),
        )
        self.wait()

        # Show data flow animation
        for _ in range(2):
            self.play(
                VShowPassingFlash(arrow1.copy().set_stroke(YELLOW, 4), time_width=0.5),
                VShowPassingFlash(arrow2.copy().set_stroke(YELLOW, 4), time_width=0.5),
                run_time=1.5
            )

        self.wait()

    def create_2d_block(self, label_text, color):
        """Create a 2D block representation."""
        rect = RoundedRectangle(width=2.5, height=3, corner_radius=0.2)
        rect.set_fill(color, opacity=0.5)
        rect.set_stroke(color, 3)

        label = Text(label_text, font_size=28)
        label.move_to(rect)

        return VGroup(rect, label)
