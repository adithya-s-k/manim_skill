"""
3D Vector Space Example
Demonstrates how coordinates create a point in 3D space with animated construction.

Based on: videos/_2024/transformers/embedding.py - ThreeDSpaceExample
"""
from manimlib import *


class ThreeDVectorSpace(InteractiveScene):
    """
    Visualizes how 3D coordinates define a point in space.
    Shows step-by-step construction along x, y, z axes.
    """

    def construct(self):
        # Set up 3D frame and axes
        frame = self.frame
        frame.reorient(-15, 78, 0, (1.07, 1.71, 1.41), 6.72)
        frame.add_ambient_rotation(1 * DEGREES)

        axes = ThreeDAxes((-5, 5), (-5, 5), (-4, 4))
        plane = NumberPlane((-5, 5), (-5, 5))
        plane.set_stroke(opacity=0.5)

        self.add(plane)
        self.add(axes)

        # Target coordinates
        x, y, z = coordinates = np.array([3, 1, 2])
        colors = [RED, GREEN, BLUE]

        # Create coordinate display (fixed in frame)
        coords = DecimalMatrix(np.zeros((3, 1)), num_decimal_places=1)
        coords.fix_in_frame()
        coords.to_corner(UR)
        coords.shift(1.5 * LEFT)
        coords.get_entries().set_submobject_colors_by_gradient(*colors)

        # Create path lines for x, y, z components
        lines = VGroup(
            Line(axes.c2p(0, 0, 0), axes.c2p(x, 0, 0)),
            Line(axes.c2p(x, 0, 0), axes.c2p(x, y, 0)),
            Line(axes.c2p(x, y, 0), axes.c2p(x, y, z)),
        )
        lines.set_flat_stroke(False)
        lines.set_submobject_colors_by_gradient(*colors)

        # Create axis labels
        labels = VGroup(*map(Tex, "xyz"))
        labels.rotate(89 * DEGREES, RIGHT)
        directions = [OUT, OUT + RIGHT, RIGHT]
        for label, line, direction in zip(labels, lines, directions):
            label.next_to(line, direction, buff=SMALL_BUFF)
            label.match_color(line)

        # Glowing dot to track position
        dot = GlowDot(color=WHITE)
        dot.move_to(axes.get_origin())

        # Final vector arrow
        vect = Arrow(axes.get_origin(), axes.c2p(x, y, z), buff=0)
        vect.set_flat_stroke(False)

        # Show coordinate matrix
        self.add(coords)

        # Animate building the vector step by step
        for entry, line, label, value in zip(coords.get_entries(), lines, labels, coordinates):
            rect = SurroundingRectangle(entry)
            rect.set_fill(line.get_color(), opacity=0.3)
            rect.set_stroke(line.get_color(), width=2, opacity=1.0)
            self.play(
                ShowCreation(line),
                FadeInFromPoint(label, line.get_start()),
                FadeIn(rect, rate_func=there_and_back),
                ChangeDecimalToValue(entry, value),
                dot.animate.move_to(line.get_end()),
            )
            self.wait(0.5)

        # Show the complete vector
        self.play(ShowCreation(vect))
        self.wait(3)

        # Show many random points
        points = GlowDots(np.random.uniform(-3, 3, size=(50, 3)), radius=0.1)
        frame.clear_updaters()
        self.play(
            FadeOut(coords),
            FadeOut(dot),
            FadeOut(plane),
            LaggedStartMap(FadeOut, VGroup(*lines, vect, *labels)),
            frame.animate.reorient(-81, 61, 0, (-0.82, 0.6, 0.36), 8.95),
            ShowCreation(points),
            run_time=2,
        )
        frame.add_ambient_rotation(5 * DEGREES)
        self.wait(5)
