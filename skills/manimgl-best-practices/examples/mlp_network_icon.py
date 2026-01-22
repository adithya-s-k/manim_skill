"""
MLP Network Icon - A simple visualization of a multilayer perceptron structure
Shows dots arranged in layers with connecting lines between neurons.
"""
from manimlib import *
import random


class MLPNetworkIcon(InteractiveScene):
    """
    Creates a classic MLP icon with three layers:
    - Input layer
    - Hidden layer (wider)
    - Output layer

    Demonstrates: VGroup organization, Line connections, random styling
    """

    def construct(self):
        # Create the MLP icon
        network = self.get_mlp_icon(layer_buff=2.5, layer0_size=5)

        # Animate the network appearing
        self.play(Write(network, stroke_width=0.5, lag_ratio=1e-2, run_time=3))
        self.wait()

        # Show data propagating through the network
        lines = VGroup(network[1].family_members_with_points()).copy()
        for line in lines:
            line.set_stroke(width=2 * line.get_width())
            line.insert_n_curves(20)

        self.play(
            LaggedStartMap(
                VShowPassingFlash,
                lines,
                time_width=1.5,
                lag_ratio=5e-3,
                run_time=3
            )
        )
        self.wait()

    def get_mlp_icon(self, dot_buff=0.15, layer_buff=1.5, layer0_size=5):
        """
        Creates an MLP icon with three layers.

        Args:
            dot_buff: Spacing between neurons in a layer
            layer_buff: Spacing between layers
            layer0_size: Number of neurons in input/output layers
        """
        # Create three layers of dots
        layers = VGroup(
            Dot().get_grid(layer0_size, 1, buff=dot_buff),
            Dot().get_grid(2 * layer0_size, 1, buff=dot_buff),  # Hidden layer is wider
            Dot().get_grid(layer0_size, 1, buff=dot_buff),
        )
        layers.set_height(4)
        layers.arrange(RIGHT, buff=layer_buff)

        # Set random opacities for visual interest
        for layer in layers:
            for dot in layer:
                dot.set_fill(opacity=random.random())
        layers.set_stroke(WHITE, 0.5)

        # Create connection lines between layers
        lines = VGroup(
            Line(
                dot1.get_center(),
                dot2.get_center(),
                buff=dot1.get_width() / 2
            )
            for l1, l2 in zip(layers, layers[1:])
            for dot1 in l1
            for dot2 in l2
        )

        # Color and style the lines randomly
        for line in lines:
            line.set_stroke(
                color=self.value_to_color(random.uniform(-10, 10)),
                width=3 * random.random()**3
            )

        return VGroup(layers, lines)

    def value_to_color(
        self,
        value,
        low_positive_color=BLUE_E,
        high_positive_color=BLUE_B,
        low_negative_color=RED_E,
        high_negative_color=RED_B,
        min_value=0.0,
        max_value=10.0
    ):
        """Maps a numeric value to a color based on its sign and magnitude."""
        alpha = clip(float(inverse_interpolate(min_value, max_value, abs(value))), 0, 1)
        if value >= 0:
            colors = (low_positive_color, high_positive_color)
        else:
            colors = (low_negative_color, high_negative_color)
        return interpolate_color_by_hsl(*colors, alpha)
