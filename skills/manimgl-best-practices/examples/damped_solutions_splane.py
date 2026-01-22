"""
Damped Spring Solutions on S-Plane

Visualization of how the damped harmonic oscillator solutions
move in the complex s-plane as parameters change.

Run: manimgl damped_solutions_splane.py DampedSolutionsDemo -w
Preview: manimgl damped_solutions_splane.py DampedSolutionsDemo -p

Source: Adapted from 3b1b's Laplace transform video (2025)
"""
from manimlib import *


class DampedSolutionsDemo(InteractiveScene):
    """
    Interactive visualization of damped spring solutions on the s-plane.

    The characteristic equation ms^2 + μs + k = 0 has roots that:
    - Stay on imaginary axis when μ=0 (undamped oscillation)
    - Move into left half-plane as μ increases (damped oscillation)
    - Become real when μ^2 > 4mk (overdamped)

    Key techniques:
    - Custom slider creation
    - GlowDot for interactive points
    - Dynamic function binding for graphs
    - Real-time root calculation
    """

    def construct(self):
        # Add the complex plane
        plane = ComplexPlane((-3, 2), (-2, 2))
        plane.set_height(5)
        plane.background_lines.set_stroke(BLUE, 1)
        plane.faded_lines.set_stroke(BLUE, 0.5, 0.25)
        plane.add_coordinate_labels(font_size=24)
        plane.move_to(DOWN)
        plane.to_edge(RIGHT, buff=1.0)

        self.add(plane)

        # Parameter sliders
        colors = [interpolate_color_by_hsl(RED, TEAL, a) for a in np.linspace(0, 1, 3)]
        chars = ["m", R"\mu", "k"]

        m_slider, mu_slider, k_slider = sliders = VGroup(
            self.create_slider(char, color)
            for char, color in zip(chars, colors)
        )
        m_tracker, mu_tracker, k_tracker = trackers = Group(
            slider.value_tracker for slider in sliders
        )

        sliders.arrange(RIGHT, buff=MED_LARGE_BUFF)
        sliders.next_to(plane, UP, aligned_edge=LEFT)

        # Initial values: m=1, μ=0, k=3
        m_tracker.set_value(1)
        mu_tracker.set_value(0)
        k_tracker.set_value(3)

        self.add(trackers)
        self.add(sliders[0], sliders[2])  # Start without damping slider

        # Root calculation
        def get_roots():
            a = m_tracker.get_value()
            b = mu_tracker.get_value()
            c = k_tracker.get_value()

            # Characteristic equation: as^2 + bs + c = 0
            # s = (-b ± sqrt(b^2 - 4ac)) / 2a
            discriminant = b**2 - 4*a*c
            if discriminant >= 0:
                radical = math.sqrt(discriminant)
            else:
                radical = 1j * math.sqrt(-discriminant)

            m = -b / (2*a)
            return (m + radical / (2*a), m - radical / (2*a))

        # Dots showing the roots
        root_dots = GlowDot().replicate(2)
        root_dots.set_color(YELLOW)

        def update_dots(dots):
            roots = get_roots()
            for dot, root in zip(dots, roots):
                dot.move_to(plane.n2p(root))

        root_dots.add_updater(update_dots)
        self.add(root_dots)

        # Lines from a reference point
        s_rhs_point = Point((-4.09, -1.0, 0.0))

        def update_lines(lines):
            for line, dot in zip(lines, root_dots):
                line.put_start_and_end_on(s_rhs_point.get_center(), dot.get_center())

        lines = Line().replicate(2)
        lines.set_stroke(YELLOW, 2, 0.35)
        lines.add_updater(update_lines)

        # Show the roots moving as k changes (undamped case)
        self.play(ShowCreation(lines, lag_ratio=0, suspend_mobject_updating=True))
        self.play(k_tracker.animate.set_value(1), run_time=2)
        self.play(m_tracker.animate.set_value(4), run_time=2)
        self.wait()
        self.play(k_tracker.animate.set_value(3), run_time=2)
        self.play(m_tracker.animate.set_value(1), run_time=2)
        self.wait()

        # Now add damping
        self.play(
            VFadeOut(lines),
            VFadeIn(sliders[1])
        )
        self.wait()

        # Increase damping - roots move left
        self.play(mu_tracker.animate.set_value(3), run_time=5)
        self.wait()

        # Decrease damping - roots approach imaginary axis
        self.play(mu_tracker.animate.set_value(0.5), run_time=3)
        self.play(ShowCreation(lines, lag_ratio=0, suspend_mobject_updating=True))
        self.wait()

        # Add solution graph
        frame = self.frame

        axes = Axes((0, 10, 1), (-1, 1, 1), width=10, height=3.5)
        axes.next_to(plane, DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)

        def solution_func(t):
            roots = get_roots()
            # Real part of e^{s1*t} + e^{s2*t} (divided by 2 for normalization)
            return 0.5 * (np.exp(roots[0] * t) + np.exp(roots[1] * t)).real

        graph = axes.get_graph(solution_func)
        graph.set_stroke(TEAL, 3)
        axes.bind_graph_to_func(graph, solution_func)

        graph_label = Tex(R"\text{Re}[e^{st}]", t2c={"s": YELLOW}, font_size=72)
        graph_label.next_to(axes.get_corner(UL), DL)

        self.play(
            frame.animate.set_height(12, about_point=4 * UP + 2 * LEFT),
            FadeIn(axes, time_span=(1.5, 3)),
            ShowCreation(graph, suspend_mobject_updating=True, time_span=(1.5, 3)),
            Write(graph_label),
            run_time=3
        )
        self.wait()

        # More parameter exploration
        self.play(k_tracker.animate.set_value(1), run_time=2)
        self.play(k_tracker.animate.set_value(4), run_time=2)
        self.wait()

        self.play(mu_tracker.animate.set_value(2), run_time=3)
        self.play(k_tracker.animate.set_value(2), run_time=2)
        self.wait()

        # Show overdamped case
        self.play(mu_tracker.animate.set_value(3.5), run_time=3)
        self.play(k_tracker.animate.set_value(5), run_time=2)
        self.wait()

        # Return to underdamped
        self.play(
            mu_tracker.animate.set_value(0.5),
            m_tracker.animate.set_value(3),
            run_time=3
        )
        self.wait(2)

    def create_slider(self, char_name, color=WHITE, x_range=(0, 5), height=1.5, font_size=36):
        """Create a vertical slider for a parameter."""
        tracker = ValueTracker(0)
        number_line = NumberLine(x_range, width=height, tick_size=0.05)
        number_line.rotate(90 * DEG)

        indicator = ArrowTip(width=0.1, length=0.2)
        indicator.rotate(PI)
        indicator.add_updater(lambda m: m.move_to(number_line.n2p(tracker.get_value()), LEFT))
        indicator.set_color(color)

        label = Tex(Rf"{char_name} = 0.00", font_size=font_size)
        label[char_name].set_color(color)
        label.rhs = label.make_number_changeable("0.00")
        label.always.next_to(indicator, RIGHT, SMALL_BUFF)
        label.rhs.f_always.set_value(tracker.get_value)

        slider = VGroup(number_line, indicator, label)
        slider.value_tracker = tracker
        return slider


