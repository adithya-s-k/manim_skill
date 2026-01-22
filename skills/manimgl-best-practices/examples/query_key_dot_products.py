"""
Query-Key Dot Products Grid Visualization
Shows how queries and keys produce a grid of dot products that form the attention pattern.
"""

from manimlib import *
import numpy as np


class QueryKeyDotProducts(InteractiveScene):
    def construct(self):
        # Create query and key symbols
        n_tokens = 5

        # Query template
        q_template = Tex(R"\vec{\textbf{Q}}_0")
        q_template[0].scale(1.5, about_edge=DOWN)
        q_template.set_color(YELLOW)
        q_subscript = q_template.make_number_changeable("0")

        # Key template
        k_template = Tex(R"\vec{\textbf{K}}_0")
        k_template[0].scale(1.5, about_edge=DOWN)
        k_template.set_color(TEAL)
        k_subscript = k_template.make_number_changeable("0")

        # Create query symbols along top
        q_syms = VGroup()
        for n in range(1, n_tokens + 1):
            q_subscript.set_value(n)
            q_syms.add(q_template.copy())
        q_syms.arrange(RIGHT, buff=0.8)
        q_syms.move_to(2 * UP)

        # Create key symbols along left
        k_syms = VGroup()
        for n in range(1, n_tokens + 1):
            k_subscript.set_value(n)
            k_syms.add(k_template.copy())
        k_syms.arrange(DOWN, buff=0.6)
        k_syms.next_to(q_syms, DL, buff=0.8)
        k_syms.shift(0.5 * LEFT)

        self.play(
            LaggedStartMap(FadeIn, q_syms, shift=0.5 * DOWN, lag_ratio=0.1),
            LaggedStartMap(FadeIn, k_syms, shift=0.5 * RIGHT, lag_ratio=0.1),
        )
        self.wait()

        # Draw grid lines
        h_lines = VGroup()
        for k in k_syms:
            h_line = Line(LEFT, RIGHT).set_width(6)
            h_line.next_to(k, DOWN, buff=0.3)
            h_line.align_to(k_syms, LEFT)
            h_lines.add(h_line)

        v_lines = VGroup()
        for q in q_syms:
            v_line = Line(UP, DOWN).set_height(5)
            v_line.next_to(q, DOWN, buff=0.3)
            v_lines.add(v_line)
        v_lines.add(v_lines[-1].copy().next_to(q_syms, RIGHT, buff=0.5))

        grid_lines = VGroup(*h_lines, *v_lines)
        grid_lines.set_stroke(GREY_A, 1)

        self.play(
            ShowCreation(h_lines, lag_ratio=0.2),
            ShowCreation(v_lines, lag_ratio=0.2),
        )

        # Create dot products in each cell
        dot_prods = VGroup()
        for k_sym in k_syms:
            for q_sym in q_syms:
                square_center = np.array([q_sym.get_x(), k_sym.get_y(), 0])
                dot = Tex(R"\cdot", font_size=48)
                dot.move_to(square_center)
                dot.set_fill(opacity=0)

                dot_prod = VGroup(k_sym.copy(), dot, q_sym.copy())
                dot_prod.target = dot_prod.generate_target()
                dot_prod.target.arrange(RIGHT, buff=0.1)
                dot_prod.target.scale(0.5)
                dot_prod.target.move_to(square_center)
                dot_prod.target.set_fill(opacity=1)
                dot_prods.add(dot_prod)

        self.play(
            LaggedStartMap(MoveToTarget, dot_prods, lag_ratio=0.02, run_time=3)
        )
        self.wait()

        # Show numerical values (random attention scores)
        np.random.seed(42)
        dots = VGroup(
            VGroup(Dot().match_x(q_sym).match_y(k_sym) for q_sym in q_syms)
            for k_sym in k_syms
        )

        # Set sizes based on "attention" - diagonal and some off-diagonal get bigger
        for n, row in enumerate(dots):
            for k, dot in enumerate(row):
                base_size = 0.1 + 0.15 * np.random.random()
                dot.set_width(base_size)
                dot.set_fill(GREY_C, 0.8)
                # Make diagonal stronger (self-attention)
                if n == k:
                    dot.set_width(0.5 + 0.2 * np.random.random())
                    dot.set_fill(WHITE, 1)

        flat_dots = VGroup(*it.chain(*dots))

        self.play(
            dot_prods.animate.set_fill(opacity=0.3),
            LaggedStartMap(GrowFromCenter, flat_dots, lag_ratio=0.02)
        )
        self.wait()

        # Label as attention pattern
        pattern_label = Text("Attention Pattern", font_size=60)
        pattern_label.to_edge(DOWN)
        pattern_label.set_color(YELLOW)

        self.play(Write(pattern_label))
        self.wait(2)
