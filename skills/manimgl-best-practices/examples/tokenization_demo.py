"""
Tokenization Visualization Demo
Shows how text gets broken into tokens with colored rectangles.

Based on: videos/_2024/transformers/embedding.py - LyingAboutTokens2
"""
from manimlib import *


def break_into_words(phrase_mob):
    """Break a Text mobject into individual word submobjects."""
    import re
    phrase = phrase_mob.get_string()
    offsets = [m.start() for m in re.finditer(" ", phrase)]
    return break_into_pieces(phrase_mob, [0, *offsets])


def break_into_pieces(phrase_mob, offsets):
    """Break a Text mobject at specified character offsets."""
    phrase = phrase_mob.get_string()
    lhs = offsets
    rhs = [*offsets[1:], len(phrase)]
    result = []
    for lh, rh in zip(lhs, rhs):
        substr = phrase[lh:rh]
        start = phrase_mob.substr_to_path_count(phrase[:lh])
        end = start + phrase_mob.substr_to_path_count(substr)
        result.append(phrase_mob[start:end])
    return VGroup(*result)


def random_bright_color(hue_range=(0.5, 0.6)):
    """Generate a random bright color within a hue range."""
    import random
    hue = random.uniform(*hue_range)
    return Color(hsl=(hue, 0.8, 0.6))


def get_piece_rectangles(
    phrase_pieces,
    h_buff=0.05,
    v_buff=0.1,
    fill_opacity=0.15,
    fill_color=None,
    stroke_width=1,
    stroke_color=None,
    hue_range=(0.5, 0.6),
    leading_spaces=False,
):
    """Create colored rectangles around text pieces."""
    rects = VGroup()
    height = phrase_pieces.get_height() + 2 * v_buff
    last_right_x = phrase_pieces.get_x(LEFT)
    for piece in phrase_pieces:
        left_x = last_right_x if leading_spaces else piece.get_x(LEFT)
        right_x = piece.get_x(RIGHT)
        fill = random_bright_color(hue_range) if fill_color is None else fill_color
        stroke = fill if stroke_color is None else stroke_color
        rect = Rectangle(
            width=right_x - left_x + 2 * h_buff,
            height=height,
            fill_color=fill,
            fill_opacity=fill_opacity,
            stroke_color=stroke,
            stroke_width=stroke_width
        )
        if leading_spaces:
            rect.set_x(left_x, LEFT)
        else:
            rect.move_to(piece)
        rect.set_y(0)
        rects.add(rect)
        last_right_x = right_x

    rects.match_y(phrase_pieces)
    return rects


class TokenizationDemo(InteractiveScene):
    """
    Demonstrates how text is broken into tokens/words with visual highlighting.
    """

    def construct(self):
        # Title
        title = Text("Tokenization", font_size=72)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Show a phrase being tokenized
        phrase = Text("The goal of our model is to predict the next word")
        phrase.set_width(FRAME_WIDTH - 2)
        phrase.next_to(title, DOWN, buff=1.0)

        self.play(Write(phrase, run_time=2))
        self.wait()

        # Break into words
        words = break_into_words(phrase)
        rects = get_piece_rectangles(words, hue_range=(0.5, 0.6))

        # Animate rectangles appearing
        self.add(rects, phrase)
        self.play(
            LaggedStartMap(FadeIn, rects, lag_ratio=0.1),
            LaggedStart(*(
                word.animate.set_color(rect.get_color())
                for word, rect in zip(words, rects)
            ), lag_ratio=0.1)
        )
        self.wait()

        # Highlight last word as prediction target
        last_rect = rects[-1]
        q_marks = Text("???", font_size=48)
        q_marks.next_to(last_rect, DOWN)

        self.play(
            last_rect.animate.set_color(YELLOW),
            FadeIn(q_marks)
        )
        self.wait()

        # Show arrow from context to prediction
        context_rect = Rectangle()
        context_rect.replace(rects[:-1], stretch=True)
        context_rect.set_stroke(WHITE, 2)

        arrow = Arrow(context_rect.get_top(), last_rect.get_top(), path_arc=-90 * DEGREES)
        arrow.scale(0.6, about_edge=DR)

        self.play(
            FadeIn(context_rect),
            GrowArrow(arrow),
        )
        self.wait()

        # Transition to showing embedding concept
        self.play(
            FadeOut(title),
            FadeOut(context_rect),
            FadeOut(arrow),
            FadeOut(q_marks),
        )

        # Show words becoming vectors
        word_labels = VGroup(*(
            Text(word.get_string().strip(), font_size=36)
            for word in words[:-1]
        ))

        # Create simple vector representations
        vectors = VGroup(*(
            VGroup(
                Tex("["),
                VGroup(*(
                    DecimalNumber(np.random.uniform(-1, 1), num_decimal_places=2)
                    for _ in range(4)
                )).arrange(DOWN, buff=0.1),
                Tex("]"),
            ).arrange(RIGHT, buff=0.05)
            for _ in words[:-1]
        ))
        for vector in vectors:
            vector.scale(0.6)

        # Arrange word-vector pairs
        pairs = VGroup()
        for word, vec, rect in zip(word_labels, vectors, rects[:-1]):
            vec.get_brackets = lambda v=vec: VGroup(v[0], v[-1])
            vec.get_brackets().match_color(rect.get_color())
            pair = VGroup(word, vec)
            pair.arrange(DOWN, buff=0.5)
            pairs.add(pair)

        pairs.arrange(RIGHT, buff=0.8)
        pairs.set_width(FRAME_WIDTH - 1)
        pairs.center()

        # Animate transformation
        self.play(
            LaggedStart(*(
                AnimationGroup(
                    ReplacementTransform(VGroup(rect, word), label),
                    FadeIn(vec, shift=DOWN),
                )
                for word, rect, label, vec in zip(words[:-1], rects[:-1], word_labels, vectors)
            ), lag_ratio=0.1),
            FadeOut(rects[-1]),
            FadeOut(words[-1]),
            run_time=3
        )
        self.wait()

        # Add title for embedding
        embed_title = Text("Word Embeddings", font_size=60)
        embed_title.to_edge(UP)
        self.play(Write(embed_title))
        self.wait(2)