class OverdampedVsUnderdamped(InteractiveScene):
    """
    Side-by-side comparison of overdamped and underdamped behavior.
    """

    def construct(self):
        # Two planes side by side
        plane_underdamped = ComplexPlane((-2, 1), (-2, 2))
        plane_overdamped = ComplexPlane((-2, 1), (-2, 2))

        for plane in [plane_underdamped, plane_overdamped]:
            plane.set_width(5)
            plane.add_coordinate_labels(font_size=16)

        planes = VGroup(plane_underdamped, plane_overdamped)
        planes.arrange(RIGHT, buff=1)
        planes.to_edge(UP)

        # Labels
        underdamped_label = Text("Underdamped", font_size=36, color=BLUE)
        underdamped_label.next_to(plane_underdamped, DOWN)

        overdamped_label = Text("Overdamped", font_size=36, color=RED)
        overdamped_label.next_to(plane_overdamped, DOWN)

        self.add(planes, underdamped_label, overdamped_label)

        # Roots for underdamped: complex conjugates
        underdamped_roots = [-0.5 + 1.5j, -0.5 - 1.5j]
        underdamped_dots = VGroup(
            GlowDot(plane_underdamped.n2p(r), color=BLUE)
            for r in underdamped_roots
        )

        # Roots for overdamped: both real
        overdamped_roots = [-0.3, -1.7]
        overdamped_dots = VGroup(
            GlowDot(plane_overdamped.n2p(r), color=RED)
            for r in overdamped_roots
        )

        self.play(
            LaggedStartMap(FadeIn, underdamped_dots),
            LaggedStartMap(FadeIn, overdamped_dots),
        )
        self.wait()

        # Graphs below
        axes_underdamped = Axes((0, 8), (-1, 1), width=5, height=2)
        axes_overdamped = Axes((0, 8), (-1, 1), width=5, height=2)

        axes_underdamped.next_to(underdamped_label, DOWN)
        axes_overdamped.next_to(overdamped_label, DOWN)

        # Underdamped solution: decaying oscillation
        def underdamped_func(t):
            s = underdamped_roots[0]
            return (np.exp(s * t)).real

        # Overdamped solution: pure decay
        def overdamped_func(t):
            s1, s2 = overdamped_roots
            return 0.5 * (np.exp(s1 * t) + np.exp(s2 * t))

        graph_under = axes_underdamped.get_graph(underdamped_func)
        graph_under.set_stroke(BLUE, 3)

        graph_over = axes_overdamped.get_graph(overdamped_func)
        graph_over.set_stroke(RED, 3)

        self.add(axes_underdamped, axes_overdamped)
        self.play(
            ShowCreation(graph_under),
            ShowCreation(graph_over),
            run_time=3
        )
        self.wait(2)
