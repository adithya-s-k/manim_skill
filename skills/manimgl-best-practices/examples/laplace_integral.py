"""
Laplace Transform Integration Visualization

Demonstrates the integral of e^{-st} as area under the curve,
showing how squishing by 1/s preserves the area relationship.

Run: manimgl laplace_integral.py LaplaceIntegral -w
Preview: manimgl laplace_integral.py LaplaceIntegral -p

Source: Adapted from 3b1b's Laplace transform video (2025)
"""
from manimlib import *


class LaplaceIntegral(InteractiveScene):
    """
    Visualize the integral ∫₀^∞ e^{-st} dt = 1/s

    Key techniques:
    - get_area_under_graph for shaded regions
    - ValueTracker for parameter animation
    - Dynamic function binding
    - make_number_changeable for live updates
    """

    def construct(self):
        # Set up axes
        max_x = 15
        unit_size = 4
        axes = Axes(
            x_range=(0, max_x, 0.25),
            y_range=(0, 1, 0.25),
            unit_size=unit_size
        )
        axes.to_edge(DL, buff=1.0)
        axes.add_coordinate_labels(num_decimal_places=2, font_size=20)

        # Parameter s
        s_tracker = ValueTracker(1)
        get_s = s_tracker.get_value

        # The exponential function
        def exp_func(t):
            return np.exp(-get_s() * t)

        # Dynamic graph
        graph = axes.get_graph(np.exp)
        graph.set_stroke(BLUE, 3)
        axes.bind_graph_to_func(graph, exp_func)

        # Label
        t2c = {"s": YELLOW}
        graph_label = Tex(R"e^{-st}", t2c=t2c, font_size=72)
        graph_label.next_to(axes.y_axis.get_top(), UR).shift(0.5 * RIGHT)

        # Integral expression
        integral = Tex(R"\int^\infty_0 e^{-st} dt", t2c=t2c)
        integral.set_x(1)
        integral.to_edge(UP)

        self.add(axes, graph, graph_label, integral)

        # Add a slider for s
        s_slider = self.create_slider(s_tracker)
        s_slider.to_edge(UP, buff=MED_LARGE_BUFF)
        s_slider.align_to(axes.c2p(0, 0), LEFT)

        self.add(s_slider)

        # Vary s to show different decay rates
        for value in [5, 0.25, 1]:
            self.play(s_tracker.animate.set_value(value), run_time=4)
            self.wait()

        # Show integral as area
        equals = Tex(R"=", font_size=72).rotate(90 * DEG)
        equals.next_to(integral, DOWN)
        area_word = Text("Area", font_size=60)
        area_word.next_to(equals, DOWN)

        area = axes.get_area_under_graph(graph)

        def update_area(area):
            area.become(axes.get_area_under_graph(graph))

        arrow = Arrow(area_word.get_corner(DL), axes.c2p(0.75, 0.5), thickness=4)

        self.play(
            LaggedStart(
                Animation(graph.copy(), remover=True),
                Write(equals),
                FadeIn(area_word, DOWN),
                GrowArrow(arrow),
                UpdateFromFunc(area, update_area),
                lag_ratio=0.25
            ),
            ShowCreation(graph, suspend_mobject_updating=True, run_time=3),
        )
        self.wait()

        # Show that area = 1 when s = 1
        simple_integral = Tex(R"\int^\infty_0 e^{-t} dt")
        simple_integral.move_to(integral)

        equals_one = Tex(R"= 1", font_size=60)
        equals_one.next_to(area_word)

        area_one_label = Tex(R"1", font_size=60)
        area_one_label.move_to(axes.c2p(0.35, 0.35))
        area_one_label.set_z_index(1)

        self.play(
            TransformMatchingTex(integral, simple_integral),
            FadeOut(graph_label),
        )
        self.wait()

        self.play(Write(equals_one))
        self.play(TransformFromCopy(equals_one["1"], area_one_label))
        self.wait()

        # Show area squishing with s
        area.clear_updaters()
        area.add_updater(update_area)

        rhs = Tex(R"= \frac{1}{s}", t2c=t2c, font_size=60)
        rhs.next_to(area_word, RIGHT)

        self.play(LaggedStart(
            FadeOut(equals_one),
            FadeOut(area_one_label),
            FadeOut(simple_integral),
            FadeIn(integral),
            FadeIn(graph_label),
            FadeOut(arrow),
            lag_ratio=0.1
        ))

        self.play(
            s_tracker.animate.set_value(5).set_anim_args(run_time=8),
        )

        area_word.save_state()
        self.play(
            area_word.animate.move_to(axes.c2p(0.6, 0.33)),
            Write(rhs),
            FadeOut(equals),
        )
        self.wait()

        # Show decimal approximation
        dec_rhs = Tex(R"= 1.00", font_size=60)
        dec_rhs.make_number_changeable("1.00").add_updater(lambda m: m.set_value(1 / get_s()))
        dec_rhs.always.next_to(rhs, RIGHT)

        self.play(
            VFadeIn(dec_rhs),
            s_tracker.animate.set_value(0.5).set_anim_args(run_time=8),
        )
        self.wait()

        self.play(
            s_tracker.animate.set_value(2),
            run_time=4,
        )
        self.wait(2)

    def create_slider(self, tracker, x_range=(0, 5), height=1.5, font_size=36):
        """Create a visual slider for the s parameter."""
        number_line = NumberLine(x_range, width=height, tick_size=0.05)
        number_line.rotate(90 * DEG)

        indicator = ArrowTip(width=0.1, length=0.2)
        indicator.rotate(PI)
        indicator.add_updater(lambda m: m.move_to(number_line.n2p(tracker.get_value()), LEFT))
        indicator.set_color(YELLOW)

        label = Tex(R"s = 0.00", font_size=font_size)
        label["s"].set_color(YELLOW)
        label.rhs = label.make_number_changeable("0.00")
        label.always.next_to(indicator, RIGHT, SMALL_BUFF)
        label.rhs.f_always.set_value(tracker.get_value)

        slider = VGroup(number_line, indicator, label)
        return slider


