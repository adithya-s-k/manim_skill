"""
Equation Transforms and Mathematical Derivations

Shows step-by-step equation manipulation with highlighting,
the hallmark of 3b1b's mathematical explanations.

Run: manimgl equation_transforms.py QuadraticFormula -w
Preview: manimgl equation_transforms.py QuadraticFormula -p

Source: Inspired by 3b1b's equation transformation style
"""
from manimlib import *


class QuadraticFormula(InteractiveScene):
    """
    Derives the quadratic formula step by step with
    color-coded terms and smooth transformations.
    """

    def construct(self):
        # Color scheme for terms
        colors = {
            "a": RED,
            "b": GREEN,
            "c": BLUE,
            "x": YELLOW,
        }

        # Step 1: Start with general quadratic
        eq1 = Tex(
            r"ax^2 + bx + c = 0",
            t2c={"a": RED, "b": GREEN, "c": BLUE, "x": YELLOW}
        )
        eq1.to_edge(UP, buff=1)

        self.play(Write(eq1))
        self.wait()

        # Step 2: Divide by a
        eq2 = Tex(
            r"x^2 + \frac{b}{a}x + \frac{c}{a} = 0",
            t2c={"a": RED, "b": GREEN, "c": BLUE, "x": YELLOW}
        )
        eq2.next_to(eq1, DOWN, buff=0.8)

        step1_label = Text("Divide by a", font_size=24, color=GREY)
        step1_label.next_to(eq2, LEFT, buff=0.5)

        self.play(
            TransformMatchingTex(eq1.copy(), eq2),
            FadeIn(step1_label, LEFT),
        )
        self.wait()

        # Step 3: Complete the square
        eq3 = Tex(
            r"\left(x + \frac{b}{2a}\right)^2 - \frac{b^2}{4a^2} + \frac{c}{a} = 0",
            t2c={"a": RED, "b": GREEN, "c": BLUE, "x": YELLOW}
        )
        eq3.next_to(eq2, DOWN, buff=0.8)

        step2_label = Text("Complete the square", font_size=24, color=GREY)
        step2_label.next_to(eq3, LEFT, buff=0.5)

        self.play(
            TransformMatchingTex(eq2.copy(), eq3),
            FadeIn(step2_label, LEFT),
        )
        self.wait()

        # Step 4: Isolate the squared term
        eq4 = Tex(
            r"\left(x + \frac{b}{2a}\right)^2 = \frac{b^2 - 4ac}{4a^2}",
            t2c={"a": RED, "b": GREEN, "c": BLUE, "x": YELLOW}
        )
        eq4.next_to(eq3, DOWN, buff=0.8)

        step3_label = Text("Rearrange", font_size=24, color=GREY)
        step3_label.next_to(eq4, LEFT, buff=0.5)

        self.play(
            TransformMatchingTex(eq3.copy(), eq4),
            FadeIn(step3_label, LEFT),
        )
        self.wait()

        # Step 5: Take square root
        eq5 = Tex(
            r"x + \frac{b}{2a} = \pm\frac{\sqrt{b^2 - 4ac}}{2a}",
            t2c={"a": RED, "b": GREEN, "c": BLUE, "x": YELLOW}
        )
        eq5.next_to(eq4, DOWN, buff=0.8)

        step4_label = Text("Square root", font_size=24, color=GREY)
        step4_label.next_to(eq5, LEFT, buff=0.5)

        self.play(
            TransformMatchingTex(eq4.copy(), eq5),
            FadeIn(step4_label, LEFT),
        )
        self.wait()

        # Final formula with box
        final = Tex(
            r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
            t2c={"a": RED, "b": GREEN, "c": BLUE, "x": YELLOW},
            font_size=60
        )
        final.next_to(eq5, DOWN, buff=1)

        box = SurroundingRectangle(final, color=GOLD, buff=0.2)

        self.play(
            TransformMatchingTex(eq5.copy(), final),
        )
        self.play(ShowCreation(box))
        self.wait(2)


class HighlightAndTransform(InteractiveScene):
    """
    Demonstrates the technique of highlighting parts of equations
    before transforming them. A core 3b1b pattern.
    """

    def construct(self):
        # Start with an equation
        eq = Tex(r"(a + b)^2 = a^2 + 2ab + b^2", font_size=48)
        eq.center()

        self.play(Write(eq))
        self.wait()

        # Highlight LHS
        lhs = eq[r"(a + b)^2"]
        lhs_rect = SurroundingRectangle(lhs, color=YELLOW, buff=0.1)

        self.play(ShowCreation(lhs_rect))
        self.wait()

        # Highlight RHS parts one by one
        parts = [
            (r"a^2", RED),
            (r"2ab", GREEN),
            (r"b^2", BLUE),
        ]

        rects = []
        for tex, color in parts:
            part = eq[tex]
            rect = SurroundingRectangle(part, color=color, buff=0.05)
            self.play(ShowCreation(rect))
            rects.append(rect)
            self.wait(0.5)

        # Fade out rectangles
        self.play(
            FadeOut(lhs_rect),
            *[FadeOut(r) for r in rects]
        )

        # Show visual proof
        self.play(eq.animate.to_edge(UP))

        # Create squares
        side = 2
        a_frac = 0.6
        a_side = side * a_frac
        b_side = side * (1 - a_frac)

        # The big square (a+b)^2
        big_square = Square(side)
        big_square.set_stroke(WHITE, 2)
        big_square.center()

        # Subdivisions
        a_sq = Square(a_side)
        a_sq.set_fill(RED, 0.5)
        a_sq.set_stroke(WHITE, 1)
        a_sq.align_to(big_square, UL)

        b_sq = Square(b_side)
        b_sq.set_fill(BLUE, 0.5)
        b_sq.set_stroke(WHITE, 1)
        b_sq.align_to(big_square, DR)

        ab_rect1 = Rectangle(width=a_side, height=b_side)
        ab_rect1.set_fill(GREEN, 0.5)
        ab_rect1.set_stroke(WHITE, 1)
        ab_rect1.next_to(a_sq, RIGHT, buff=0)

        ab_rect2 = Rectangle(width=b_side, height=a_side)
        ab_rect2.set_fill(GREEN, 0.5)
        ab_rect2.set_stroke(WHITE, 1)
        ab_rect2.next_to(a_sq, DOWN, buff=0)

        squares = VGroup(a_sq, b_sq, ab_rect1, ab_rect2)

        # Labels
        a_label = Tex("a^2", color=RED, font_size=24)
        a_label.move_to(a_sq)

        b_label = Tex("b^2", color=BLUE, font_size=24)
        b_label.move_to(b_sq)

        ab_label1 = Tex("ab", color=GREEN, font_size=20)
        ab_label1.move_to(ab_rect1)

        ab_label2 = Tex("ab", color=GREEN, font_size=20)
        ab_label2.move_to(ab_rect2)

        self.play(ShowCreation(big_square))
        self.play(
            FadeIn(a_sq), Write(a_label),
            FadeIn(ab_rect1), Write(ab_label1),
            FadeIn(ab_rect2), Write(ab_label2),
            FadeIn(b_sq), Write(b_label),
            run_time=2
        )
        self.wait(2)


