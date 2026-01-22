"""
Token to Embedding Visualization

Shows the transformation from text tokens to vector embeddings.
Based on 3Blue1Brown's transformer visualizations.

Run: manimgl token_to_embedding.py TokenToEmbedding -o
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


class SimpleNumericEmbedding(VGroup):
    """A simplified numeric embedding visualization."""

    def __init__(self, length=8, height=2.5, width=0.5, bracket_color=GREY_B, **kwargs):
        super().__init__(**kwargs)

        entries = VGroup()
        entry_height = (height / length) * 0.85

        for _ in range(length):
            value = random.uniform(-9.9, 9.9)
            rect = Rectangle(width=width * 0.8, height=entry_height)
            rect.set_fill(value_to_color(value), opacity=0.9)
            rect.set_stroke(WHITE, 0.5)
            entries.add(rect)

        entries.arrange(DOWN, buff=0.02)
        entries.set_height(height)

        # Brackets
        lb = Text("[", font_size=72)
        rb = Text("]", font_size=72)
        lb.stretch_to_fit_height(height * 1.1)
        rb.stretch_to_fit_height(height * 1.1)
        lb.set_color(bracket_color)
        rb.set_color(bracket_color)
        lb.next_to(entries, LEFT, buff=0.05)
        rb.next_to(entries, RIGHT, buff=0.05)

        self.add(lb, entries, rb)
        self.entries = entries
        self.brackets = VGroup(lb, rb)


class TokenToEmbedding(Scene):
    """
    Demonstrates the conversion of text tokens into vector embeddings.

    Shows how each word/token in a sentence gets converted into
    a numerical vector representation.
    """

    example_text = "The quick brown fox"

    def construct(self):
        # Show the phrase
        phrase = Text(self.example_text, font_size=60)
        phrase.to_edge(UP, buff=1)

        self.play(Write(phrase))
        self.wait()

        # Split into words/tokens
        word_strings = self.example_text.split()
        colors = [BLUE, GREEN, YELLOW, RED]

        word_groups = VGroup()
        for i, word_str in enumerate(word_strings):
            word = phrase[word_str][0]
            rect = SurroundingRectangle(word, buff=0.1)
            rect.set_stroke(colors[i % len(colors)], 2)
            rect.set_fill(colors[i % len(colors)], 0.2)
            word_groups.add(VGroup(rect, word.copy()))

        # Animate word rectangles appearing
        self.play(
            LaggedStart(*(
                DrawBorderThenFill(wg[0])
                for wg in word_groups
            ), lag_ratio=0.2),
            run_time=2
        )
        self.wait()

        # Create embedding vectors
        vectors = VGroup(*(
            SimpleNumericEmbedding(length=10, height=3.0, width=0.6)
            for _ in word_strings
        ))
        vectors.arrange(RIGHT, buff=1.0)
        vectors.set_width(FRAME_WIDTH - 2)
        vectors.to_edge(DOWN, buff=1)

        # Color code the brackets
        for vec, color in zip(vectors, colors):
            vec.brackets.set_color(color)

        # Position token blocks above vectors
        token_blocks = VGroup()
        for i, (wg, vec) in enumerate(zip(word_groups, vectors)):
            block = wg.copy()
            block.set_width(vec.get_width() * 1.2)
            block.next_to(vec, UP, buff=1.5)
            token_blocks.add(block)

        # Create arrows
        arrows = VGroup(*(
            Arrow(block.get_bottom(), vec.get_top(), stroke_width=3, buff=0.1)
            for block, vec in zip(token_blocks, vectors)
        ))
        for arrow, color in zip(arrows, colors):
            arrow.set_color(color)

        # Animate transformation
        self.play(
            ReplacementTransform(
                VGroup(*(wg.copy() for wg in word_groups)),
                token_blocks
            ),
            self.frame.animate.shift(0.5 * DOWN) if hasattr(self, 'frame') else Wait(),
            run_time=2
        )

        self.play(
            LaggedStartMap(GrowArrow, arrows, lag_ratio=0.2),
            LaggedStartMap(FadeIn, vectors, shift=0.5 * DOWN, lag_ratio=0.2),
            run_time=2
        )
        self.wait()

        # Add dimension label
        dim_label = Text("Each vector has d dimensions", font_size=36)
        dim_label.next_to(vectors, DOWN)

        brace = Brace(vectors[0], RIGHT)
        dim_num = brace.get_tex("d = 12288", font_size=30)

        self.play(
            FadeIn(dim_label),
            GrowFromCenter(brace),
            FadeIn(dim_num),
        )
        self.wait(2)

        # Cleanup
        self.play(
            FadeOut(VGroup(
                phrase, word_groups, token_blocks, arrows, vectors,
                dim_label, brace, dim_num
            ))
        )


class EmbeddingArrayVisualization(Scene):
    """
    Shows multiple embeddings arranged as an array/matrix.
    """

    def construct(self):
        # Title
        title = Text("Embedding Array", font_size=56)
        title.to_edge(UP)

        # Create array of embeddings
        n_tokens = 7
        n_dims = 10

        # Create the embedding columns
        columns = VGroup()
        for i in range(n_tokens):
            col = VGroup()
            for j in range(n_dims):
                value = random.uniform(-10, 10)
                rect = Rectangle(width=0.5, height=0.35)
                rect.set_fill(value_to_color(value), opacity=0.9)
                rect.set_stroke(WHITE, 0.5)
                col.add(rect)
            col.arrange(DOWN, buff=0.02)
            columns.add(col)

        columns.arrange(RIGHT, buff=0.3)

        # Add brackets
        left_bracket = Tex(r"\left[", font_size=120)
        right_bracket = Tex(r"\right]", font_size=120)
        left_bracket.stretch_to_fit_height(columns.get_height() * 1.1)
        right_bracket.stretch_to_fit_height(columns.get_height() * 1.1)
        left_bracket.next_to(columns, LEFT, buff=0.1)
        right_bracket.next_to(columns, RIGHT, buff=0.1)

        array = VGroup(left_bracket, columns, right_bracket)
        array.center()

        # Token labels
        token_labels = VGroup(*(
            Text(f"t{i}", font_size=24)
            for i in range(n_tokens)
        ))
        for label, col in zip(token_labels, columns):
            label.next_to(col, UP, buff=0.3)

        # Dimension label
        dim_brace = Brace(columns[0], LEFT)
        dim_label = dim_brace.get_text("d", font_size=36)

        # Animate
        self.play(Write(title))

        self.play(
            LaggedStartMap(FadeIn, columns, shift=0.3 * DOWN, lag_ratio=0.1),
            run_time=2
        )

        self.play(
            FadeIn(left_bracket, shift=0.2 * LEFT),
            FadeIn(right_bracket, shift=0.2 * RIGHT),
        )

        self.play(LaggedStartMap(FadeIn, token_labels, shift=0.2 * DOWN, lag_ratio=0.1))

        self.play(
            GrowFromCenter(dim_brace),
            FadeIn(dim_label),
        )
        self.wait()

        # Highlight one column
        highlight_rect = SurroundingRectangle(columns[3], buff=0.1)
        highlight_rect.set_stroke(YELLOW, 3)

        self.play(ShowCreation(highlight_rect))
        self.wait()

        # Show context note
        context_note = Text(
            "Each column encodes one token's meaning + context",
            font_size=30
        )
        context_note.next_to(array, DOWN, buff=1)

        self.play(FadeIn(context_note, shift=UP))
        self.wait(2)

        # Cleanup
        self.play(FadeOut(VGroup(
            title, array, token_labels, dim_brace, dim_label,
            highlight_rect, context_note
        )))
