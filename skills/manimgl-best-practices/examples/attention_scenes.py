"""
Attention Mechanism Scenes - ManimGL Examples

A collection of scenes from 3Blue1Brown's Attention video,
adapted to be self-contained without external image dependencies.

Run with: manimgl attention_scenes.py <SceneName> -w -l

Available scenes:
- ShowMasking
- ScalingAPattern
- LowRankTransformation
- ThinkAboutOverallMap
- CrossAttention
- TwoHarrysExample
- QueryMap
- MultiHeadedAttention
"""
from manimlib import *
import numpy as np
import re
import itertools as it
import random
import warnings


# ============================================================
# Helper Functions
# ============================================================

def softmax(logits, temperature=1.0):
    """Compute softmax of logits array."""
    logits = np.array(logits)
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')
        logits = logits - np.max(logits)
        exps = np.exp(np.divide(logits, temperature, where=temperature != 0))

    if np.isinf(exps).any() or np.isnan(exps).any() or temperature == 0:
        result = np.zeros_like(logits)
        result[np.argmax(logits)] = 1
        return result
    return exps / np.sum(exps)


def value_to_color(
    value,
    low_positive_color=BLUE_E,
    high_positive_color=BLUE_B,
    low_negative_color=RED_E,
    high_negative_color=RED_B,
    min_value=0.0,
    max_value=10.0
):
    """Map a value to a color using interpolation."""
    alpha = clip(float(inverse_interpolate(min_value, max_value, abs(value))), 0, 1)
    if value >= 0:
        colors = (low_positive_color, high_positive_color)
    else:
        colors = (low_negative_color, high_negative_color)
    return interpolate_color_by_hsl(*colors, alpha)


def break_into_pieces(phrase_mob, offsets):
    """Break a Text mobject into pieces at given character offsets."""
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


def break_into_words(phrase_mob):
    """Break a Text mobject into individual words."""
    offsets = [m.start() for m in re.finditer(" ", phrase_mob.get_string())]
    return break_into_pieces(phrase_mob, [0, *offsets])


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
    """Create colored rectangles behind phrase pieces."""
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


class WeightMatrix(DecimalMatrix):
    """A matrix display for neural network weights."""
    def __init__(
        self,
        values=None,
        shape=(6, 8),
        value_range=(-9.9, 9.9),
        ellipses_row=-2,
        ellipses_col=-2,
        num_decimal_places=1,
        bracket_h_buff=0.1,
        decimal_config=dict(include_sign=True),
        low_positive_color=BLUE_E,
        high_positive_color=BLUE_B,
        low_negative_color=RED_E,
        high_negative_color=RED_B,
    ):
        if values is not None:
            shape = values.shape
        self.shape = shape
        self.value_range = value_range
        self.low_positive_color = low_positive_color
        self.high_positive_color = high_positive_color
        self.low_negative_color = low_negative_color
        self.high_negative_color = high_negative_color
        self.ellipses_row = ellipses_row
        self.ellipses_col = ellipses_col

        if values is None:
            values = np.random.uniform(*self.value_range, size=shape)

        super().__init__(
            values,
            num_decimal_places=num_decimal_places,
            bracket_h_buff=bracket_h_buff,
            decimal_config=decimal_config,
            ellipses_row=ellipses_row,
            ellipses_col=ellipses_col,
        )
        self.set_entry_colors()

    def set_entry_colors(self):
        for entry in self.get_entries():
            if isinstance(entry, DecimalNumber):
                entry.set_color(value_to_color(
                    entry.get_value(),
                    self.low_positive_color,
                    self.high_positive_color,
                    self.low_negative_color,
                    self.high_negative_color,
                    min_value=0.0,
                    max_value=self.value_range[1],
                ))
        return self


class NumericEmbedding(DecimalMatrix):
    """A vector display for embeddings."""
    def __init__(
        self,
        values=None,
        length=8,
        value_range=(-9.9, 9.9),
        num_decimal_places=1,
        bracket_h_buff=0.1,
        decimal_config=dict(include_sign=True),
        ellipses_row=-2,
    ):
        if values is None:
            values = np.random.uniform(*value_range, (length, 1))
        super().__init__(
            values,
            num_decimal_places=num_decimal_places,
            bracket_h_buff=bracket_h_buff,
            decimal_config=decimal_config,
            ellipses_row=ellipses_row,
        )


