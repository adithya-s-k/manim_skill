"""
Vector Space and Dot Products for MLPs
Shows how dot products can be used to detect features in embeddings.
"""
from manimlib import *
import numpy as np


class VectorDotProduct(InteractiveScene):
    """
    Visualizes how the dot product between a feature direction
    and an embedding determines neuron activation.

    Demonstrates: NumberPlane, vectors, dot product projection
    """

    def construct(self):
        # Create 2D plane for visualization
        unit_size = 2.0
        plane = NumberPlane(
            x_range=(-3, 3),
            y_range=(-3, 3),
            axis_config=dict(stroke_width=1),
            background_line_style=dict(
                stroke_color=BLUE_D,
                stroke_width=1,
                stroke_opacity=0.5
            ),
            faded_line_ratio=1,
            unit_size=unit_size,
        )
        plane.shift(DOWN * 0.5)

        # Title
        title = Text("Dot Product as Feature Detection", font_size=36)
        title.to_edge(UP)

        self.play(Write(title))
        self.play(FadeIn(plane))

        # Feature direction vector (represents what the neuron is looking for)
        feature_angle = 60 * DEGREES
        feature_vect = Vector(
            unit_size * np.array([np.cos(feature_angle), np.sin(feature_angle), 0])
        )
        feature_vect.set_color(RED)
        feature_vect.shift(plane.get_origin())

        feature_label = Text("Feature\nDirection", font_size=20)
        feature_label.set_color(RED)
        feature_label.next_to(feature_vect.get_end(), UR, buff=0.1)

        self.play(
            GrowArrow(feature_vect),
            FadeIn(feature_label)
        )
        self.wait()

        # Embedding vector (the input we're testing)
        emb_vect = Vector(unit_size * 1.5 * RIGHT)
        emb_vect.set_color(YELLOW)
        emb_vect.shift(plane.get_origin())

        emb_label = Tex(R"\vec{E}", font_size=36)
        emb_label.set_color(YELLOW)
        emb_label.next_to(emb_vect.get_end(), DR, buff=0.1)

        self.play(
            GrowArrow(emb_vect),
            FadeIn(emb_label)
        )
        self.wait()

        # Show the projection (dot product visualization)
        feature_unit = normalize(feature_vect.get_vector())

        def get_projection_point():
            emb_vec = emb_vect.get_end() - plane.get_origin()
            proj_length = np.dot(emb_vec, feature_unit)
            return plane.get_origin() + proj_length * feature_unit

        proj_line = Line(plane.get_origin(), get_projection_point())
        proj_line.set_stroke(PINK, 4)

        dashed_line = DashedLine(emb_vect.get_end(), get_projection_point())
        dashed_line.set_stroke(GREY, 2)

        proj_dot = Dot(get_projection_point(), radius=0.1)
        proj_dot.set_color(PINK)

        self.play(
            ShowCreation(proj_line),
            ShowCreation(dashed_line),
            GrowFromCenter(proj_dot)
        )

        # Dot product value
        dp_value = DecimalNumber(
            np.dot(emb_vect.get_end() - plane.get_origin(), feature_unit) / unit_size,
            num_decimal_places=2,
            font_size=30
        )
        dp_value.set_color(PINK)
        dp_label = Text("Dot Product: ", font_size=24)
        dp_display = VGroup(dp_label, dp_value).arrange(RIGHT)
        dp_display.next_to(proj_dot, RIGHT, buff=0.3)

        self.play(FadeIn(dp_display))
        self.wait()

        # Animate the embedding vector rotating
        original_angle = 0

        def update_emb_vect(mob, angle):
            new_end = plane.get_origin() + unit_size * 1.5 * np.array([
                np.cos(angle), np.sin(angle), 0
            ])
            mob.put_start_and_end_on(plane.get_origin(), new_end)
            emb_label.next_to(new_end, normalize(new_end - plane.get_origin()), buff=0.1)

        def update_projection():
            proj_pt = get_projection_point()
            proj_line.put_start_and_end_on(plane.get_origin(), proj_pt)
            dashed_line.put_start_and_end_on(emb_vect.get_end(), proj_pt)
            proj_dot.move_to(proj_pt)
            dp_val = np.dot(emb_vect.get_end() - plane.get_origin(), feature_unit) / unit_size
            dp_value.set_value(dp_val)
            dp_display.next_to(proj_dot, RIGHT, buff=0.3)

        # Rotate through different angles
        for target_angle in [45 * DEGREES, 90 * DEGREES, 150 * DEGREES, 220 * DEGREES, 300 * DEGREES, 0]:
            self.play(
                Rotate(
                    emb_vect,
                    target_angle - original_angle,
                    about_point=plane.get_origin()
                ),
                UpdateFromFunc(proj_line, lambda m: update_projection()),
                run_time=1.5
            )
            update_projection()
            original_angle = target_angle
            self.wait(0.5)

        self.wait()


