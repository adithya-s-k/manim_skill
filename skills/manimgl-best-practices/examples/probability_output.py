"""
Probability Output Visualization

Shows how the network produces probability distributions over possible next tokens.
Based on 3Blue1Brown's transformer visualizations.

Run: manimgl probability_output.py ProbabilityOutput -o
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


def softmax(logits, temperature=1.0):
    """Compute softmax of logits."""
    logits = np.array(logits) / temperature
    logits = logits - np.max(logits)
    exps = np.exp(logits)
    return exps / np.sum(exps)


class ProbabilityOutput(Scene):
    """
    Demonstrates how the final layer outputs probability distributions.

    Shows the transformation from embedding vector to probabilities over vocabulary.
    """

    # Example predictions
    possible_next_tokens = [
        ("the", 0.35),
        ("a", 0.25),
        ("an", 0.15),
        ("this", 0.10),
        ("that", 0.08),
        ("some", 0.04),
        ("my", 0.02),
        ("...", 0.01),
    ]

    def construct(self):
        # Title
        title = Text("Network Output: Probability Distribution", font_size=44)
        title.to_edge(UP)

        self.play(Write(title))
        self.wait()

        # Show the prompt
        prompt = Text('Input: "The cat sat on"', font_size=36)
        prompt.next_to(title, DOWN, buff=0.5)

        self.play(FadeIn(prompt, shift=DOWN))
        self.wait()

        # Create final embedding vector
        vector = self.create_embedding_vector()
        vector.to_edge(LEFT, buff=1.5)
        vector.shift(0.5 * DOWN)

        vector_label = Text("Final\nembedding", font_size=24)
        vector_label.next_to(vector, DOWN)

        self.play(
            FadeIn(vector, shift=RIGHT),
            FadeIn(vector_label),
        )
        self.wait()

        # Arrow to probabilities
        arrow = Arrow(vector.get_right(), vector.get_right() + 2 * RIGHT, buff=0.2)
        arrow.set_color(YELLOW)

        softmax_label = Text("softmax", font_size=28)
        softmax_label.next_to(arrow, UP, buff=0.1)

        self.play(
            GrowArrow(arrow),
            FadeIn(softmax_label),
        )

        # Create probability bars
        prob_group = self.create_probability_bars()
        prob_group.next_to(arrow, RIGHT, buff=0.5)

        self.play(
            LaggedStartMap(FadeIn, prob_group, shift=0.3 * RIGHT, lag_ratio=0.1),
            run_time=2
        )
        self.wait()

        # Highlight top prediction
        highlight = SurroundingRectangle(prob_group[0], buff=0.1)
        highlight.set_stroke(GREEN, 3)

        prediction_label = Text('Prediction: "the"', font_size=36, color=GREEN)
        prediction_label.next_to(prob_group, DOWN, buff=0.8)

        self.play(ShowCreation(highlight))
        self.play(FadeIn(prediction_label, shift=UP))
        self.wait()

        # Show this is a distribution
        dist_note = Text("This is a probability distribution over ~50,000 tokens", font_size=28)
        dist_note.next_to(prediction_label, DOWN, buff=0.5)

        self.play(FadeIn(dist_note, shift=UP))
        self.wait(2)

        # Cleanup
        self.play(FadeOut(VGroup(
            title, prompt, vector, vector_label,
            arrow, softmax_label, prob_group,
            highlight, prediction_label, dist_note
        )))

    def create_embedding_vector(self, length=12, height=4.0):
        """Create a visual embedding vector."""
        entries = VGroup()
        entry_height = (height / length) * 0.85

        for _ in range(length):
            value = random.uniform(-9.9, 9.9)
            rect = Rectangle(width=0.4, height=entry_height)
            rect.set_fill(value_to_color(value), opacity=0.9)
            rect.set_stroke(WHITE, 0.5)
            entries.add(rect)

        entries.arrange(DOWN, buff=0.02)

        # Brackets
        lb = Text("[", font_size=96)
        rb = Text("]", font_size=96)
        lb.stretch_to_fit_height(height * 1.1)
        rb.stretch_to_fit_height(height * 1.1)
        lb.set_color(GREY_B)
        rb.set_color(GREY_B)
        lb.next_to(entries, LEFT, buff=0.05)
        rb.next_to(entries, RIGHT, buff=0.05)

        return VGroup(lb, entries, rb)

    def create_probability_bars(self):
        """Create probability bar chart."""
        bars_group = VGroup()

        for word, prob in self.possible_next_tokens:
            # Bar
            bar = Rectangle(
                width=4 * prob,
                height=0.4,
            )
            bar.set_fill(interpolate_color(BLUE_E, BLUE_B, prob), opacity=0.8)
            bar.set_stroke(WHITE, 1)

            # Word label
            word_label = Text(word, font_size=24)
            word_label.next_to(bar, LEFT, buff=0.2)

            # Probability label
            prob_label = Text(f"{prob:.0%}", font_size=20)
            prob_label.next_to(bar, RIGHT, buff=0.1)

            row = VGroup(word_label, bar, prob_label)
            bars_group.add(row)

        bars_group.arrange(DOWN, buff=0.15, aligned_edge=LEFT)

        # Align bars
        for row in bars_group:
            row[1].align_to(bars_group[0][1], LEFT)

        return bars_group


class SoftmaxVisualization(Scene):
    """
    Shows the softmax transformation turning logits into probabilities.
    """

    def construct(self):
        # Title
        title = Text("Softmax: Logits to Probabilities", font_size=48)
        title.to_edge(UP)

        self.play(Write(title))

        # Create logits
        logits = [2.5, 1.8, 1.2, 0.5, 0.1, -0.3, -1.0, -2.0]
        probs = softmax(logits)

        # Logits bars
        logit_bars = self.create_bars(logits, max_val=3.0, color=RED)
        logit_bars.to_edge(LEFT, buff=1)

        logit_label = Text("Logits (raw scores)", font_size=28)
        logit_label.next_to(logit_bars, DOWN)

        # Probability bars
        prob_bars = self.create_bars(probs * 10, max_val=10, color=BLUE)
        prob_bars.to_edge(RIGHT, buff=1)

        prob_label = Text("Probabilities", font_size=28)
        prob_label.next_to(prob_bars, DOWN)

        # Arrow with softmax
        arrow = Arrow(logit_bars.get_right(), prob_bars.get_left(), buff=0.3)
        softmax_text = Tex(r"\text{softmax}", font_size=36)
        softmax_text.next_to(arrow, UP)

        # Animate
        self.play(FadeIn(logit_bars, shift=RIGHT))
        self.play(FadeIn(logit_label))
        self.wait()

        self.play(
            GrowArrow(arrow),
            FadeIn(softmax_text),
        )

        self.play(TransformFromCopy(logit_bars, prob_bars))
        self.play(FadeIn(prob_label))
        self.wait()

        # Show formula
        formula = Tex(
            r"\text{softmax}(x_i) = \frac{e^{x_i}}{\sum_j e^{x_j}}",
            font_size=36
        )
        formula.next_to(arrow, DOWN, buff=1)

        self.play(Write(formula))
        self.wait(2)

        # Cleanup
        self.play(FadeOut(VGroup(
            title, logit_bars, logit_label,
            arrow, softmax_text, prob_bars, prob_label, formula
        )))

    def create_bars(self, values, max_val=1.0, color=BLUE):
        """Create a group of horizontal bars."""
        bars = VGroup()

        for val in values:
            # Normalize width
            width = max(0.1, abs(val) / max_val * 3)

            bar = Rectangle(width=width, height=0.3)
            if val >= 0:
                bar.set_fill(color, opacity=0.7)
            else:
                bar.set_fill(RED, opacity=0.7)
            bar.set_stroke(WHITE, 1)
            bars.add(bar)

        bars.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        return bars


class VocabProjection(Scene):
    """
    Shows the unembedding matrix projecting to vocabulary space.
    """

    def construct(self):
        # Title
        title = Text("Projecting to Vocabulary Space", font_size=44)
        title.to_edge(UP)

        self.play(Write(title))

        # Embedding vector (small)
        emb_entries = VGroup(*(
            Rectangle(width=0.3, height=0.25).set_fill(
                value_to_color(random.uniform(-10, 10)), opacity=0.9
            ).set_stroke(WHITE, 0.5)
            for _ in range(10)
        ))
        emb_entries.arrange(DOWN, buff=0.02)

        emb_bracket_l = Text("[", font_size=72).stretch_to_fit_height(emb_entries.get_height() * 1.1)
        emb_bracket_r = Text("]", font_size=72).stretch_to_fit_height(emb_entries.get_height() * 1.1)
        emb_bracket_l.next_to(emb_entries, LEFT, buff=0.05)
        emb_bracket_r.next_to(emb_entries, RIGHT, buff=0.05)

        embedding = VGroup(emb_bracket_l, emb_entries, emb_bracket_r)
        embedding.scale(0.8)
        embedding.to_edge(LEFT, buff=1)
        embedding.shift(0.5 * DOWN)

        emb_label = Text("Embedding\n(d dims)", font_size=24)
        emb_label.next_to(embedding, DOWN)

        # Matrix (wide)
        matrix = self.create_matrix(rows=8, cols=10)
        matrix.next_to(embedding, RIGHT, buff=1)

        matrix_label = Text("Unembedding\nMatrix", font_size=24)
        matrix_label.next_to(matrix, DOWN)

        # Result (vocab sized)
        result_entries = VGroup(*(
            Rectangle(width=0.25, height=0.2).set_fill(
                value_to_color(random.uniform(-10, 10)), opacity=0.9
            ).set_stroke(WHITE, 0.5)
            for _ in range(8)
        ))
        result_entries.arrange(DOWN, buff=0.02)

        result_bracket_l = Text("[", font_size=72).stretch_to_fit_height(result_entries.get_height() * 1.1)
        result_bracket_r = Text("]", font_size=72).stretch_to_fit_height(result_entries.get_height() * 1.1)
        result_bracket_l.next_to(result_entries, LEFT, buff=0.05)
        result_bracket_r.next_to(result_entries, RIGHT, buff=0.05)

        result = VGroup(result_bracket_l, result_entries, result_bracket_r)
        result.scale(0.8)
        result.next_to(matrix, RIGHT, buff=0.8)

        result_label = Text("Logits\n(~50k)", font_size=24)
        result_label.next_to(result, DOWN)

        # Multiply symbol
        times = Tex(r"\times", font_size=48)
        times.move_to(midpoint(embedding.get_right(), matrix.get_left()))

        equals = Tex("=", font_size=48)
        equals.move_to(midpoint(matrix.get_right(), result.get_left()))

        # Animate
        self.play(FadeIn(embedding, shift=RIGHT), FadeIn(emb_label))
        self.play(FadeIn(times))
        self.play(FadeIn(matrix, scale=0.9), FadeIn(matrix_label))
        self.play(FadeIn(equals))
        self.play(FadeIn(result, shift=LEFT), FadeIn(result_label))
        self.wait()

        # Formula
        formula = Tex(r"W_U \cdot \text{emb} = \text{logits}", font_size=36)
        formula.next_to(VGroup(embedding, matrix, result), UP, buff=0.8)

        self.play(Write(formula))
        self.wait(2)

        # Cleanup
        self.play(FadeOut(VGroup(
            title, embedding, emb_label, times, matrix, matrix_label,
            equals, result, result_label, formula
        )))

    def create_matrix(self, rows=6, cols=8):
        """Create a visual matrix."""
        entries = VGroup()

        for i in range(rows):
            row = VGroup()
            for j in range(cols):
                value = random.uniform(-10, 10)
                rect = Rectangle(width=0.25, height=0.25)
                rect.set_fill(value_to_color(value), opacity=0.8)
                rect.set_stroke(WHITE, 0.3)
                row.add(rect)
            row.arrange(RIGHT, buff=0.02)
            entries.add(row)

        entries.arrange(DOWN, buff=0.02)

        # Brackets
        lb = Text("[", font_size=72)
        rb = Text("]", font_size=72)
        lb.stretch_to_fit_height(entries.get_height() * 1.1)
        rb.stretch_to_fit_height(entries.get_height() * 1.1)
        lb.next_to(entries, LEFT, buff=0.05)
        rb.next_to(entries, RIGHT, buff=0.05)

        return VGroup(lb, entries, rb)
