"""
Linear Regression visualization showing data points and a fitted line.
Demonstrates: Axes, DotCloud, Line, ValueTracker, updaters
"""
from manimlib import *
import numpy as np
import random


class LinearRegression(Scene):
    def construct(self):
        # Set up axes
        x_min, x_max = (-1, 12)
        y_min, y_max = (-1, 10)
        axes = Axes((x_min, x_max), (y_min, y_max), width=12, height=6)
        axes.to_edge(DOWN)
        self.add(axes)

        # Add data points
        n_data_points = 30
        m = 0.75  # slope
        y0 = 1    # y-intercept

        np.random.seed(42)
        data = np.array([
            (x, y0 + m * x + 0.75 * np.random.normal(0, 1))
            for x in np.random.uniform(2, x_max, n_data_points)
        ])
        points = axes.c2p(data[:, 0], data[:, 1])
        dots = DotCloud(points)
        dots.set_color(YELLOW)
        dots.set_glow_factor(1)
        dots.set_radius(0.075)

        self.add(dots)

        # Title
        title = Text("Linear Regression", font_size=72)
        title.to_edge(UP)

        # Create line with trackers for slope and y-intercept
        m_tracker = ValueTracker(m)
        y0_tracker = ValueTracker(y0)
        line = Line()
        line.set_stroke(TEAL, 2)

        def update_line(line):
            curr_y0 = y0_tracker.get_value()
            curr_m = m_tracker.get_value()
            line.put_start_and_end_on(
                axes.c2p(0, curr_y0),
                axes.c2p(x_max, curr_y0 + curr_m * x_max),
            )

        line.add_updater(update_line)

        self.play(
            FadeIn(title, UP),
            ShowCreation(line),
        )
        self.wait()

        # Label inputs and outputs
        in_label = Text("Input")
        in_label.next_to(axes.x_axis, DOWN, buff=0.1, aligned_edge=RIGHT)
        out_label = Text("Output")
        out_label.rotate(90 * DEGREES)
        out_label.next_to(axes.y_axis, LEFT, aligned_edge=UP)

        self.play(LaggedStart(
            FadeIn(in_label, lag_ratio=0.1),
            FadeIn(out_label, lag_ratio=0.1),
            lag_ratio=0.5,
        ))
        self.wait()

        # Emphasize line
        self.play(
            VShowPassingFlash(
                line.copy().set_stroke(BLUE, 8).scale(1.1).insert_n_curves(100),
                time_width=1.5,
                run_time=2
            ),
        )
        self.wait()

        # Show parameter labels
        m_label = VGroup(
            Text("slope = "),
            DecimalNumber(m_tracker.get_value()),
        )
        m_label.arrange(RIGHT)
        m_label[1].f_always.set_value(m_tracker.get_value)

        y0_label = VGroup(
            Text("y-intercept = "),
            DecimalNumber(y0_tracker.get_value()),
        )
        y0_label.arrange(RIGHT)
        y0_label[1].f_always.set_value(y0_tracker.get_value)

        labels = VGroup(m_label, y0_label)
        labels.arrange(DOWN, aligned_edge=LEFT)
        labels.next_to(axes.y_axis, RIGHT, buff=1.0)
        labels.to_edge(UP)

        self.play(
            FadeOut(title, UP),
            FadeIn(m_label, UP),
        )
        self.play(
            m_tracker.animate.set_value(1.5),
            run_time=2,
        )
        self.play(FadeIn(y0_label, UP))
        self.play(
            y0_tracker.animate.set_value(-2),
            run_time=2
        )
        self.wait()

        # Tweak line parameters to show fitting
        for n in range(6):
            alpha = random.random()
            if alpha > 0.5:
                alpha += 1
            new_m = interpolate(m_tracker.get_value(), m, alpha)
            new_y0 = interpolate(y0_tracker.get_value(), y0, alpha)
            self.play(LaggedStart(
                m_tracker.animate.set_value(new_m),
                y0_tracker.animate.set_value(new_y0),
                run_time=1.5,
                lag_ratio=0.25,
            ))
            self.wait(0.5)
