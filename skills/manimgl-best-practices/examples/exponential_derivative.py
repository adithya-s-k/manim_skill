"""
Exponential Function and Its Derivative

Demonstrates the fundamental property that d/dt e^t = e^t
with tangent line visualization and moving point.

Run: manimgl exponential_derivative.py ExpDerivative -w
Preview: manimgl exponential_derivative.py ExpDerivative -p

Source: Adapted from 3b1b's Laplace transform video (2025)
"""
from manimlib import *


class ExpDerivative(InteractiveScene):
    """
    Visual demonstration of the exponential function's defining property.

    Key techniques:
    - get_v_line_to_graph for vertical lines
    - get_tangent_line for derivative visualization
    - always updaters for dynamic positioning
    - make_number_changeable for live value displays
    """

    def construct(self):
        # Set up graph
        axes = Axes(
            x_range=(-1, 4),
            y_range=(0, 20),
            width=10,
            height=6
        )
        axes.to_edge(RIGHT)

        # Axis label
        t_label = Tex("t")
        t_label.next_to(axes.x_axis.get_right(), UL, MED_SMALL_BUFF)
        axes.add(t_label)

        # The exponential graph
        graph = axes.get_graph(np.exp)
        graph.set_stroke(BLUE, 3)

        # Title showing the defining property
        title = Tex(
            R"\frac{d}{dt} e^t = e^t",
            t2c={"t": GREY_B},
            font_size=60
        )
        title.to_edge(UP)
        title.match_x(axes.c2p(1.5, 0))

        self.add(axes, graph, title)

        # Tracker for the point on the graph
        t_tracker = ValueTracker(1)
        get_t = t_tracker.get_value

        # Vertical line showing height e^t
        v_line = always_redraw(
            lambda: axes.get_v_line_to_graph(get_t(), graph, line_func=Line)
                       .set_stroke(RED, 3)
        )

        # Height label
        height_label = Tex(R"e^t", font_size=42)
        height_label.always.next_to(v_line, RIGHT, SMALL_BUFF)

        # Constrain label size when line is short
        height_label_height = height_label.get_height()
        height_label.add_updater(lambda m: m.set_height(
            min(height_label_height, 0.7 * v_line.get_height())
        ))

        # Animate the height visualization
        self.play(
            ShowCreation(v_line, suspend_mobject_updating=True),
            FadeIn(height_label, UP, suspend_mobject_updating=True),
        )
        self.wait()

        # Add tangent line showing the derivative
        tangent_line = always_redraw(
            lambda: axes.get_tangent_line(get_t(), graph, length=10)
                       .set_stroke(BLUE_A, 1)
        )

        # Show "1" run on the tangent line
        unit_size = axes.x_axis.get_unit_size()
        unit_line = Line(axes.c2p(0, 0), axes.c2p(1, 0))
        unit_line.add_updater(lambda m: m.move_to(v_line.get_end(), LEFT))
        unit_line.set_stroke(WHITE, 2)

        unit_label = Integer(1, font_size=24)
        unit_label.add_updater(lambda m: m.next_to(unit_line.pfp(0.6), UP, 0.5 * SMALL_BUFF))

        # Vertical rise = slope * 1 = derivative value
        tan_v_line = always_redraw(
            lambda: v_line.copy().shift(v_line.get_vector() + unit_size * RIGHT)
        )

        # Label for the derivative (rise of tangent)
        deriv_label = Tex(R"\frac{d}{dt} e^t = e^t", font_size=42)
        deriv_label[R"\frac{d}{dt}"].scale(0.75, about_edge=RIGHT)
        deriv_label_height = deriv_label.get_height()
        deriv_label.add_updater(lambda m: m.set_height(
            min(deriv_label_height, 0.8 * v_line.get_height())
        ))
        deriv_label.always.next_to(tan_v_line, RIGHT, SMALL_BUFF)

        # Show the tangent line
        self.play(ShowCreation(tangent_line, suspend_mobject_updating=True))

        # Show unit run and derivative rise
        self.play(
            VFadeIn(unit_line),
            VFadeIn(unit_label),
            VFadeIn(tan_v_line, suspend_mobject_updating=True),
            TransformFromCopy(title, deriv_label),
        )

        # Animate the height = derivative correspondence
        self.play(
            ReplacementTransform(
                v_line.copy().clear_updaters(),
                tan_v_line,
                path_arc=45 * DEG
            ),
            FadeTransform(height_label.copy(), deriv_label["e^t"][1], path_arc=45 * DEG, remover=True),
        )
        self.wait()

        # Move the point around to show consistency
        for t in [2.35, 0, 1, 2]:
            self.play(t_tracker.animate.set_value(t), run_time=4)
        self.wait()


