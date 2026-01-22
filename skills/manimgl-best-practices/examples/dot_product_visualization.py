"""
Dot Product Visualization
Interactive demonstration of how dot products work with two vectors.

Based on: videos/_2024/transformers/embedding.py - DotProducts
"""
from manimlib import *


class DotProductVisualization(InteractiveScene):
    """
    Shows dot product calculation between two vectors in 2D.
    The result updates dynamically as vectors are rotated.
    """

    def construct(self):
        # Set up coordinate plane
        plane = NumberPlane(
            (-4, 4), (-4, 4),
            background_line_style=dict(
                stroke_width=2,
                stroke_opacity=0.5,
                stroke_color=BLUE,
            ),
            faded_line_ratio=1
        )
        plane.set_height(6)
        plane.to_edge(LEFT, buff=0)

        # Create two vectors
        vects = VGroup(
            Vector(0.5 * RIGHT + 2 * UP).set_stroke(MAROON_B, 6),
            Vector(1.0 * RIGHT + 0.5 * UP).set_stroke(YELLOW, 6),
        )
        vects.shift(plane.get_center())

        def get_dot_product():
            coords = np.array([plane.p2c(v.get_end()) for v in vects])
            return np.dot(coords[0], coords[1])

        self.add(plane)
        self.add(vects)

        # Vector labels
        vect_labels = VGroup(*(
            Tex(Rf"\vec{{\textbf{{ {char} }} }}")
            for char in "vw"
        ))
        for label, vect in zip(vect_labels, vects):
            label.vect = vect
            label.match_color(vect)
            label.add_updater(lambda m: m.move_to(
                m.vect.get_end() + 0.25 * normalize(m.vect.get_vector())
            ))

        self.add(vect_labels)

        # Coordinate expressions
        vect_coords = VGroup(*(
            TexMatrix(
                [
                    [char + f"_{{{str(n)}}}"]
                    for n in [1, 2, 3, 4, "n"]
                ],
                bracket_h_buff=0.1,
                ellipses_row=-2,
            )
            for char in "vw"
        ))
        vect_coords.arrange(RIGHT, buff=0.75)
        vect_coords.next_to(plane, RIGHT, buff=1)
        vect_coords.set_y(1)
        for coords, vect in zip(vect_coords, vects):
            coords.get_entries().match_color(vect)

        dot = Tex(R"\cdot", font_size=72)
        dot.move_to(vect_coords)

        self.add(vect_coords, dot)

        # Result display
        rhs = Tex("= +0.00", font_size=60)
        rhs.next_to(vect_coords, RIGHT)
        result = rhs.make_number_changeable("+0.00", include_sign=True)
        result.add_updater(lambda m: m.set_value(get_dot_product()))

        self.add(rhs)

        # Label
        brace = Brace(vect_coords, DOWN, buff=0.25)
        dp_label = brace.get_text("Dot product", buff=0.25)

        self.add(brace, dp_label)

        # Helper function for dual rotation
        def dual_rotate(angle1, angle2, run_time=2):
            self.play(
                Rotate(vects[0], angle1 * DEGREES, about_point=plane.get_origin()),
                Rotate(vects[1], angle2 * DEGREES, about_point=plane.get_origin()),
                run_time=run_time
            )

        # Demonstrate various configurations
        dual_rotate(-20, 20)
        dual_rotate(50, -60)
        dual_rotate(0, 80)
        dual_rotate(20, -80)

        # Show computation breakdown
        equals = rhs[0].copy()
        entry_pairs = VGroup(*(
            VGroup(*pair)
            for pair in zip(*[vc.get_columns()[0] for vc in vect_coords])
        ))
        prod_terms = entry_pairs.copy()
        for src_pair, trg_pair in zip(entry_pairs, prod_terms):
            trg_pair.arrange(RIGHT, buff=0.1)
            trg_pair.next_to(equals, RIGHT, buff=0.5)
            trg_pair.match_y(src_pair)
        prod_terms[-2].space_out_submobjects(1e-3)
        prod_terms[-2].match_x(prod_terms)
        prod_terms.target = prod_terms.generate_target()
        prod_terms.target.space_out_submobjects(1.5).match_y(vect_coords)
        plusses = VGroup(*(
            Tex("+", font_size=48).move_to(midpoint(m1.get_bottom(), m2.get_top()))
            for m1, m2 in zip(prod_terms.target, prod_terms.target[1:])
        ))

        rhs.target = rhs.generate_target()
        rhs.target[0].rotate(PI / 2)
        rhs.target.arrange(DOWN)
        rhs.target.next_to(prod_terms, DOWN)

        self.add(equals)
        self.play(
            LaggedStart(*(
                TransformFromCopy(m1, m2)
                for m1, m2 in zip(entry_pairs, prod_terms)
            ), lag_ratio=0.1, run_time=2),
            MoveToTarget(rhs)
        )
        self.wait()
        self.play(
            MoveToTarget(prod_terms),
            rhs.animate.next_to(prod_terms.target, DOWN),
            LaggedStartMap(Write, plusses),
        )
        self.wait()

        # Show positive dot product
        dual_rotate(-65, 65)
        self.play(FlashAround(result, time_width=1.5, run_time=3))
        self.wait()

        # Show orthogonal (zero dot product)
        elbow = Elbow(width=0.25, angle=vects[0].get_angle())
        elbow.shift(plane.get_origin())
        zero = DecimalNumber(0)
        zero.replace(result, 1)
        dual_rotate(
            (vects[1].get_angle() + PI / 2 - vects[0].get_angle()) / DEGREES,
            0,
        )
        self.remove(result)
        self.add(zero)
        self.play(ShowCreation(elbow))
        self.wait()
        self.remove(elbow, zero)
        self.add(result)

        # Show negative dot product
        dual_rotate(20, -60)
        self.play(FlashAround(result, time_width=1.5, run_time=3))
        self.wait()

        # Final animation
        dual_rotate(75, -95, run_time=5)
