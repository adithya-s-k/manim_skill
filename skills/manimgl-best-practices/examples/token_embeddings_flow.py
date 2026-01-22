"""
Token Embeddings Flow Visualization
Shows tokens being converted to embeddings and then updated through attention.
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
    """Map a value to a color based on sign and magnitude."""
    alpha = clip(float(inverse_interpolate(min_value, max_value, abs(value))), 0, 1)
    if value >= 0:
        return interpolate_color(low_positive_color, high_positive_color, alpha)
    else:
        return interpolate_color(low_negative_color, high_negative_color, alpha)


class NumericEmbedding(DecimalMatrix):
    """A column vector (embedding) with color-coded entries."""
    def __init__(
        self,
        values=None,
        length=7,
        value_range=(-9.9, 9.9),
        ellipses_row=-2,
        num_decimal_places=1,
        bracket_h_buff=0.1,
        **kwargs
    ):
        if values is None:
            values = np.random.uniform(*value_range, size=(length, 1))
        elif len(values.shape) == 1:
            values = values.reshape((values.shape[0], 1))

        self.value_range = value_range

        super().__init__(
            values,
            num_decimal_places=num_decimal_places,
            bracket_h_buff=bracket_h_buff,
            decimal_config=dict(include_sign=True),
            ellipses_row=ellipses_row,
            ellipses_col=None,
        )
        self.reset_entry_colors()

    def reset_entry_colors(self):
        for entry in self.get_entries():
            entry.set_fill(color=value_to_color(
                entry.get_value(),
                low_positive_color=GREY_C,
                high_positive_color=WHITE,
                low_negative_color=GREY_C,
                high_negative_color=WHITE,
                min_value=0,
                max_value=max(self.value_range),
            ))
        return self


class TokenEmbeddingsFlow(InteractiveScene):
    def construct(self):
        # Create sentence
        phrase = "a fluffy blue creature"
        phrase_mob = Text(phrase, font_size=42)
        phrase_mob.to_edge(UP, buff=1)

        words = phrase.split()
        word_mobs = VGroup()
        for word in words:
            word_mob = phrase_mob[word][0]
            word_mobs.add(word_mob)

        self.play(
            LaggedStartMap(FadeIn, word_mobs, shift=0.5 * UP, lag_ratio=0.15)
        )
        self.wait()

        # Create colored rectangles around words
        colors = [GREY, TEAL, BLUE, ORANGE]
        rects = VGroup()
        for word_mob, color in zip(word_mobs, colors):
            rect = SurroundingRectangle(word_mob, buff=0.1)
            rect.set_stroke(color, 2)
            rect.set_fill(color, 0.2)
            rects.add(rect)

        self.play(LaggedStartMap(DrawBorderThenFill, rects, lag_ratio=0.1))
        self.wait()

        # Create embeddings below each word
        np.random.seed(42)
        embeddings = VGroup(
            NumericEmbedding(length=8).set_height(2.5)
            for _ in word_mobs
        )
        embeddings.arrange(RIGHT, buff=0.6)
        embeddings.next_to(rects, DOWN, buff=1.5)

        # Arrows from words to embeddings
        arrows = VGroup(
            Arrow(rect.get_bottom(), emb.get_top(), buff=0.15)
            for rect, emb in zip(rects, embeddings)
        )

        # Labels for embeddings
        e_template = Tex(R"\vec{\textbf{E}}_0", font_size=36)
        e_subscript = e_template.make_number_changeable("0")
        e_labels = VGroup()
        for n, emb in enumerate(embeddings, start=1):
            e_subscript.set_value(n)
            label = e_template.copy()
            label.set_color(GREY_A)
            label.next_to(emb, DOWN, buff=0.3)
            e_labels.add(label)

        self.play(
            LaggedStartMap(GrowArrow, arrows, lag_ratio=0.1),
            LaggedStartMap(FadeIn, embeddings, shift=0.5 * DOWN, lag_ratio=0.1),
            LaggedStartMap(FadeIn, e_labels, shift=0.2 * DOWN, lag_ratio=0.1),
            run_time=2
        )
        self.wait()

        # Show attention arrows (adjectives -> noun)
        # fluffy -> creature, blue -> creature
        attention_arrows = VGroup(
            Arrow(
                embeddings[1].get_top() + 0.3 * UP,
                embeddings[3].get_top() + 0.3 * UP,
                path_arc=-120 * DEGREES,
                buff=0.1
            ).set_stroke(TEAL, 3),
            Arrow(
                embeddings[2].get_top() + 0.3 * UP,
                embeddings[3].get_top() + 0.3 * UP,
                path_arc=-90 * DEGREES,
                buff=0.1
            ).set_stroke(BLUE, 3),
        )

        attention_label = Text("Attention", font_size=30)
        attention_label.next_to(attention_arrows, UP, buff=0.2)
        attention_label.set_color(YELLOW)

        self.play(
            LaggedStartMap(ShowCreation, attention_arrows, lag_ratio=0.3),
            FadeIn(attention_label, shift=0.2 * DOWN),
            run_time=1.5
        )
        self.wait()

        # Show updated embedding for "creature"
        updated_emb = embeddings[3].copy()
        updated_emb.set_color(YELLOW)
        prime = Tex("'", font_size=48)
        prime.next_to(e_labels[3], RIGHT, buff=0)
        prime.shift(0.1 * UL)
        prime.set_color(YELLOW)

        update_label = Text("Updated with context!", font_size=28)
        update_label.set_color(YELLOW)
        update_label.next_to(embeddings[3], RIGHT, buff=0.5)

        # Animate the update
        self.play(
            embeddings[3].animate.set_color(YELLOW),
            FadeIn(prime),
            Write(update_label),
            run_time=1.5
        )
        self.wait()

        # Final message
        final_message = Text(
            "Now 'creature' knows about 'fluffy' and 'blue'",
            font_size=32
        )
        final_message.to_edge(DOWN)

        self.play(Write(final_message))
        self.wait(2)
