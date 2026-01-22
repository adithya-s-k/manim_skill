"""
MLP Forward Pass Visualization
Shows data flowing through Linear -> ReLU -> Linear operations.
"""
from manimlib import *
import numpy as np


def value_to_color(value, max_value=10.0):
    """Maps a value to blue (positive) or red (negative)."""
    alpha = clip(abs(value) / max_value, 0, 1)
    if value >= 0:
        return interpolate_color_by_hsl(BLUE_E, BLUE_B, alpha)
    else:
        return interpolate_color_by_hsl(RED_E, RED_B, alpha)


class MLPForwardPass(InteractiveScene):
    """
    Shows the three-step MLP forward pass:
    1. Linear transformation (matrix multiply + bias)
    2. ReLU activation
    3. Linear transformation (matrix multiply + bias)

    Demonstrates: Sequential animations, data transformation visualization
    """

    def construct(self):
        # Title
        title = Text("MLP Forward Pass", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))

        # Create the three arrows showing the pipeline
        arrows = VGroup(
            Arrow(ORIGIN, 1.8 * RIGHT) for _ in range(3)
        )
        arrows.arrange(RIGHT, buff=0.8)
        arrows.move_to(ORIGIN)

        # Labels for each stage
        labels = VGroup(
            Text("Linear", font_size=28),
            Text("ReLU", font_size=28),
            Text("Linear", font_size=28),
        )
        for label, arrow in zip(labels, arrows):
            label.next_to(arrow, UP, buff=0.1)

        # Position for vectors at each stage
        # Input vector
        input_values = np.array([1.5, -0.8, 2.1, -1.4, 0.6])
        input_vect = self.create_vector(input_values, YELLOW)
        input_vect.next_to(arrows[0], LEFT, buff=0.5)

        # After first linear (expanded to 8 neurons)
        mid1_values = np.array([2.3, -1.5, 0.8, -2.1, 1.9, -0.3, 0.1, -1.8])
        mid1_vect = self.create_vector(mid1_values, None)  # Will color by value

        # After ReLU (negative values zeroed)
        relu_values = np.maximum(mid1_values, 0)
        relu_vect = self.create_vector(relu_values, None, zero_color=GREY)

        # After second linear (back to 5 output neurons)
        output_values = np.array([1.2, 0.5, -0.3, 1.8, 0.9])
        output_vect = self.create_vector(output_values, GREEN)

        # Position intermediate vectors
        vects = [mid1_vect, relu_vect, output_vect]
        positions = [
            arrows[0].get_right() + 0.5 * RIGHT,
            arrows[1].get_right() + 0.5 * RIGHT,
            arrows[2].get_right() + 0.5 * RIGHT,
        ]
        for vect, pos in zip(vects, positions):
            vect.move_to(pos)

        # Show input
        self.play(FadeIn(input_vect, shift=LEFT))
        self.wait()

        # Show first linear arrow
        self.play(
            GrowArrow(arrows[0]),
            FadeIn(labels[0])
        )

        # Animate transformation to mid1
        self.play(
            TransformFromCopy(input_vect, mid1_vect, run_time=1.5)
        )
        self.wait()

        # Show ReLU arrow
        self.play(
            GrowArrow(arrows[1]),
            FadeIn(labels[1])
        )

        # Show negative values being zeroed
        neg_highlights = VGroup()
        for i, val in enumerate(mid1_values):
            if val < 0:
                rect = SurroundingRectangle(mid1_vect[i], buff=0.05)
                rect.set_stroke(RED, 2)
                neg_highlights.add(rect)

        self.play(ShowCreation(neg_highlights, lag_ratio=0.2))
        self.wait(0.5)

        # Transform to ReLU output
        self.play(
            TransformFromCopy(mid1_vect, relu_vect),
            FadeOut(neg_highlights),
            run_time=1.5
        )
        self.wait()

        # Show second linear arrow
        self.play(
            GrowArrow(arrows[2]),
            FadeIn(labels[2])
        )

        # Final transformation
        self.play(
            TransformFromCopy(relu_vect, output_vect, run_time=1.5)
        )
        self.wait(2)

    def create_vector(self, values, color=None, zero_color=GREY):
        """Creates a vertical vector display with colored entries."""
        entries = VGroup()
        for val in values:
            entry = DecimalNumber(
                val,
                num_decimal_places=1,
                include_sign=True,
                font_size=24
            )
            if color is not None:
                entry.set_color(color)
            elif val == 0:
                entry.set_color(zero_color)
            else:
                entry.set_color(value_to_color(val, max_value=3))
            entries.add(entry)

        entries.arrange(DOWN, buff=0.15)

        # Add brackets
        left_b = Tex("[").stretch_to_fit_height(entries.get_height() * 1.1)
        right_b = Tex("]").stretch_to_fit_height(entries.get_height() * 1.1)
        left_b.next_to(entries, LEFT, buff=0.05)
        right_b.next_to(entries, RIGHT, buff=0.05)

        return VGroup(*entries, left_b, right_b)