class FeatureDirectionThreshold(InteractiveScene):
    """
    Shows how a threshold on the dot product creates a decision boundary.
    Positive side = "Yes", Negative side = "No".

    Demonstrates: Regions, decision boundaries, classification
    """

    def construct(self):
        # Create plane
        unit_size = 2.0
        plane = NumberPlane(
            x_range=(-3, 3),
            y_range=(-3, 3),
            axis_config=dict(stroke_width=1),
            background_line_style=dict(
                stroke_color=BLUE_D,
                stroke_width=1,
                stroke_opacity=0.5
            ),
            faded_line_ratio=1,
            unit_size=unit_size,
        )

        # Title
        title = Text("Decision Boundary from Dot Product", font_size=32)
        title.to_edge(UP)

        self.play(Write(title))
        self.play(FadeIn(plane))

        # Feature direction
        feature_angle = 45 * DEGREES
        feature_dir = np.array([np.cos(feature_angle), np.sin(feature_angle), 0])
        feature_vect = Vector(unit_size * feature_dir)
        feature_vect.set_color(WHITE)

        # Decision boundary (perpendicular to feature direction)
        perp_dir = np.array([-feature_dir[1], feature_dir[0], 0])
        boundary_line = Line(
            -4 * perp_dir * unit_size,
            4 * perp_dir * unit_size
        )
        boundary_line.set_stroke(WHITE, 3)

        self.play(GrowArrow(feature_vect))
        self.play(ShowCreation(boundary_line))

        # Create "Yes" and "No" regions
        yes_region = Rectangle(width=8, height=8)
        yes_region.set_fill(GREEN, 0.2)
        yes_region.set_stroke(width=0)
        yes_region.rotate(feature_angle)
        yes_region.shift(2 * feature_dir * unit_size)

        no_region = Rectangle(width=8, height=8)
        no_region.set_fill(RED, 0.15)
        no_region.set_stroke(width=0)
        no_region.rotate(feature_angle)
        no_region.shift(-2 * feature_dir * unit_size)

        # Clip regions to visible area
        yes_region.set_clip_path(Rectangle(width=12, height=8))
        no_region.set_clip_path(Rectangle(width=12, height=8))

        self.play(
            FadeIn(yes_region),
            FadeIn(no_region)
        )

        # Labels
        yes_label = Text("Yes", font_size=36, color=GREEN)
        yes_label.move_to(2.5 * feature_dir * unit_size)

        no_label = Text("No", font_size=36, color=RED)
        no_label.move_to(-2.5 * feature_dir * unit_size)

        self.play(
            FadeIn(yes_label),
            FadeIn(no_label)
        )
        self.wait()

        # Show example points
        points_data = [
            (1.5 * unit_size, 1.8 * unit_size, "Match", GREEN),
            (-0.5 * unit_size, -1.0 * unit_size, "No Match", RED),
            (2.0 * unit_size, 0.5 * unit_size, "Match", GREEN),
            (-1.5 * unit_size, 0.2 * unit_size, "No Match", RED),
        ]

        dots = VGroup()
        for x, y, label_text, color in points_data:
            dot = Dot(point=np.array([x, y, 0]), radius=0.15)
            dot.set_color(color)
            dots.add(dot)

        self.play(
            LaggedStartMap(GrowFromCenter, dots, lag_ratio=0.3)
        )
        self.wait(2)

        # Show threshold adjustment
        threshold_label = Text("Threshold can be adjusted with bias", font_size=24)
        threshold_label.next_to(title, DOWN)

        self.play(Write(threshold_label))

        # Move boundary line (simulating bias adjustment)
        for offset in [0.5, -0.5, 0]:
            new_line = Line(
                -4 * perp_dir * unit_size + offset * feature_dir * unit_size,
                4 * perp_dir * unit_size + offset * feature_dir * unit_size
            )
            new_line.set_stroke(WHITE, 3)
            self.play(Transform(boundary_line, new_line))
            self.wait(0.5)

        self.wait(2)
