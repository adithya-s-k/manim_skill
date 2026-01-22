"""
Word Vector Analogy Visualization
Demonstrates the famous king - man + woman = queen analogy in embedding space.

Based on: videos/_2024/transformers/embedding.py - KingQueenExample
"""
from manimlib import *


class WordVectorAnalogy(InteractiveScene):
    """
    Visualizes word vector arithmetic in 3D space.
    Shows how semantic relationships are encoded as directions.
    """

    def construct(self):
        # Set up 3D scene
        frame = self.frame
        frame.reorient(-20, 70, 0)
        frame.add_ambient_rotation(2 * DEGREES)

        # Create axes
        axes = ThreeDAxes(
            x_range=(-4, 4, 1),
            y_range=(-4, 4, 1),
            z_range=(-3, 3, 1),
            width=8,
            height=8,
            depth=6,
        )
        axes.set_stroke(width=2)
        self.add(axes)

        # Add plane for reference
        plane = NumberPlane(
            axes.x_range[:2], axes.y_range[:2],
            width=axes.get_width(),
            height=axes.get_height(),
            background_line_style=dict(
                stroke_color=GREY,
                stroke_width=1,
            ),
            faded_line_style=dict(
                stroke_opacity=0.25,
                stroke_width=0.5,
            ),
            faded_line_ratio=1,
        )
        plane.rotate(90 * DEGREES, LEFT)
        self.add(plane)

        # Define word positions (simplified for demo)
        word_data = {
            "man": {"pos": np.array([1, -1, 0.5]), "color": BLUE_B},
            "woman": {"pos": np.array([1, 1, 0.5]), "color": RED_B},
            "king": {"pos": np.array([-2, -1, 1.5]), "color": BLUE_D},
            "queen": {"pos": np.array([-2, 1, 1.5]), "color": RED_D},
        }

        def create_labeled_arrow(word, pos, color):
            """Create an arrow with a word label."""
            arrow = Arrow(
                axes.get_origin(),
                axes.c2p(*pos),
                buff=0,
                stroke_color=color,
                stroke_width=4,
            )
            arrow.set_flat_stroke(False)
            label = Text(word, font_size=30)
            label.set_backstroke(BLACK, 3)
            label.next_to(arrow.get_end(), normalize(arrow.get_vector()), buff=0.1)
            label.rotate(90 * DEGREES, RIGHT)  # Orient for 3D
            return arrow, label

        # Create all word vectors
        vectors = {}
        labels = {}
        for word, data in word_data.items():
            arrow, label = create_labeled_arrow(word, data["pos"], data["color"])
            vectors[word] = arrow
            labels[word] = label

        # Show equation (fixed in frame)
        equation = Tex(
            R"\text{woman} - \text{man} \approx \text{queen} - \text{king}",
            font_size=42
        )
        equation.fix_in_frame()
        equation.to_corner(UR)
        equation["woman"].set_color(RED_B)
        equation["man"].set_color(BLUE_B)
        equation["queen"].set_color(RED_D)
        equation["king"].set_color(BLUE_D)

        top_rect = FullScreenFadeRectangle().set_fill(BLACK, 0.7)
        top_rect.set_height(1.2, about_edge=UP, stretch=True)
        top_rect.fix_in_frame()

        # Animate man and woman vectors
        self.play(
            GrowArrow(vectors["man"]),
            FadeIn(labels["man"]),
            GrowArrow(vectors["woman"]),
            FadeIn(labels["woman"]),
            run_time=2
        )
        self.wait()

        # Show difference vector (man -> woman)
        diff = Arrow(
            vectors["man"].get_end(),
            vectors["woman"].get_end(),
            buff=0,
            stroke_color=YELLOW,
            stroke_width=4,
        )
        diff.set_flat_stroke(False)

        self.play(GrowArrow(diff))
        self.wait()

        # Show equation
        self.add(top_rect)
        self.play(Write(equation))
        self.wait()

        # Add king and queen
        self.play(
            GrowArrow(vectors["king"]),
            FadeIn(labels["king"]),
            run_time=1.5
        )

        # Show the same difference applied to king
        king_to_queen = diff.copy()
        king_to_queen.shift(vectors["king"].get_end() - vectors["man"].get_end())

        self.play(TransformFromCopy(diff, king_to_queen))
        self.wait()

        # Show queen at the tip
        self.play(
            GrowArrow(vectors["queen"]),
            FadeIn(labels["queen"]),
        )
        self.wait()

        # Rotate to show the relationship
        frame.clear_updaters()
        self.play(
            frame.animate.reorient(-100, 20, 100),
            run_time=4
        )
        frame.add_ambient_rotation(2 * DEGREES)

        # Flash the gender direction
        gender_dir = diff.get_vector()
        lines = Line(ORIGIN, 1.5 * normalize(gender_dir)).replicate(100)
        lines.insert_n_curves(20)
        lines.set_stroke(YELLOW, 3)
        for line in lines:
            line.move_to(np.random.uniform(-2, 2, 3))

        self.play(
            LaggedStartMap(
                VShowPassingFlash, lines,
                lag_ratio=1 / len(lines),
                run_time=3
            )
        )

        # Add direction label
        dir_label = Text("Gender direction", font_size=36, color=YELLOW)
        dir_label.fix_in_frame()
        dir_label.next_to(equation, DOWN, buff=0.5)

        self.play(Write(dir_label))
        self.wait(3)

        # Show another example
        new_eq = Tex(
            R"\text{uncle} - \text{aunt} \approx \text{man} - \text{woman}",
            font_size=36
        )
        new_eq.fix_in_frame()
        new_eq.next_to(dir_label, DOWN, buff=0.3)

        self.play(Write(new_eq))
        self.wait(5)