class MLPBlockDiagram(InteractiveScene):
    """
    Shows a high-level block diagram of an MLP.
    Input -> [Up Projection] -> [Nonlinearity] -> [Down Projection] -> Output

    Demonstrates: Block diagram style, text labels, arrows
    """

    def construct(self):
        # Title
        title = Text("MLP Block Structure", font_size=48)
        title.to_edge(UP)

        # Create blocks
        def create_block(text, color, width=2.5, height=1.5):
            rect = Rectangle(width=width, height=height)
            rect.set_fill(color, 0.3)
            rect.set_stroke(color, 2)
            label = Text(text, font_size=24)
            label.move_to(rect)
            return VGroup(rect, label)

        up_proj = create_block("Up\nProjection", BLUE)
        nonlin = create_block("ReLU", YELLOW, width=1.5)
        down_proj = create_block("Down\nProjection", GREEN)

        # Arrange blocks
        blocks = VGroup(up_proj, nonlin, down_proj)
        blocks.arrange(RIGHT, buff=1.0)

        # Arrows between blocks
        arrow1 = Arrow(up_proj.get_right(), nonlin.get_left(), buff=0.1)
        arrow2 = Arrow(nonlin.get_right(), down_proj.get_left(), buff=0.1)

        # Input/Output arrows
        input_arrow = Arrow(up_proj.get_left() + LEFT, up_proj.get_left(), buff=0.1)
        output_arrow = Arrow(down_proj.get_right(), down_proj.get_right() + RIGHT, buff=0.1)

        # Input/Output labels
        input_label = Tex(R"\vec{E}", font_size=36)
        input_label.next_to(input_arrow, LEFT)
        output_label = Tex(R"\vec{E}'", font_size=36)
        output_label.next_to(output_arrow, RIGHT)

        # Dimension labels
        dim_in = Text("d", font_size=20, color=GREY)
        dim_mid = Text("4d", font_size=20, color=GREY)
        dim_out = Text("d", font_size=20, color=GREY)

        dim_in.next_to(input_arrow, DOWN, buff=0.1)
        dim_mid.next_to(arrow1, DOWN, buff=0.1)
        dim_out.next_to(output_arrow, DOWN, buff=0.1)

        # Build the scene
        self.play(Write(title))
        self.play(
            FadeIn(input_label),
            GrowArrow(input_arrow)
        )
        self.play(FadeIn(up_proj, shift=RIGHT))
        self.play(
            GrowArrow(arrow1),
            FadeIn(dim_in)
        )
        self.play(FadeIn(nonlin, shift=RIGHT))
        self.play(
            GrowArrow(arrow2),
            FadeIn(dim_mid)
        )
        self.play(FadeIn(down_proj, shift=RIGHT))
        self.play(
            GrowArrow(output_arrow),
            FadeIn(output_label),
            FadeIn(dim_out)
        )
        self.wait()

        # Show data flow animation
        data_dot = Dot(radius=0.1, color=ORANGE)
        data_dot.move_to(input_arrow.get_start())

        path = VMobject()
        path.set_points_as_corners([
            input_arrow.get_start(),
            input_arrow.get_end(),
            up_proj.get_center(),
            arrow1.get_start(),
            arrow1.get_end(),
            nonlin.get_center(),
            arrow2.get_start(),
            arrow2.get_end(),
            down_proj.get_center(),
            output_arrow.get_start(),
            output_arrow.get_end(),
        ])

        self.play(
            MoveAlongPath(data_dot, path, run_time=4),
        )
        self.wait()

        # Highlight the residual connection concept
        residual_label = Text(
            "Output = Input + MLP(Input)",
            font_size=28
        )
        residual_label.next_to(blocks, DOWN, buff=1.0)

        plus_sign = Tex("+", font_size=48)
        plus_sign.next_to(down_proj, RIGHT, buff=0.5)

        skip_arrow = CurvedArrow(
            input_arrow.get_end() + 0.2 * UP,
            plus_sign.get_left() + 0.1 * LEFT,
            angle=-TAU/4
        )
        skip_arrow.set_color(PINK)

        self.play(
            FadeIn(residual_label),
            ShowCreation(skip_arrow),
            Write(plus_sign)
        )
        self.wait(2)
