"""
Neuron Activation Visualization
Shows neurons firing based on input patterns, with active/inactive states.
"""
from manimlib import *
import numpy as np


class NeuronActivationStates(InteractiveScene):
    """
    Visualizes neurons as dots with varying activation levels.
    Active neurons glow, inactive neurons are dim.

    Demonstrates: Dot animations, opacity changes, highlighting
    """

    def construct(self):
        # Title
        title = Text("Neuron Activations", font_size=48)
        title.to_edge(UP)

        # Create a column of neurons (dots)
        neuron_values = [0.0, 0.8, 0.0, 0.5, 0.9, 0.0, 0.3, 0.0, 0.7]
        neurons = VGroup()

        for val in neuron_values:
            neuron = Dot(radius=0.25)
            neuron.set_stroke(WHITE, 2)
            # Active neurons are bright, inactive are dim
            if val > 0:
                neuron.set_fill(BLUE, opacity=val)
            else:
                neuron.set_fill(GREY_D, opacity=0.3)
            neurons.add(neuron)

        neurons.arrange(DOWN, buff=0.15)
        neurons.set_height(5)
        neurons.move_to(ORIGIN)

        # Add labels showing activation values
        labels = VGroup()
        for i, (neuron, val) in enumerate(zip(neurons, neuron_values)):
            label = DecimalNumber(val, num_decimal_places=1, font_size=24)
            label.next_to(neuron, RIGHT, buff=0.5)
            if val > 0:
                label.set_color(BLUE)
            else:
                label.set_color(GREY)
            labels.add(label)

        # Animate appearance
        self.play(Write(title))
        self.play(
            LaggedStartMap(GrowFromCenter, neurons, lag_ratio=0.1)
        )
        self.play(
            LaggedStartMap(FadeIn, labels, shift=LEFT, lag_ratio=0.1)
        )
        self.wait()

        # Highlight active vs inactive
        active_rect = SurroundingRectangle(
            VGroup(neurons[1], neurons[4], neurons[6], neurons[8]),
            buff=0.15
        )
        active_rect.set_stroke(GREEN, 3)
        active_label = Text("Active", font_size=30, color=GREEN)
        active_label.next_to(active_rect, LEFT, buff=0.5)

        inactive_rect = SurroundingRectangle(
            VGroup(neurons[0], neurons[2], neurons[5], neurons[7]),
            buff=0.15
        )
        inactive_rect.set_stroke(RED, 3)
        inactive_label = Text("Inactive", font_size=30, color=RED)
        inactive_label.next_to(inactive_rect, LEFT, buff=0.5)

        self.play(
            ShowCreation(active_rect),
            FadeIn(active_label)
        )
        self.wait()
        self.play(
            ShowCreation(inactive_rect),
            FadeIn(inactive_label)
        )
        self.wait(2)

        # Show activation changing
        self.play(
            FadeOut(active_rect),
            FadeOut(active_label),
            FadeOut(inactive_rect),
            FadeOut(inactive_label)
        )

        # Animate neurons activating/deactivating
        new_values = [0.9, 0.0, 0.6, 0.0, 0.0, 0.8, 0.0, 0.4, 0.0]

        anims = []
        for neuron, label, old_val, new_val in zip(neurons, labels, neuron_values, new_values):
            if new_val > 0:
                anims.append(neuron.animate.set_fill(BLUE, opacity=new_val))
            else:
                anims.append(neuron.animate.set_fill(GREY_D, opacity=0.3))
            anims.append(ChangeDecimalToValue(label, new_val))
            if new_val > 0:
                anims.append(label.animate.set_color(BLUE))
            else:
                anims.append(label.animate.set_color(GREY))

        self.play(*anims, run_time=2)
        self.wait(2)


