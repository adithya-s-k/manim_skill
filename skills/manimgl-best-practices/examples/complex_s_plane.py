"""
Complex S-Plane Visualization

Interactive visualization of exponential functions in the complex plane.
Shows how the parameter s affects growth, decay, and oscillation.

Run: manimgl complex_s_plane.py SPlaneVisualization -w
Preview: manimgl complex_s_plane.py SPlaneVisualization -p

Source: Adapted from 3b1b's Laplace transform video (2025)
"""
from manimlib import *


class SPlaneVisualization(InteractiveScene):
    """
    Comprehensive s-plane visualization with:
    - Complex s parameter with dot and label
    - Output e^{st} on complex plane
    - Real part graph over time

    Key techniques:
    - ComplexValueTracker for complex numbers
    - Multiple synchronized planes
    - Dynamic graph updating with bind_graph_to_func
    - GlowDot for emphasis
    """

    def construct(self):
        # Trackers for s and t
        s_tracker = ComplexValueTracker(-1)
        t_tracker = ValueTracker(0)
        get_s = s_tracker.get_value
        get_t = t_tracker.get_value

        # S-plane (input)
        s_plane = self.create_s_plane()
        s_dot, s_label = self.create_s_indicator(s_plane, get_s)

        # Output plane (e^{st})
        exp_plane = self.create_output_plane()
        exp_label = self.create_output_label(exp_plane)
        output_dot, output_label = self.create_output_indicator(exp_plane, get_s, get_t)
        output_path = self.create_output_path(exp_plane, get_t, get_s)

        # Graph of Re[e^{st}]
        axes = self.create_graph_axes()
        graph = self.create_dynamic_graph(axes, get_s)
        v_line = self.create_graph_indicator(axes, get_t, get_s)

        # Add everything
        self.add(s_plane, s_dot, s_label)
        self.add(exp_plane, exp_label, output_path, output_dot, output_label)
        self.add(axes, graph, v_line)

        # Store for later use
        self.s_tracker = s_tracker
        self.t_tracker = t_tracker
        self.s_plane = s_plane

        # Animate s exploration
        self.explore_s_values()

    def create_s_plane(self):
        """Create the s-plane (input plane)."""
        plane = ComplexPlane((-2, 2), (-2, 2))
        plane.set_width(7)
        plane.to_edge(LEFT, buff=SMALL_BUFF)
        plane.add_coordinate_labels(font_size=16)
        return plane

    def create_s_indicator(self, s_plane, get_s):
        """Create dot and label tracking s value."""
        s_dot = Group(
            Dot(radius=0.05, fill_color=YELLOW),
            GlowDot(color=YELLOW),
        )
        s_dot.add_updater(lambda m: m.move_to(s_plane.n2p(get_s())))

        s_label = Tex(R"s = +0.5", font_size=36)
        s_rhs = s_label.make_number_changeable("+0.5")
        s_rhs.f_always.set_value(get_s)
        s_label.set_color(YELLOW)
        s_label.set_backstroke(BLACK, 5)
        s_label.always.next_to(s_dot[0], UR, SMALL_BUFF)

        return Group(s_dot, s_label)

    def create_output_plane(self):
        """Create the output plane showing e^{st}."""
        plane = ComplexPlane((-2, 2), (-2, 2))
        plane.background_lines.set_stroke(width=1)
        plane.faded_lines.set_stroke(opacity=0.25)
        plane.set_width(4)
        plane.to_corner(DR).shift(0.5 * LEFT)
        return plane

    def create_output_label(self, exp_plane, font_size=60):
        """Label for output plane."""
        label = Tex(R"e^{st}", font_size=font_size, t2c={"s": YELLOW, "t": BLUE})
        label.set_backstroke(BLACK, 5)
        label.next_to(exp_plane.get_corner(UL), DL, 0.2)
        return label

    def create_output_indicator(self, exp_plane, get_s, get_t):
        """Moving dot showing e^{st} value."""
        output_dot = Group(
            TrueDot(color=GREEN),
            GlowDot(color=GREEN)
        )
        output_dot.add_updater(lambda m: m.move_to(
            exp_plane.n2p(np.exp(get_s() * get_t()))
        ))

        output_label = Tex(R"e^{s \cdot 0.00}", font_size=36, t2c={"s": YELLOW})
        t_label = output_label.make_number_changeable("0.00")
        t_label.set_color(BLUE)
        t_label.f_always.set_value(get_t)
        output_label.always.next_to(output_dot, UR, buff=SMALL_BUFF, aligned_edge=LEFT, index_of_submobject_to_align=0)
        output_label.set_backstroke(BLACK, 3)

        return Group(output_dot, output_label)

    def create_output_path(self, exp_plane, get_t, get_s, delta_t=1/30, color=TEAL, stroke_width=2):
        """Traced path of e^{st} as t increases."""
        path = VMobject()
        path.set_points([ORIGIN])
        path.set_stroke(color, stroke_width)

        def get_path_points():
            t_range = np.arange(0, get_t(), delta_t)
            if len(t_range) == 0:
                t_range = np.array([0])
            values = np.exp(t_range * get_s())
            return np.array([exp_plane.n2p(z) for z in values])

        path.f_always.set_points_smoothly(get_path_points)
        return path

    def create_graph_axes(self):
        """Axes for plotting Re[e^{st}] over time."""
        axes = Axes(
            x_range=(0, 24),
            y_range=(-2, 2),
            width=15,
            height=2
        )
        t_label = Tex(R"t", font_size=36, t2c={"t": BLUE})
        y_label = Tex(R"\text{Re}\left[e^{st}\right]", font_size=36, t2c={"s": YELLOW, "t": BLUE})
        t_label.next_to(axes.x_axis.get_right(), UP, buff=0.15)
        y_label.next_to(axes.y_axis.get_top(), UP, SMALL_BUFF)
        axes.add(t_label, y_label)
        axes.next_to(ORIGIN, RIGHT, MED_LARGE_BUFF)
        axes.to_edge(UP, buff=0.5)
        return axes

    def create_dynamic_graph(self, axes, get_s, stroke_color=TEAL, stroke_width=3):
        """Graph that updates based on current s value."""
        graph = Line().set_stroke(stroke_color, stroke_width)
        t_samples = np.arange(*axes.x_range[:2], 0.1)

        def update_graph(graph):
            s = get_s()
            values = np.exp(s * t_samples)
            xs = values.astype(np.complex128).real
            graph.set_points_smoothly(axes.c2p(t_samples, xs))

        graph.add_updater(update_graph)
        return graph

    def create_graph_indicator(self, axes, get_t, get_s):
        """Vertical line indicator on the graph."""
        v_line = Line(DOWN, UP)
        v_line.set_stroke(WHITE, 2)
        v_line.f_always.put_start_and_end_on(
            lambda: axes.c2p(get_t(), 0),
            lambda: axes.c2p(get_t(), np.exp(get_s() * get_t()).real),
        )
        return v_line

    def play_time_forward(self, duration, added_anims=[]):
        """Utility to animate time passing."""
        self.t_tracker.set_value(0)
        self.play(
            self.t_tracker.animate.set_value(duration).set_anim_args(rate_func=linear),
            *added_anims,
            run_time=duration,
        )

    def explore_s_values(self):
        """Explore different s values and their effects."""
        s_tracker = self.s_tracker

        # Start with negative real (decay)
        s_tracker.set_value(-1)
        self.play(s_tracker.animate.set_value(0.2), run_time=4)

        # Pure real = 0 (constant)
        self.play(s_tracker.animate.set_value(0), run_time=2)

        # Pure imaginary (oscillation)
        self.play(s_tracker.animate.set_value(1j), run_time=3)
        self.wait()

        # Let time run
        self.play_time_forward(3 * TAU)
        self.wait()

        # Reset time
        self.play(self.t_tracker.animate.set_value(0), run_time=2)

        # Complex with negative real (decaying oscillation)
        self.play(s_tracker.animate.set_value(-0.2 + 1j), run_time=3)
        self.play_time_forward(2 * TAU)

        # Complex with positive real (growing oscillation)
        self.t_tracker.set_value(0)
        self.play(s_tracker.animate.set_value(0.1 + 1j), run_time=3)
        self.play_time_forward(TAU)