class ContextAnimation(LaggedStart):
    """Animation showing context flowing between tokens."""
    def __init__(
        self,
        target,
        sources,
        direction=UP,
        hue_range=(0.1, 0.3),
        time_width=2,
        min_stroke_width=0,
        max_stroke_width=5,
        lag_ratio=None,
        strengths=None,
        run_time=3,
        fix_in_frame=False,
        path_arc=PI / 2,
        **kwargs,
    ):
        arcs = VGroup()
        if strengths is None:
            strengths = np.random.random(len(sources))**2
        for source, strength in zip(sources, strengths):
            sign = direction[1] * (-1)**int(source.get_x() < target.get_x())
            arcs.add(Line(
                source.get_edge_center(direction),
                target.get_edge_center(direction),
                path_arc=sign * path_arc,
                stroke_color=random_bright_color(hue_range=hue_range),
                stroke_width=interpolate(
                    min_stroke_width,
                    max_stroke_width,
                    strength,
                )
            ))
        if fix_in_frame:
            arcs.fix_in_frame()
        arcs.shuffle()
        lag_ratio = 0.5 / len(arcs) if lag_ratio is None else lag_ratio

        super().__init__(
            *(
                VShowPassingFlash(arc, time_width=time_width)
                for arc in arcs
            ),
            lag_ratio=lag_ratio,
            run_time=run_time,
            **kwargs,
        )


class RandomizeMatrixEntries(Animation):
    """Animation that randomizes matrix entries."""
    def __init__(self, matrix, **kwargs):
        self.matrix = matrix
        super().__init__(matrix, **kwargs)

    def interpolate_mobject(self, alpha):
        if random.random() < 0.1:
            for entry in self.matrix.get_entries():
                if isinstance(entry, DecimalNumber):
                    new_val = random.uniform(-9.9, 9.9)
                    entry.set_value(new_val)


# ============================================================
# Scene Definitions
# ============================================================