class ClassicNeuronDiagram(InteractiveScene):
    """
    Shows the classic neural network diagram with connected nodes.
    Inputs feed into hidden layer neurons which connect to outputs.

    Demonstrates: VGroup, Line connections, network structure
    """

    def construct(self):
        # Title
        title = Text("Neural Network Layer", font_size=42)
        title.to_edge(UP)

        # Create three layers
        input_layer = VGroup(
            Dot(radius=0.2) for _ in range(4)
        )
        input_layer.arrange(DOWN, buff=0.5)
        input_layer.set_fill(YELLOW, 0.8)
        input_layer.set_stroke(WHITE, 2)

        hidden_layer = VGroup(
            Dot(radius=0.2) for _ in range(6)
        )
        hidden_layer.arrange(DOWN, buff=0.35)
        hidden_layer.set_stroke(WHITE, 2)

        output_layer = VGroup(
            Dot(radius=0.2) for _ in range(3)
        )
        output_layer.arrange(DOWN, buff=0.6)
        output_layer.set_fill(GREEN, 0.8)
        output_layer.set_stroke(WHITE, 2)

        # Position layers
        layers = VGroup(input_layer, hidden_layer, output_layer)
        layers.arrange(RIGHT, buff=2.5)

        # Create connections
        def create_connections(layer1, layer2):
            lines = VGroup()
            for n1 in layer1:
                for n2 in layer2:
                    line = Line(n1.get_center(), n2.get_center(), buff=0.2)
                    line.set_stroke(GREY, 1, opacity=0.5)
                    lines.add(line)
            return lines

        connections1 = create_connections(input_layer, hidden_layer)
        connections2 = create_connections(hidden_layer, output_layer)

        # Layer labels
        input_label = Text("Input", font_size=28)
        input_label.next_to(input_layer, DOWN)
        hidden_label = Text("Hidden", font_size=28)
        hidden_label.next_to(hidden_layer, DOWN)
        output_label = Text("Output", font_size=28)
        output_label.next_to(output_layer, DOWN)

        # Animate construction
        self.play(Write(title))
        self.play(
            LaggedStartMap(GrowFromCenter, input_layer, lag_ratio=0.2),
            FadeIn(input_label)
        )
        self.play(
            ShowCreation(connections1, lag_ratio=0.01, run_time=2),
            LaggedStartMap(GrowFromCenter, hidden_layer, lag_ratio=0.1),
            FadeIn(hidden_label)
        )
        self.play(
            ShowCreation(connections2, lag_ratio=0.01, run_time=2),
            LaggedStartMap(GrowFromCenter, output_layer, lag_ratio=0.2),
            FadeIn(output_label)
        )
        self.wait()

        # Show activation propagating
        for i, neuron in enumerate(hidden_layer):
            # Random activation
            activation = np.random.random()
            if activation > 0.5:
                neuron.set_fill(BLUE, activation)
            else:
                neuron.set_fill(GREY_D, 0.3)

        self.play(
            LaggedStart(
                *(
                    neuron.animate.set_fill(
                        BLUE if np.random.random() > 0.4 else GREY_D,
                        np.random.random() if np.random.random() > 0.4 else 0.3
                    )
                    for neuron in hidden_layer
                ),
                lag_ratio=0.1
            )
        )
        self.wait()

        # Highlight signal flow with VShowPassingFlash
        flash_lines = connections1.copy()
        for line in flash_lines:
            line.set_stroke(YELLOW, 3)
            line.insert_n_curves(20)

        self.play(
            LaggedStartMap(
                VShowPassingFlash,
                flash_lines,
                time_width=0.5,
                lag_ratio=0.02,
                run_time=2
            )
        )

        flash_lines2 = connections2.copy()
        for line in flash_lines2:
            line.set_stroke(GREEN, 3)
            line.insert_n_curves(20)

        self.play(
            LaggedStartMap(
                VShowPassingFlash,
                flash_lines2,
                time_width=0.5,
                lag_ratio=0.02,
                run_time=2
            )
        )
        self.wait(2)