class BraceAnnotations(InteractiveScene):
    """
    Uses braces to annotate and explain equation parts.
    Another signature 3b1b technique.
    """

    def construct(self):
        # Main equation
        eq = Tex(
            r"F = ma",
            font_size=96
        )
        eq.center()

        self.play(Write(eq))
        self.wait()

        # Add braces with labels
        F_brace = Brace(eq["F"], UP, color=BLUE)
        F_label = F_brace.get_text("Force", font_size=30)
        F_label.set_color(BLUE)

        m_brace = Brace(eq["m"], DOWN, color=RED)
        m_label = m_brace.get_text("Mass", font_size=30)
        m_label.set_color(RED)

        a_brace = Brace(eq["a"], DOWN, color=GREEN)
        a_label = a_brace.get_text("Acceleration", font_size=30)
        a_label.set_color(GREEN)

        self.play(
            GrowFromCenter(F_brace),
            FadeIn(F_label, UP),
        )
        self.wait()

        self.play(
            GrowFromCenter(m_brace),
            FadeIn(m_label, DOWN),
        )
        self.wait()

        self.play(
            GrowFromCenter(a_brace),
            FadeIn(a_label, DOWN),
        )
        self.wait()

        # Fade all and show rearrangement
        all_braces = VGroup(F_brace, F_label, m_brace, m_label, a_brace, a_label)

        eq2 = Tex(r"a = \frac{F}{m}", font_size=96)
        eq2.center()

        self.play(FadeOut(all_braces))
        self.play(TransformMatchingTex(eq, eq2))
        self.wait()

        # New annotation
        new_brace = Brace(eq2[r"\frac{F}{m}"], DOWN, color=YELLOW)
        new_label = new_brace.get_text("Force per unit mass", font_size=24)
        new_label.set_color(YELLOW)

        self.play(
            GrowFromCenter(new_brace),
            FadeIn(new_label, DOWN),
        )
        self.wait(2)


class ColorCodedSubstitution(InteractiveScene):
    """
    Shows variable substitution with color tracking.
    Makes complex substitutions easy to follow.
    """

    def construct(self):
        # Define substitution
        sub_def = Tex(
            r"u = x^2 + 1",
            t2c={"u": RED, "x": BLUE}
        )
        sub_def.to_edge(UP)

        self.play(Write(sub_def))
        self.wait()

        # Original integral
        integral1 = Tex(
            r"\int 2x(x^2 + 1)^3 \, dx",
            t2c={"x": BLUE},
            font_size=48
        )
        integral1.center()

        self.play(Write(integral1))
        self.wait()

        # Highlight the u part
        u_part = integral1[r"(x^2 + 1)"]
        u_rect = SurroundingRectangle(u_part, color=RED, buff=0.05)

        self.play(ShowCreation(u_rect))
        self.wait()

        # Show du
        du_def = Tex(
            r"du = 2x \, dx",
            t2c={"u": RED, "x": BLUE}
        )
        du_def.next_to(sub_def, DOWN)

        # Highlight the 2x dx part
        dx_part = integral1[r"2x"]
        dx_rect = SurroundingRectangle(dx_part, color=GREEN, buff=0.05)

        self.play(
            Write(du_def),
            ShowCreation(dx_rect),
        )
        self.wait()

        # Transform to u integral
        integral2 = Tex(
            r"\int u^3 \, du",
            t2c={"u": RED},
            font_size=48
        )
        integral2.center()

        self.play(
            FadeOut(u_rect),
            FadeOut(dx_rect),
            TransformMatchingTex(integral1, integral2),
        )
        self.wait()

        # Solve
        solution = Tex(
            r"= \frac{u^4}{4} + C",
            t2c={"u": RED},
            font_size=48
        )
        solution.next_to(integral2, DOWN, buff=0.5)

        self.play(Write(solution))
        self.wait()

        # Substitute back
        final = Tex(
            r"= \frac{(x^2+1)^4}{4} + C",
            t2c={"x": BLUE},
            font_size=48
        )
        final.next_to(solution, DOWN, buff=0.5)

        self.play(
            TransformMatchingTex(solution.copy(), final),
        )
        self.wait(2)