class ShowMasking(Scene):
    """Demonstrates causal masking in attention."""
    def construct(self):
        # Set up two patterns
        shape = (6, 6)
        left_grid = Square().get_grid(*shape, buff=0)
        left_grid.set_shape(5.5, 5)
        left_grid.to_edge(LEFT)
        left_grid.set_y(-0.5)
        left_grid.set_stroke(GREY_B, 1)

        right_grid = left_grid.copy()
        right_grid.to_edge(RIGHT)

        grids = VGroup(left_grid, right_grid)
        arrow = Arrow(left_grid, right_grid)
        sm_label = Text("softmax")
        sm_label.next_to(arrow, UP)

        titles = VGroup(
            Text("Unnormalized\nAttention Pattern"),
            Text("Normalized\nAttention Pattern"),
        )
        for title, grid in zip(titles, grids):
            title.next_to(grid, UP, buff=MED_LARGE_BUFF)

        values_array = np.random.normal(0, 2, shape)
        font_size = 30
        raw_values = VGroup(
            DecimalNumber(
                value,
                include_sign=True,
                font_size=font_size,
            ).move_to(square)
            for square, value in zip(left_grid, values_array.flatten())
        )

        self.add(left_grid)
        self.add(right_grid)
        self.add(titles)
        self.add(arrow)
        self.add(sm_label)
        self.add(raw_values)

        # Highlight lower lefts (masking)
        changers = VGroup()
        for n, dec in enumerate(raw_values):
            i = n // shape[1]
            j = n % shape[1]
            if i > j:
                changers.add(dec)
                neg_inf = Tex(R"-\infty", font_size=36)
                neg_inf.move_to(dec)
                neg_inf.set_fill(RED, border_width=1.5)
                dec.target = neg_inf
                values_array[i, j] = -np.inf
        rects = VGroup(map(SurroundingRectangle, changers))
        rects.set_stroke(RED, 3)

        self.play(LaggedStartMap(ShowCreation, rects))
        self.play(
            LaggedStartMap(FadeOut, rects),
            LaggedStartMap(MoveToTarget, changers)
        )
        self.wait()

        # Normalized values
        normalized_array = np.array([
            softmax(col)
            for col in values_array.T
        ]).T
        normalized_values = VGroup(
            DecimalNumber(value, font_size=font_size).move_to(square)
            for square, value in zip(right_grid, normalized_array.flatten())
        )
        for n, value in enumerate(normalized_values):
            value.set_fill(opacity=interpolate(0.5, 1, rush_from(value.get_value())))
            if (n // shape[1]) > (n % shape[1]):
                value.set_fill(RED, 0.75)

        self.play(
            LaggedStart(
                (FadeTransform(v1.copy(), v2)
                for v1, v2 in zip(raw_values, normalized_values)),
                lag_ratio=0.05,
                group_type=Group
            )
        )
        self.wait()


class ScalingAPattern(Scene):
    """Shows a large attention pattern scaling up."""
    def construct(self):
        # Position grid
        N = 50
        grid = Square(side_length=1.0).get_grid(N, N, buff=0)
        grid.set_stroke(GREY_A, 1)
        grid.stretch(0.89, 0)
        grid.stretch(0.70, 1)
        grid.move_to(5.0 * LEFT + 2.5 * UP, UL)
        self.add(grid)

        # Dots representing attention weights
        values = np.random.normal(0, 1, (N, N))
        dots = VGroup()
        for n, row in enumerate(values):
            row[:n] = -np.inf
        for k, col in enumerate(values.T):
            for n, value in enumerate(softmax(col)):
                dot = Dot(radius=0.3 * value**0.75)
                dot.move_to(grid[n * N + k])
                dots.add(dot)
        dots.set_fill(GREY_C, 1)
        self.add(dots)

        # Add Q and K symbols
        q_template = Tex(R"\vec{\textbf{Q}}_0").set_color(YELLOW)
        k_template = Tex(R"\vec{\textbf{K}}_0").set_color(TEAL)
        for template in [q_template, k_template]:
            template.scale(0.75)
            template.substr = template.make_number_changeable("0")

        qs = VGroup()
        ks = VGroup()
        for n, square in enumerate(grid[:N], start=1):
            q_template.substr.set_value(n)
            q_template.next_to(square, UP, buff=SMALL_BUFF)
            qs.add(q_template.copy())
        for k, square in enumerate(grid[::N], start=1):
            k_template.substr.set_value(k)
            k_template.next_to(square, LEFT, buff=2 * SMALL_BUFF)
            ks.add(k_template.copy())
        self.add(qs, ks)

        # Slowly zoom out
        self.play(
            self.frame.animate.reorient(0, 0, 0, (14.72, -14.71, 0.0), 38.06),
            grid.animate.set_stroke(width=1, opacity=0.25),
            dots.animate.set_fill(GREY_B, 1).set_stroke(GREY_B, 1),
            run_time=20,
        )
        self.wait()


class LowRankTransformation(Scene):
    """Visualizes low-rank transformation in attention."""
    def construct(self):
        frame = self.frame
        frame.set_field_of_view(10 * DEGREES)

        all_axes = VGroup(
            self.get_3d_axes(),
            self.get_2d_axes(),
            self.get_3d_axes(),
        )
        all_axes.arrange(RIGHT, buff=2.0)
        all_axes.set_width(FRAME_WIDTH - 2)
        all_axes.move_to(0.5 * DOWN)
        dim_labels = VGroup(
            Text("12,288 dims"),
            Text("128 dims"),
            Text("12,288 dims"),
        )
        dim_labels.scale(0.75)
        dim_labels.set_fill(GREY_A)
        for label, axes in zip(dim_labels, all_axes):
            label.next_to(axes, UP, buff=MED_LARGE_BUFF)

        map_arrows = Tex(R"\rightarrow", font_size=96).replicate(2)
        map_arrows.set_color(YELLOW)
        for arrow, vect in zip(map_arrows, [LEFT, RIGHT]):
            arrow.next_to(all_axes[1], vect, buff=0.5)

        axes_group = VGroup(all_axes, dim_labels)
        self.add(axes_group)
        self.add(map_arrows)

        # Add vectors
        all_coords = [
            (4, 2, 1),
            (2, 3),
            (-3, 3, -2),
        ]
        colors = [BLUE, RED_B, RED_C]
        vects = VGroup(
            Arrow(axes.get_origin(), axes.c2p(*coords), buff=0, stroke_color=color)
            for axes, coords, color in zip(all_axes, all_coords, colors)
        )

        self.add(vects[0])
        for v1, v2 in zip(vects, vects[1:]):
            self.play(TransformFromCopy(v1, v2))

        for axes, vect in zip(all_axes, vects):
            axes.add(vect)
        for axes in all_axes[0::2]:
            axes.add_updater(lambda m, dt: m.rotate(2 * dt * DEGREES, axis=m.y_axis.get_vector()))
        self.wait(3)

        # Add title
        big_rect = SurroundingRectangle(axes_group, buff=0.5)
        big_rect.round_corners(radius=0.5)
        big_rect.set_stroke(RED_B, 2)
        title = Text("Low-rank transformation", font_size=72)
        title.next_to(big_rect, UP, buff=MED_LARGE_BUFF)

        self.play(
            ShowCreation(big_rect),
            FadeIn(title, shift=0.25 * UP)
        )
        self.wait(5)

    def get_3d_axes(self, height=3):
        result = ThreeDAxes((-4, 4), (-4, 4), (-4, 4))
        result.set_height(height)
        result.rotate(20 * DEGREES, DOWN)
        result.rotate(5 * DEGREES, RIGHT)
        return result

    def get_2d_axes(self, height=2):
        plane = NumberPlane(
            (-4, 4), (-4, 4),
            faded_line_ratio=0,
            background_line_style=dict(
                stroke_color=GREY_B,
                stroke_width=1,
                stroke_opacity=0.5
            )
        )
        plane.set_height(height)
        return plane


class ThinkAboutOverallMap(Scene):
    """Simple scene showing a reminder about overall maps."""
    def construct(self):
        rect = Rectangle(6.5, 2.75)
        rect.round_corners(radius=0.5)
        rect.set_stroke(RED_B, 2)
        label = Text("Think about the\noverall map")
        label.next_to(rect, UP, aligned_edge=LEFT)
        label.shift(0.5 * RIGHT)
        self.play(
            ShowCreation(rect),
            FadeIn(label, UP),
        )
        self.wait()


class CrossAttention(Scene):
    """Shows cross-attention between two languages."""
    def construct(self):
        # Show both language phrases
        en_tokens = self.get_words("I do not want to pet it")
        fr_tokens = self.get_words("Je ne veux pas le caresser", hue_range=(0.2, 0.3))
        phrases = VGroup(en_tokens, fr_tokens)
        phrases.arrange(DOWN, buff=2.0)
        self.play(LaggedStartMap(FadeIn, en_tokens, scale=2, lag_ratio=0.25))
        self.wait()
        self.play(LaggedStartMap(FadeIn, fr_tokens, scale=2, lag_ratio=0.25))
        self.wait()

        # Create attention pattern
        unnormalized_pattern = [
            [3, 0, 0, 0, 0, 0],
            [0, 1, 1.3, 1, 0, 0],
            [0, 3, 0, 3, 0, 0],
            [0, 0, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 3],
            [0, 0, 0, 0, 0, 3],
            [0, 0, 0, 0, 3, 0],
        ]
        attention_pattern = np.array([
            softmax(col) for col in unnormalized_pattern
        ]).T

        # Show connections
        lines = VGroup()
        for n, row in enumerate(attention_pattern.T):
            for k, value in enumerate(row):
                line = Line(en_tokens[n].get_bottom(), fr_tokens[k].get_top(), buff=0)
                line.set_stroke(
                    color=[
                        en_tokens[n][0].get_color(),
                        fr_tokens[k][0].get_color(),
                    ],
                    width=3,
                    opacity=value,
                )
                lines.add(line)

        self.play(ShowCreation(lines, lag_ratio=0.01, run_time=2))
        self.wait(2)
        self.play(FadeOut(lines))

        # Create grid
        grid = Square().get_grid(len(fr_tokens), len(en_tokens), buff=0)
        grid.stretch(1.2, 0)
        grid.set_stroke(GREY_B, 1)
        grid.set_height(5.0)
        grid.to_edge(DOWN, buff=SMALL_BUFF)
        grid.set_x(1)

        # Create qk symbols
        q_sym_generator = self.get_symbol_generator(R"\vec{\textbf{Q}}_0", color=YELLOW)
        k_sym_generator = self.get_symbol_generator(R"\vec{\textbf{K}}_0", color=TEAL)
        e_sym_generator = self.get_symbol_generator(R"\vec{\textbf{E}}_0", color=GREY_B)
        f_sym_generator = self.get_symbol_generator(R"\vec{\textbf{F}}_0", color=BLUE)

        q_syms = VGroup(q_sym_generator(n + 1) for n in range(len(en_tokens)))
        k_syms = VGroup(k_sym_generator(n + 1) for n in range(len(fr_tokens)))
        e_syms = VGroup(e_sym_generator(n + 1) for n in range(len(en_tokens)))
        f_syms = VGroup(f_sym_generator(n + 1) for n in range(len(fr_tokens)))
        VGroup(q_syms, k_syms, e_syms, f_syms).scale(0.65)

        for q_sym, e_sym, square in zip(q_syms, e_syms, grid):
            q_sym.next_to(square, UP, SMALL_BUFF)
            e_sym.next_to(q_sym, UP, buff=0.65)

        for k_sym, f_sym, square in zip(k_syms, f_syms, grid[::len(en_tokens)]):
            k_sym.next_to(square, LEFT, SMALL_BUFF)
            f_sym.next_to(k_sym, LEFT, buff=0.75)

        q_arrows = VGroup(Arrow(*pair, buff=0.1) for pair in zip(e_syms, q_syms))
        k_arrows = VGroup(Arrow(*pair, buff=0.1) for pair in zip(f_syms, k_syms))
        e_arrows = VGroup(Vector(0.4 * DOWN).next_to(e_sym, UP, SMALL_BUFF) for e_sym in e_syms)
        f_arrows = VGroup(Vector(0.5 * RIGHT).next_to(f_sym, LEFT, SMALL_BUFF) for f_sym in f_syms)
        arrows = VGroup(q_arrows, k_arrows, e_arrows, f_arrows)
        arrows.set_color(GREY_B)

        wq_syms = VGroup(
            Tex("W_Q", font_size=20, fill_color=YELLOW).next_to(arrow, RIGHT, buff=0.1)
            for arrow in q_arrows
        )
        wk_syms = VGroup(
            Tex("W_K", font_size=20, fill_color=TEAL).next_to(arrow, UP, buff=0.1)
            for arrow in k_arrows
        )

        # Move tokens into place
        en_tokens.target = en_tokens.generate_target()
        fr_tokens.target = fr_tokens.generate_target()
        for token, arrow in zip(en_tokens.target, e_arrows):
            token.next_to(arrow, UP, SMALL_BUFF)
        for token, arrow in zip(fr_tokens.target, f_arrows):
            token.next_to(arrow, LEFT, SMALL_BUFF)
        self.play(
            MoveToTarget(en_tokens),
            MoveToTarget(fr_tokens),
        )
        self.play(
            LaggedStartMap(GrowArrow, e_arrows),
            LaggedStartMap(GrowArrow, f_arrows),
            LaggedStartMap(FadeIn, e_syms, shift=0.25 * DOWN),
            LaggedStartMap(FadeIn, f_syms, shift=0.25 * RIGHT),
            lag_ratio=0.25,
            run_time=1.5,
        )
        self.play(
            LaggedStartMap(GrowArrow, q_arrows),
            LaggedStartMap(GrowArrow, k_arrows),
            LaggedStartMap(FadeIn, wq_syms, shift=0.25 * DOWN),
            LaggedStartMap(FadeIn, wk_syms, shift=0.25 * RIGHT),
            LaggedStartMap(FadeIn, q_syms, shift=0.5 * DOWN),
            LaggedStartMap(FadeIn, k_syms, shift=0.5 * RIGHT),
            lag_ratio=0.25,
            run_time=1.5,
        )
        self.play(FadeIn(grid, lag_ratio=1e-2), run_time=2)
        self.wait()

        # Show dot products
        dot_prods = VGroup()
        for q_sym in q_syms:
            for k_sym in k_syms:
                dot = Tex(".")
                dot.match_x(q_sym)
                dot.match_y(k_sym)
                dot_prod = VGroup(q_sym.copy(), dot, k_sym.copy())
                dot_prod.target = dot_prod.generate_target()
                dot_prod.target.arrange(RIGHT, buff=SMALL_BUFF)
                dot_prod.target.scale(0.7)
                dot_prod.target.move_to(dot)
                dot.set_opacity(0)
                dot_prods.add(dot_prod)

        self.play(
            LaggedStartMap(MoveToTarget, dot_prods, lag_ratio=0.01),
            run_time=3
        )
        self.wait()

        # Show dots
        dots = VGroup()
        for square, value in zip(grid, attention_pattern.flatten()):
            dot = Dot(radius=value * 0.4)
            dot.set_fill(GREY_B, 1)
            dot.move_to(square)
            dots.add(dot)

        self.play(
            LaggedStartMap(GrowFromCenter, dots, lag_ratio=1e-2),
            dot_prods.animate.set_fill(opacity=0.2).set_anim_args(lag_ratio=1e-3),
            run_time=4
        )
        self.wait()

    def get_words(self, text, hue_range=(0.5, 0.6)):
        sent = Text(text)
        tokens = break_into_words(sent)
        rects = get_piece_rectangles(tokens, hue_range=hue_range)
        return VGroup(VGroup(*pair) for pair in zip(rects, tokens))

    def get_symbol_generator(self, raw_tex, subsrc="0", color=WHITE):
        template = Tex(raw_tex)
        template.set_color(color)
        subscr = template.make_number_changeable(subsrc)

        def get_sym(number):
            subscr.set_value(number)
            return template.copy()

        return get_sym


class TwoHarrysExample(Scene):
    """Shows how context disambiguates 'Harry'."""
    def construct(self):
        s1, s2 = sentences = VGroup(
            break_into_words(Text("... " + " ... ".join(words)))
            for words in [
                ("wizard", "Hogwarts", "Hermione", "Harry"),
                ("Queen", "Sussex", "William", "Harry"),
            ]
        )
        sentences.arrange(DOWN, buff=2.0, aligned_edge=RIGHT)
        sentences.to_edge(LEFT)

        def context_anim(group):
            self.play(
                ContextAnimation(
                    group[-1],
                    VGroup(*it.chain(*group[1:-1:2])),
                    direction=DOWN,
                    path_arc=PI / 4,
                    run_time=5,
                    lag_ratio=0.025,
                )
            )

        self.add(s1)
        context_anim(s1)
        self.wait()
        self.play(FadeTransformPieces(s1.copy(), s2))
        context_anim(s2)


class QueryMap(Scene):
    """Shows how embedding space maps to query/key space."""
    map_tex = "W_Q"
    map_color = YELLOW
    src_name = "Creature"
    pos_word = "position 4"
    trg_name = "Any adjectives\nbefore position 4?"
    in_vect_color = BLUE_B
    in_vect_coords = (3, 2, -2)
    out_vect_coords = (-2, -1)

    def construct(self):
        # Setup 3d axes
        axes_3d = ThreeDAxes((-4, 4), (-3, 3), (-4, 4))
        xz_plane = NumberPlane(
            (-4, 4), (-4, 4),
            background_line_style=dict(
                stroke_color=GREY,
                stroke_width=1,
            ),
            faded_line_ratio=0
        )
        xz_plane.rotate(90 * DEGREES, RIGHT)
        xz_plane.move_to(axes_3d)
        xz_plane.axes.set_opacity(0)
        axes_3d.add(xz_plane)
        axes_3d.set_height(2.0)

        self.set_floor_plane("xz")
        frame = self.frame
        frame.set_field_of_view(30 * DEGREES)
        frame.reorient(-32, 0, 0, (2.13, 1.11, 0.27), 4.50)
        frame.add_ambient_rotation(1 * DEGREES)

        self.add(axes_3d)

        # Set up target plane
        plane = NumberPlane(
            (-3, 3), (-3, 3),
            faded_line_ratio=1,
            background_line_style=dict(
                stroke_color=BLUE,
                stroke_width=1,
                stroke_opacity=0.75
            ),
            faded_line_style=dict(
                stroke_color=BLUE,
                stroke_width=1,
                stroke_opacity=0.25,
            )
        )
        plane.set_height(3.5)
        plane.to_corner(DR)

        arrow = Tex(R"\longrightarrow")
        arrow.set_width(2)
        arrow.stretch(0.75, 1)
        arrow.next_to(plane, LEFT, buff=1.0)
        arrow.set_color(self.map_color)

        map_name = Tex(self.map_tex, font_size=72)
        map_name.set_color(self.map_color)
        map_name.next_to(arrow.get_left(), UR, SMALL_BUFF).shift(0.25 * RIGHT)

        for mob in [plane, arrow, map_name]:
            mob.fix_in_frame()

        self.add(plane)
        self.add(arrow)
        self.add(map_name)

        # Add titles
        titles = VGroup(
            Text("Embedding space"),
            Text("Query/Key space"),
        )
        subtitles = VGroup(
            Text("12,288-dimensional"),
            Text("128-dimensional"),
        )
        subtitles.scale(0.75)
        subtitles.set_fill(GREY_B)
        x_values = [-frame.get_x() * FRAME_HEIGHT / frame.get_height(), plane.get_x()]
        for title, subtitle, x_value in zip(titles, subtitles, x_values):
            subtitle.next_to(title, DOWN, SMALL_BUFF)
            title.add(subtitle)
            title.next_to(plane, UP, MED_LARGE_BUFF)
            title.set_x(x_value)
            title.fix_in_frame()

        self.add(titles)

        # Show vector transformation
        in_vect = Arrow(axes_3d.get_origin(), axes_3d.c2p(*self.in_vect_coords), buff=0)
        in_vect.set_stroke(self.in_vect_color)
        in_vect_label = TexText("``" + self.src_name + "''", font_size=24)
        pos_label = Text(self.pos_word, font_size=16)
        pos_label.next_to(in_vect_label, DOWN, SMALL_BUFF)
        pos_label.set_opacity(0.75)
        in_vect_label.add(pos_label)
        in_vect_label.set_color(self.in_vect_color)
        in_vect_label.next_to(in_vect.get_end(), UP, SMALL_BUFF)

        out_vect = Arrow(plane.get_origin(), plane.c2p(*self.out_vect_coords), buff=0)
        out_vect.set_stroke(self.map_color)
        out_vect_label = Text(self.trg_name, font_size=30)
        out_vect_label.next_to(out_vect.get_end(), DOWN, buff=0.2)
        out_vect_label.set_backstroke(BLACK, 5)
        VGroup(out_vect, out_vect_label).fix_in_frame()

        self.play(
            GrowArrow(in_vect),
            FadeInFromPoint(in_vect_label, axes_3d.get_origin()),
        )
        self.wait(2)
        self.play(
            TransformFromCopy(in_vect, out_vect),
            FadeTransform(in_vect_label.copy(), out_vect_label),
            run_time=2,
        )
        self.wait(10)
        self.play(FadeOut(out_vect_label))
        self.wait(3)


class MultiHeadedAttention(Scene):
    """Demonstrates multi-headed attention with procedural patterns."""
    def construct(self):
        # Mention head
        background_rect = FullScreenRectangle()
        single_title = Text("Single head of attention")
        multiple_title = Text("Multi-headed attention")
        titles = VGroup(single_title, multiple_title)
        for title in titles:
            title.scale(1.25)
            title.to_edge(UP)

        # Create attention pattern instead of loading image
        screen_rect = ScreenRectangle(height=6)
        screen_rect.set_fill(BLACK, 1)
        screen_rect.set_stroke(WHITE, 3)
        screen_rect.next_to(titles, DOWN, buff=0.5)

        head = single_title["head"][0]

        self.add(background_rect)
        self.add(single_title)
        self.add(screen_rect)
        self.wait()
        self.play(
            FlashAround(head, run_time=2),
            head.animate.set_color(YELLOW),
        )
        self.wait()

        # Change title
        kw = dict(path_arc=45 * DEGREES)
        self.play(
            FadeTransform(single_title["Single"], multiple_title["Multi-"], **kw),
            FadeTransform(single_title["head"], multiple_title["head"], **kw),
            FadeIn(multiple_title["ed"], 0.25 * RIGHT),
            FadeTransform(single_title["attention"], multiple_title["attention"], **kw),
            FadeOut(single_title["of"])
        )
        self.add(multiple_title)

        # Set up procedural attention pattern heads
        n_heads = 15
        heads = Group()
        for n in range(n_heads):
            # Create procedural attention pattern
            pattern_grid = self.create_attention_pattern(seed=n * 7)
            pattern_grid.set_opacity(1)
            pattern_grid.shift(0.01 * OUT)
            rect = SurroundingRectangle(pattern_grid, buff=0)
            rect.set_fill(BLACK, 0.75)
            rect.set_stroke(WHITE, 1, 1)
            heads.add(Group(rect, pattern_grid))

        # Show many parallel layers
        self.set_floor_plane("xz")
        frame = self.frame
        multiple_title.fix_in_frame()
        background_rect.fix_in_frame()

        heads.set_height(4)
        heads.arrange(OUT, buff=1.0)
        heads.move_to(DOWN)

        pre_head = self.create_attention_pattern(seed=0)
        pre_head.replace(screen_rect)
        pre_head_rect = SurroundingRectangle(pre_head, buff=0)
        pre_head_rect.set_fill(BLACK, 0.75)
        pre_head_rect.set_stroke(WHITE, 1, 1)
        pre_head = Group(pre_head_rect, pre_head)

        self.add(pre_head)
        self.wait()
        self.play(
            frame.animate.reorient(41, -12, 0, (-1.0, -1.42, 1.09), 12.90).set_anim_args(run_time=2),
            background_rect.animate.set_fill(opacity=0.75),
            FadeTransform(pre_head, heads[-1], time_span=(1, 2)),
        )
        self.play(
            frame.animate.reorient(48, -11, 0, (-1.0, -1.42, 1.09), 12.90),
            LaggedStart(
                (FadeTransform(heads[-1].copy(), image)
                for image in heads),
                lag_ratio=0.1,
                group_type=Group,
            ),
            run_time=4,
        )
        self.add(heads)
        self.wait()

        # Show matrices
        colors = [YELLOW, TEAL, RED, PINK]
        texs = ["W_Q", "W_K", R"\downarrow W_V", R"\uparrow W_V"]
        n_shown = 9
        wq_syms, wk_syms, wv_down_syms, wv_up_syms = sym_groups = VGroup(
            VGroup(
                Tex(tex + f"^{{({n})}}", font_size=36).next_to(image, UP, MED_SMALL_BUFF)
                for n, image in enumerate(heads[:-n_shown - 1:-1], start=1)
            ).set_color(color).set_backstroke(BLACK, 5)
            for tex, color in zip(texs, colors)
        )
        for group in wv_down_syms, wv_up_syms:
            for sym in group:
                sym[0].next_to(sym[1], LEFT, buff=0.025)
        dots = Tex(R"\dots", font_size=90)
        dots.rotate(PI / 2, UP)
        sym_rot_angle = 70 * DEGREES
        for syms in sym_groups:
            syms.align_to(heads, LEFT)
            for sym in syms:
                sym.rotate(sym_rot_angle, UP)
            dots.next_to(syms, IN, buff=0.5)
            dots.match_style(syms[0])
            syms.add(dots.copy())

        up_shift = 0.75 * UP
        self.play(
            LaggedStartMap(FadeIn, wq_syms, shift=0.2 * UP, lag_ratio=0.25),
            frame.animate.reorient(59, -7, 0, (-1.62, 0.25, 1.29), 14.18),
            run_time=2,
        )
        for n in range(1, len(sym_groups)):
            self.play(
                LaggedStartMap(FadeIn, sym_groups[n], shift=0.2 * UP, lag_ratio=0.1),
                sym_groups[:n].animate.shift(up_shift),
                run_time=1,
            )
        self.wait()

        # Count up 96 heads
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
        self.wait(2)

    def create_attention_pattern(self, n_rows=8, seed=0):
        """Create a procedural attention pattern grid."""
        np.random.seed(seed)

        grid = Square().get_grid(n_rows, 1, buff=0).get_grid(1, n_rows, buff=0)
        grid.set_stroke(WHITE, 1, 0.5)
        grid.set_height(3.0)

        pattern = np.random.normal(0, 1, (n_rows, n_rows))
        for n in range(len(pattern[0])):
            pattern[:, n][n + 1:] = -np.inf
            pattern[:, n] = softmax(pattern[:, n])
        pattern = pattern.T

        dots = VGroup()
        for col, values in zip(grid, pattern):
            for square, value in zip(col, values):
                if value < 1e-3:
                    continue
                dot = Dot(radius=0.4 * square.get_height() * value)
                dot.move_to(square)
                dots.add(dot)
        dots.set_fill(GREY_B, 1)
        grid.add(dots)

        return grid