class AverageValueInterpretation(InteractiveScene):
    """
    Show that unit integrals equal the average value over that interval.
    Helps build intuition for the Laplace transform.
    """

    def construct(self):
        # Set up axes
        axes = Axes(
            x_range=(0, 6),
            y_range=(0, 1.2),
            width=10,
            height=4
        )
        axes.to_edge(DOWN, buff=1)

        # Fixed s value
        s = 0.5

        def exp_func(t):
            return np.exp(-s * t)

        # Graph
        graph = axes.get_graph(exp_func)
        graph.set_stroke(BLUE, 3)

        self.add(axes, graph)

        # Unit interval [0, 1]
        v_lines = VGroup(
            DashedLine(axes.c2p(0, 0), axes.c2p(0, 1.2)),
            DashedLine(axes.c2p(1, 0), axes.c2p(1, 1.2)),
        )
        v_lines.set_stroke(WHITE, 1)

        # Area under [0, 1]
        area = axes.get_area_under_graph(graph, x_range=(0, 1))

        # Integral label
        int_tex = Tex(R"\int^1_0 e^{-st} dt", t2c={"s": YELLOW}, font_size=48)
        int_tex.move_to(v_lines, UP).shift(0.5 * UP)

        self.play(
            ShowCreation(v_lines),
            FadeIn(area),
            Write(int_tex),
        )
        self.wait()

        # Show average value interpretation
        avg_value = np.mean([exp_func(t) for t in np.linspace(0, 1, 1000)])

        avg_rect = Rectangle(
            width=axes.x_axis.get_unit_size(),
            height=avg_value * axes.y_axis.get_unit_size()
        )
        avg_rect.set_fill(GREEN, 0.5)
        avg_rect.set_stroke(GREEN, 2)
        avg_rect.move_to(axes.c2p(0.5, avg_value/2))

        avg_label = Text("Average height", font_size=24)
        avg_label.next_to(avg_rect, RIGHT)

        self.play(
            area.animate.set_fill(opacity=0.3),
            FadeIn(avg_rect),
            Write(avg_label),
        )
        self.wait()

        # Explanation
        explanation = Tex(
            R"\text{Area} = \text{Width} \times \text{Height}_{avg}",
            font_size=36
        )
        explanation.to_edge(UP)

        self.play(Write(explanation))
        self.wait(2)


class IntegralAsSum(InteractiveScene):
    """
    Show the full integral as a sum of unit interval averages.
    """

    def construct(self):
        # Axes
        axes = Axes(
            x_range=(0, 8),
            y_range=(0, 1.2),
            width=12,
            height=4
        )
        axes.to_edge(DOWN, buff=1)

        s = 0.75

        def exp_func(t):
            return np.exp(-s * t)

        graph = axes.get_graph(exp_func)
        graph.set_stroke(BLUE, 3)

        self.add(axes, graph)

        # Create stacked areas for each unit interval
        areas = VGroup()
        colors = color_gradient([BLUE_E, TEAL_E], 6)

        for n, color in enumerate(colors):
            area = axes.get_area_under_graph(graph, x_range=(n, n+1))
            area.set_fill(color, 0.7)
            areas.add(area)

        # Labels for each interval
        labels = VGroup()
        for n in range(6):
            label = Tex(f"[{n}, {n+1}]", font_size=24)
            label.move_to(areas[n])
            labels.add(label)

        # Animate adding areas
        self.play(LaggedStartMap(FadeIn, areas, lag_ratio=0.3))
        self.play(LaggedStartMap(FadeIn, labels, lag_ratio=0.2))
        self.wait()

        # Show total integral
        total = Tex(
            R"\int^\infty_0 e^{-st} dt = \sum_{n=0}^{\infty} \int_n^{n+1} e^{-st} dt",
            t2c={"s": YELLOW},
            font_size=36
        )
        total.to_edge(UP)

        self.play(Write(total))
        self.wait()

        # Highlight that it converges
        result = Tex(R"= \frac{1}{s}", t2c={"s": YELLOW}, font_size=48)
        result.next_to(total, DOWN)

        self.play(Write(result))
        self.wait(2)
