"""
Solving Damped Harmonic Oscillator ODE

Demonstrates animated equation solving for the damped spring-mass system.
Shows hypothesis substitution, algebraic manipulation, and quadratic formula.

Run: manimgl solve_damped_ode.py SolveDampedODE -w
Preview: manimgl solve_damped_ode.py SolveDampedODE -p

Source: Adapted from 3b1b's Laplace transform video (2025)
"""
from manimlib import *


def get_coef_colors(n_coefs=3):
    """Generate gradient colors for position, velocity, acceleration."""
    return [
        interpolate_color_by_hsl(TEAL, RED, a)
        for a in np.linspace(0, 1, n_coefs)
    ]


class SolveDampedODE(InteractiveScene):
    """
    Animated walkthrough of solving x'' + μx' + kx = 0
    using the exponential hypothesis x(t) = e^{st}.

    Key techniques demonstrated:
    - TransformMatchingTex for equation transformations
    - Animated arrows between derivatives
    - SurroundingRectangle for highlighting
    - Brace annotations
    """

    def construct(self):
        # Color scheme for derivatives
        colors = get_coef_colors()

        # Show x, x', x'' with labels
        self.show_derivative_relationship(colors)

        # Show F = ma equation
        self.show_force_equation(colors)

        # Hypothesis: x = e^{st}
        self.show_exponential_hypothesis(colors)

        # Solve for s
        self.solve_for_s()

    def show_derivative_relationship(self, colors):
        """Show position, velocity, acceleration and their relationships."""
        pos, vel, acc = funcs = VGroup(
            Tex(R"x(t)"),
            Tex(R"x'(t)"),
            Tex(R"x''(t)"),
        )
        funcs.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)

        labels = VGroup(
            Text("Position").set_color(colors[0]),
            Text("Velocity").set_color(colors[1]),
            Text("Acceleration").set_color(colors[2]),
        )
        for line, label in zip(funcs, labels):
            label.next_to(line, RIGHT, MED_LARGE_BUFF)
            label.align_to(labels[0], LEFT)

        VGroup(funcs, labels).to_corner(UR)

        # Derivative arrows between terms
        arrows = VGroup()
        for l1, l2 in zip(funcs, funcs[1:]):
            arrow = Line(l1.get_left(), l2.get_left(), path_arc=150 * DEG, buff=0.2)
            arrow.add_tip(width=0.2, length=0.2)
            arrow.set_color(GREY_B)
            ddt = Tex(R"\frac{d}{dt}", font_size=30)
            ddt.set_color(GREY_B)
            ddt.next_to(arrow, LEFT, SMALL_BUFF)
            arrow.add(ddt)
            arrows.add(arrow)

        # Animate
        self.play(Write(funcs[0]), Write(labels[0]))
        self.wait()

        for func1, func2, label1, label2, arrow in zip(funcs, funcs[1:], labels, labels[1:], arrows):
            self.play(LaggedStart(
                GrowFromPoint(arrow, arrow.get_corner(UR), path_arc=30 * DEG),
                TransformFromCopy(func1, func2, path_arc=30 * DEG),
                FadeTransform(label1.copy(), label2),
                lag_ratio=0.1
            ))
            self.wait()

        self.deriv_group = VGroup(funcs, labels, arrows)
        self.funcs = funcs
        self.colors = colors

    def show_force_equation(self, colors):
        """Show F = ma formulation: mx'' = -kx - μx'"""
        t2c = {
            "x(t)": colors[0],
            "x'(t)": colors[1],
            "x''(t)": colors[2],
        }
        equation1 = Tex(R"{m} x''(t) = -k x(t) - \mu x'(t)", t2c=t2c)
        equation1.to_corner(UL)

        ma = equation1["{m} x''(t)"][0]
        kx = equation1["-k x(t)"][0]
        mu_v = equation1[R"- \mu x'(t)"][0]

        # Braces for each term
        ma_brace = Brace(ma, DOWN, buff=SMALL_BUFF)
        ma_brace.add(ma_brace.get_tex(R"\textbf{F}"))

        kx_brace = Brace(kx, DOWN, buff=SMALL_BUFF)
        kx_brace.add(kx_brace.get_tex(R"\text{Spring force}"))

        mu_v_brace = Brace(mu_v, DOWN, buff=SMALL_BUFF)
        mu_v_brace.add(mu_v_brace.get_tex(R"\text{Damping}"))

        pos, vel, acc = self.funcs

        self.play(TransformFromCopy(acc, ma[1:], path_arc=-45 * DEG))
        self.play(LaggedStart(
            GrowFromCenter(ma_brace),
            Write(ma[0]),
            run_time=1,
            lag_ratio=0.1
        ))
        self.wait()

        self.play(LaggedStart(
            Write(equation1["= -k"][0]),
            FadeTransformPieces(ma_brace, kx_brace),
            TransformFromCopy(pos, equation1["x(t)"][0], path_arc=-45 * DEG),
        ))
        self.wait()

        self.play(LaggedStart(
            FadeTransformPieces(kx_brace, mu_v_brace),
            Write(equation1[R"- \mu"][0]),
            TransformFromCopy(vel, equation1["x'(t)"][0], path_arc=-45 * DEG),
        ))
        self.wait()
        self.play(FadeOut(mu_v_brace))

        # Rearrange to standard form
        equation2 = Tex(R"{m} x''(t) + \mu x'(t) + k x(t) = 0", t2c=t2c)
        equation2.move_to(equation1, UL)

        self.play(TransformMatchingTex(equation1, equation2, path_arc=45 * DEG))
        self.wait()

        self.equation = equation2

    def show_exponential_hypothesis(self, colors):
        """Show guess x(t) = e^{st} and plug it in."""
        t2c = {"s": YELLOW, "x(t)": TEAL}

        hyp_word, hyp_tex = hypothesis = VGroup(
            Text("Hypothesis: "),
            Tex("x(t) = e^{st}", t2c=t2c),
        )
        hypothesis.arrange(RIGHT)
        hypothesis.to_corner(UR)

        sub_hyp = TexText(R"(For some $s$)", t2c={"$s$": YELLOW}, font_size=36, fill_color=GREY_B)
        sub_hyp.next_to(hyp_tex, DOWN)

        pos = self.funcs[0]

        self.play(LaggedStart(
            FadeTransform(pos.copy(), hyp_tex[:4], path_arc=45 * DEG, remover=True),
            FadeOut(self.deriv_group),
            Write(hyp_word, run_time=1),
            Write(hyp_tex[4:], time_span=(0.5, 1.5)),
        ))
        self.add(hypothesis)
        self.wait()
        self.play(FadeIn(sub_hyp, 0.25 * DOWN))
        self.wait()

        self.hypothesis = hypothesis
        self.sub_hyp = sub_hyp

    def solve_for_s(self):
        """Plug in hypothesis and solve the characteristic equation."""
        t2c = {"s": YELLOW}

        # After substitution: m s^2 e^{st} + μ s e^{st} + k e^{st} = 0
        equation3 = Tex(R"{m} s^2 e^{st} + \mu s e^{st} + k e^{st} = 0", t2c=t2c)
        equation3.next_to(self.equation, DOWN, LARGE_BUFF)

        self.play(FadeIn(equation3, 0.5 * DOWN))
        self.wait()

        # Factor out e^{st}
        equation4 = Tex(R"e^{st} \left( ms^2 + \mu s + k \right) = 0", t2c=t2c)
        equation4.next_to(equation3, DOWN, LARGE_BUFF)

        self.play(
            TransformMatchingTex(
                equation3.copy(),
                equation4,
                matched_keys=[R"e^{st}"],
                run_time=1.5,
                path_arc=30 * DEG
            )
        )
        self.wait()

        # Highlight e^{st} ≠ 0
        exp_rect = SurroundingRectangle(equation4[R"e^{st}"])
        exp_rect.set_stroke(YELLOW, 2)
        ne_0 = VGroup(Tex(R"\ne").rotate(90 * DEG), Integer(0))
        ne_0.arrange(DOWN).next_to(exp_rect, DOWN)

        self.play(ShowCreation(exp_rect))
        self.play(Write(ne_0))
        self.wait()

        # Characteristic equation
        equation5 = Tex(R"ms^2 + \mu s + k = 0", t2c=t2c)
        equation5.next_to(equation4, DOWN, LARGE_BUFF)

        self.play(
            FadeOut(ne_0),
            FadeOut(exp_rect),
            Write(equation5),
        )
        self.wait()

        # Quadratic formula result
        equation6 = Tex(R"s = {{-\mu \pm \sqrt{\mu^2 - 4mk}} \over 2m}")
        equation6["s"].set_color(YELLOW)
        equation6.next_to(equation5, DOWN, LARGE_BUFF)

        qf_words = Text("Quadratic Formula", font_size=30, fill_color=GREY_B)
        qf_words.next_to(equation6, RIGHT, MED_LARGE_BUFF)

        self.play(
            FadeIn(equation6, 0.5 * DOWN),
            FadeIn(qf_words),
        )
        self.wait(2)