class ExpFamilyGraph(InteractiveScene):
    """
    Show family of exponentials e^{st} for different values of s.
    When s > 0: growth, s < 0: decay, s = 0: constant.
    """

    def construct(self):
        # Axes
        axes = Axes(
            x_range=(-1, 8),
            y_range=(-1, 5),
            width=FRAME_WIDTH - 2,
            height=FRAME_HEIGHT - 1.5
        )
        axes.to_edge(DOWN)

        # Parameter tracker
        s_tracker = ValueTracker(0.5)
        get_s = s_tracker.get_value

        # Dynamic graph
        graph = axes.get_graph(lambda t: np.exp(t))
        graph.set_stroke(BLUE, 3)
        axes.bind_graph_to_func(graph, lambda t: np.exp(get_s() * t))

        # Label
        label = Tex(R"e^{st}", font_size=90)
        label.move_to(UP)
        label["s"].set_color(YELLOW)

        # s value display
        s_label = Tex(R"s = 0.50", font_size=48)
        s_label["s"].set_color(YELLOW)
        s_value = s_label.make_number_changeable("0.50")
        s_value.add_updater(lambda m: m.set_value(get_s()))
        s_label.to_corner(UR)

        self.add(axes, label, s_label)

        # Draw initial graph
        self.play(ShowCreation(graph, suspend_mobject_updating=True))
        self.wait()

        # Vary s through different regimes
        self.play(
            s_tracker.animate.set_value(-1),
            graph.animate.set_color(YELLOW),
            run_time=4
        )
        self.wait()

        self.play(s_tracker.animate.set_value(0), run_time=2)
        self.wait()

        self.play(
            s_tracker.animate.set_value(0.3),
            graph.animate.set_color(GREEN),
            run_time=2
        )
        self.wait()

        self.play(s_tracker.animate.set_value(0.5), run_time=2)
        self.wait(2)


class ComplexExpSpiral(InteractiveScene):
    """
    Visualize e^{(a+bi)t} as a spiral in the complex plane.
    Shows how real part controls growth/decay, imaginary controls rotation.
    """

    def construct(self):
        # Complex plane
        plane = ComplexPlane(
            x_range=(-3, 3),
            y_range=(-3, 3),
            background_line_style=dict(stroke_color=BLUE, stroke_width=1),
        )
        plane.set_height(6)
        plane.to_edge(LEFT)
        plane.add_coordinate_labels(font_size=20)

        self.add(plane)

        # s = a + bi tracker
        s_tracker = ComplexValueTracker(-0.1 + 1j)
        get_s = s_tracker.get_value

        # Time tracker
        t_tracker = ValueTracker(0)
        get_t = t_tracker.get_value

        # Moving point
        dot = GlowDot(color=TEAL)
        dot.add_updater(lambda m: m.move_to(plane.n2p(np.exp(get_s() * get_t()))))

        # Traced path
        path = TracedPath(dot.get_center, stroke_color=TEAL, stroke_width=2)

        # Vector from origin
        vector = Vector(fill_color=YELLOW)
        vector.add_updater(lambda m: m.put_start_and_end_on(
            plane.n2p(0),
            plane.n2p(np.exp(get_s() * get_t()))
        ))

        # s value display
        s_label = Tex(R"s = -0.10 + 1.00i", font_size=36)
        s_label.to_corner(UR)

        # Expression
        exp_label = Tex(R"e^{st}", font_size=60)
        exp_label["s"].set_color(YELLOW)
        exp_label.next_to(plane, UP)

        self.add(exp_label, s_label)
        self.add(vector, path, dot)

        # Run the animation
        t_tracker.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(t_tracker)

        self.wait(8)

        # Change s to show different spirals
        t_tracker.clear_updaters()
        path.clear_updaters()
        path = TracedPath(dot.get_center, stroke_color=GREEN, stroke_width=2)
        self.add(path)

        t_tracker.set_value(0)
        s_tracker.set_value(0.1 + 1.5j)
        t_tracker.add_updater(lambda m, dt: m.increment_value(dt))

        self.wait(8)