class SPlaneRegions(InteractiveScene):
    """
    Highlight different regions of the s-plane and their meaning:
    - Right half: exponential growth
    - Left half: exponential decay
    - Imaginary axis: pure oscillation
    """

    def construct(self):
        # S-plane
        plane = ComplexPlane((-3, 3), (-3, 3))
        plane.set_height(6)
        plane.add_coordinate_labels(font_size=20)

        self.add(plane)

        # Right half (growth)
        right_half = Rectangle(width=plane.get_width()/2, height=plane.get_height())
        right_half.set_fill(RED, 0.3)
        right_half.set_stroke(width=0)
        right_half.move_to(plane.n2p(1.5))

        # Left half (decay)
        left_half = Rectangle(width=plane.get_width()/2, height=plane.get_height())
        left_half.set_fill(GREEN, 0.3)
        left_half.set_stroke(width=0)
        left_half.move_to(plane.n2p(-1.5))

        # Imaginary axis highlight
        imag_axis = Line(plane.n2p(-3j), plane.n2p(3j))
        imag_axis.set_stroke(YELLOW, 4)

        # Labels
        growth_label = Text("Growth", color=RED)
        growth_label.move_to(plane.n2p(1.5 + 2j))

        decay_label = Text("Decay", color=GREEN)
        decay_label.move_to(plane.n2p(-1.5 + 2j))

        osc_label = Text("Oscillation", color=YELLOW)
        osc_label.next_to(imag_axis, RIGHT)
        osc_label.shift(UP)

        # Animate
        self.play(FadeIn(right_half), Write(growth_label))
        self.wait()

        self.play(FadeIn(left_half), Write(decay_label))
        self.wait()

        self.play(ShowCreation(imag_axis), Write(osc_label))
        self.wait(2)

        # Add sample points
        sample_points = [
            (1, RED, "Grows"),
            (-1, GREEN, "Decays"),
            (1j, YELLOW, "Oscillates"),
            (-0.5 + 1j, TEAL, "Decays + Oscillates"),
        ]

        dots = VGroup()
        for s, color, label_text in sample_points:
            dot = GlowDot(plane.n2p(s), color=color)
            label = Text(label_text, font_size=24, color=color)
            label.next_to(dot, UR, buff=0.1)
            dots.add(VGroup(dot, label))

        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.5))
        self.wait(2)
