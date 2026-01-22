"""
ReLU Activation Function Visualization
Shows the ReLU and GELU activation functions used in neural networks.
"""
from manimlib import *
from scipy.stats import norm


class ReLUVisualization(InteractiveScene):
    """
    Visualizes the ReLU (Rectified Linear Unit) activation function
    and compares it with GELU.

    Demonstrates: Axes, graph plotting, labels, transitions
    """

    def construct(self):
        # Create axes for the activation function
        axes = Axes(
            x_range=(-4, 4),
            y_range=(-1, 4),
            axis_config=dict(include_tip=True),
        )
        axes.set_width(8)
        axes.add_coordinate_labels(font_size=20)

        # Graph ReLU: f(x) = max(0, x)
        relu_graph = axes.get_graph(
            lambda x: max(0, x),
            discontinuities=[0]
        )
        relu_graph.set_stroke(YELLOW, 4)

        # Labels
        relu_title = Text("Rectified Linear Unit (ReLU)", font_size=36)
        relu_title.to_edge(UP)

        relu_label = Text("ReLU", font_size=30)
        relu_label.set_color(YELLOW)
        relu_label.move_to(axes.c2p(2, 3))

        # Formula
        relu_formula = Tex(R"f(x) = \max(0, x)", font_size=36)
        relu_formula.next_to(axes, DOWN)

        # Animate building the scene
        self.play(Write(axes))
        self.play(
            Write(relu_title),
            ShowCreation(relu_graph, run_time=2)
        )
        self.play(
            FadeIn(relu_label),
            Write(relu_formula)
        )
        self.wait(2)

        # Show GELU comparison
        gelu_graph = axes.get_graph(lambda x: x * norm.cdf(x))
        gelu_graph.set_stroke(GREEN, 4)

        gelu_label = Text("GELU", font_size=30)
        gelu_label.set_color(GREEN)
        gelu_label.next_to(relu_label, DOWN, buff=0.5, aligned_edge=LEFT)

        gelu_title = Text("Gaussian Error Linear Unit (GELU)", font_size=36)
        gelu_title.to_edge(UP)

        self.play(
            relu_graph.animate.set_stroke(opacity=0.3),
            relu_label.animate.set_fill(opacity=0.3),
            FadeTransform(relu_title, gelu_title),
            ShowCreation(gelu_graph),
            FadeIn(gelu_label)
        )
        self.wait(2)

        # Back to ReLU
        self.play(
            gelu_graph.animate.set_stroke(opacity=0.3),
            gelu_label.animate.set_fill(opacity=0.3),
            relu_graph.animate.set_stroke(opacity=1),
            relu_label.animate.set_fill(opacity=1),
            FadeTransform(gelu_title, relu_title)
        )
        self.wait(2)


class ReLUNeuronBehavior(InteractiveScene):
    """
    Shows how ReLU affects neuron values - negative values become 0,
    positive values pass through unchanged.

    Demonstrates: DecimalNumber, color coding, visual feedback
    """

    def construct(self):
        # Create input values
        input_values = [-3.5, -1.2, 0.5, 2.8, -0.7, 1.5, 4.2, -2.1, 0.0]
        output_values = [max(0, v) for v in input_values]

        # Create input column
        input_entries = VGroup()
        output_entries = VGroup()

        for val in input_values:
            entry = DecimalNumber(val, num_decimal_places=1, include_sign=True)
            entry.set_color(BLUE if val >= 0 else RED)
            input_entries.add(entry)

        for val in output_values:
            entry = DecimalNumber(val, num_decimal_places=1, include_sign=True)
            entry.set_color(BLUE if val > 0 else GREY)
            output_entries.add(entry)

        input_entries.arrange(DOWN, buff=0.3)
        output_entries.arrange(DOWN, buff=0.3)

        # Add brackets
        input_group = VGroup(
            Tex("["),
            input_entries,
            Tex("]")
        )
        input_group[0].next_to(input_entries, LEFT)
        input_group[2].next_to(input_entries, RIGHT)

        output_group = VGroup(
            Tex("["),
            output_entries,
            Tex("]")
        )
        output_group[0].next_to(output_entries, LEFT)
        output_group[2].next_to(output_entries, RIGHT)

        # Position groups
        input_group.move_to(2 * LEFT)
        output_group.move_to(2 * RIGHT)

        # Arrow with ReLU label
        arrow = Arrow(input_group.get_right(), output_group.get_left(), buff=0.3)
        relu_label = Text("ReLU", font_size=36)
        relu_label.next_to(arrow, UP)

        # Title
        title = Text("ReLU: Negative values become zero", font_size=36)
        title.to_edge(UP)

        # Animate
        self.play(Write(title))
        self.play(FadeIn(input_group, shift=LEFT))
        self.play(
            GrowArrow(arrow),
            FadeIn(relu_label)
        )
        self.wait()

        # Transform input to output with highlighting
        for i, (inp, out) in enumerate(zip(input_entries, output_entries)):
            inp_copy = inp.copy()
            if input_values[i] < 0:
                # Highlight negative -> zero transformation
                self.play(
                    Transform(inp_copy, out),
                    Flash(inp, color=RED),
                    run_time=0.5
                )
            else:
                self.play(
                    Transform(inp_copy, out),
                    run_time=0.3
                )
            output_group.add(inp_copy)

        self.play(
            FadeIn(output_group[0]),
            FadeIn(output_group[2])
        )
        self.wait(2)