class SimpleODEDemo(InteractiveScene):
    """
    Simpler version showing just the undamped case: x'' + ωx = 0
    Results in x = e^{±iωt}, demonstrating complex exponentials.
    """

    def construct(self):
        # Undamped equation
        equation = Tex(R"x''(t) + \omega^2 x(t) = 0", font_size=60)
        equation.to_edge(UP)

        self.add(equation)
        self.wait()

        # Hypothesis
        hypothesis = Tex(R"\text{Try } x(t) = e^{st}", font_size=48)
        hypothesis["s"].set_color(YELLOW)
        hypothesis.next_to(equation, DOWN, LARGE_BUFF)

        self.play(Write(hypothesis))
        self.wait()

        # Result
        result = Tex(R"s^2 + \omega^2 = 0 \implies s = \pm i\omega", font_size=48)
        result["s"].set_color(YELLOW)
        result.next_to(hypothesis, DOWN, LARGE_BUFF)

        self.play(Write(result))
        self.wait()

        # Solutions
        solutions = Tex(
            R"x(t) = c_1 e^{i\omega t} + c_2 e^{-i\omega t}",
            font_size=48
        )
        solutions.next_to(result, DOWN, LARGE_BUFF)

        self.play(Write(solutions))
        self.wait()

        # Box the result
        box = SurroundingRectangle(solutions, buff=0.2)
        box.set_stroke(TEAL, 3)

        self.play(ShowCreation(box))
        self.wait(2)
