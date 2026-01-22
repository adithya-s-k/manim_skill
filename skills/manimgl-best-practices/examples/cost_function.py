"""
Negative Log Loss (Cross-Entropy) cost function visualization.
Demonstrates: Graph plotting, labeled axes, mathematical expressions
"""
from manimlib import *
import numpy as np


class CostFunction(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            (0, 1, 0.1),
            (0, 5, 1),
            width=10,
            height=6
        )
        axes.center().to_edge(LEFT)
        axes.x_axis.add_numbers(num_decimal_places=1)
        axes.y_axis.add_numbers(num_decimal_places=0, direction=LEFT)

        # Add axis label
        x_label = Tex("p")
        x_label.next_to(axes.x_axis.get_right(), UR)
        axes.add(x_label)

        y_label = Text("Cost", font_size=36)
        y_label.next_to(axes.y_axis.get_top(), RIGHT)
        axes.add(y_label)

        # Create the -log(p) graph
        graph = axes.get_graph(
            lambda x: -np.log(x) if x > 0.001 else 5,
            x_range=(0.001, 1, 0.01)
        )
        graph.set_color(RED)

        # Expression
        expr = Tex(R"\text{Cost} = -\log(p)", font_size=60)
        expr.to_edge(UP)

        # Animate
        self.play(FadeIn(axes))
        self.wait(0.5)

        self.play(
            ShowCreation(graph, run_time=3),
            Write(expr, run_time=2),
        )
        self.wait()

        # Explanation labels
        low_p_label = Text("Low probability\n= High cost", font_size=30, color=RED)
        low_p_label.next_to(axes.i2gp(0.1, graph), RIGHT, buff=0.5)

        high_p_label = Text("High probability\n= Low cost", font_size=30, color=GREEN)
        high_p_label.next_to(axes.i2gp(0.8, graph), UP, buff=0.5)

        self.play(FadeIn(low_p_label, shift=LEFT))
        self.wait()
        self.play(FadeIn(high_p_label, shift=DOWN))
        self.wait()

        # Show a moving dot on the curve
        p_tracker = ValueTracker(0.5)

        dot = Dot(color=YELLOW)
        dot.f_always.move_to(lambda: axes.i2gp(p_tracker.get_value(), graph))

        # Vertical line from x-axis to point
        v_line = always_redraw(lambda: axes.get_line_from_axis_to_point(
            0, axes.i2gp(p_tracker.get_value(), graph),
            line_func=DashedLine
        ).set_stroke(YELLOW, 2))

        # Horizontal line from y-axis to point
        h_line = always_redraw(lambda: axes.get_line_from_axis_to_point(
            1, axes.i2gp(p_tracker.get_value(), graph),
            line_func=DashedLine
        ).set_stroke(YELLOW, 2))

        # Value labels
        p_label = VGroup(
            Text("p = ", font_size=36),
            DecimalNumber(p_tracker.get_value(), num_decimal_places=2, font_size=36)
        )
        p_label.arrange(RIGHT)
        p_label.to_corner(UR)
        p_label[1].f_always.set_value(p_tracker.get_value)

        cost_label = VGroup(
            Text("Cost = ", font_size=36),
            DecimalNumber(-np.log(0.5), num_decimal_places=2, font_size=36)
        )
        cost_label.arrange(RIGHT)
        cost_label.next_to(p_label, DOWN, aligned_edge=LEFT)
        cost_label[1].f_always.set_value(lambda: -np.log(max(p_tracker.get_value(), 0.001)))

        self.play(
            FadeOut(low_p_label),
            FadeOut(high_p_label),
            FadeIn(dot),
            FadeIn(v_line),
            FadeIn(h_line),
            FadeIn(p_label),
            FadeIn(cost_label),
        )
        self.wait()

        # Animate the dot moving
        self.play(p_tracker.animate.set_value(0.1), run_time=2)
        self.wait()
        self.play(p_tracker.animate.set_value(0.9), run_time=3)
        self.wait()
        self.play(p_tracker.animate.set_value(0.05), run_time=2)
        self.wait()
        self.play(p_tracker.animate.set_value(0.5), run_time=2)
        self.wait()

        # Final message
        message = Text(
            "Goal: Maximize probability of correct answer",
            font_size=36,
            color=BLUE
        )
        message.to_edge(DOWN)
        self.play(FadeIn(message, shift=UP))
        self.wait(2)
