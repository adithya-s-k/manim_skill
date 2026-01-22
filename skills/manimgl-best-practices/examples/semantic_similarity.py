"""
Semantic Similarity Visualization
Shows how similar words cluster together in embedding space.

Based on: videos/_2024/transformers/embedding.py - ShowNearestNeighbors
"""
from manimlib import *


class SemanticSimilarity(InteractiveScene):
    """
    Demonstrates semantic clustering in word embedding space.
    Similar words are shown as nearby vectors.
    """

    def construct(self):
        # Set up 3D scene
        frame = self.frame
        frame.reorient(-21, 87, 0, (2.18, 0.09, 0.72), 4)
        frame.add_ambient_rotation(1 * DEGREES)

        # Create axes
        axes = ThreeDAxes(
            x_range=(-5, 5, 1),
            y_range=(-5, 5, 1),
            z_range=(-4, 4, 1),
            width=8,
            height=8,
            depth=6.4,
        )
        axes.set_stroke(width=2)
        self.add(axes)

        # Add reference plane
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
        self.add(plane)

        # Seed word and its neighbors
        seed_word = "tower"
        seed_color = YELLOW
        neighbor_words = [
            "castle", "fortress", "building", "spire",
            "monument", "cathedral", "skyscraper"
        ]

        # Create seed vector
        seed_pos = np.array([2, 0, 1])

        def create_word_arrow(word, pos, color):
            arrow = Arrow(
                axes.get_origin(),
                axes.c2p(*pos),
                buff=0,
                stroke_color=color,
                stroke_width=4,
            )
            arrow.set_flat_stroke(False)
            label = Text(word, font_size=24)
            label.set_backstroke(BLACK, 3)
            label.next_to(arrow.get_end(), normalize(arrow.get_vector()), buff=0.05)
            # Keep label visible by fixing in frame
            label.fix_in_frame()
            return VGroup(arrow, label)

        seed_vect = create_word_arrow(seed_word, seed_pos, seed_color)
        self.add(seed_vect)

        # Create title (fixed in frame)
        title = Text(f"Words similar to '{seed_word}'", font_size=42)
        title.fix_in_frame()
        title.to_corner(UR)
        underline = Underline(title)
        underline.fix_in_frame()

        self.add(title, underline)

        # Create neighbor positions (clustered around seed)
        np.random.seed(42)
        neighbor_positions = [
            seed_pos + np.random.uniform(-0.8, 0.8, 3)
            for _ in neighbor_words
        ]

        # Create list display
        items = VGroup(*(
            Text(f"  {word}", font_size=30)
            for word in neighbor_words
        ))
        items.arrange(DOWN, aligned_edge=LEFT)
        items.next_to(underline, DOWN, buff=0.5)
        items.align_to(title, LEFT)
        items.fix_in_frame()

        # Animate neighbors appearing
        neighbors = []
        last_neighbor = VectorizedPoint()
        for i, (word, pos, item) in enumerate(zip(neighbor_words, neighbor_positions, items)):
            # Create slightly different colors for variety
            hue = 0.55 + 0.1 * np.random.random()
            color = Color(hsl=(hue, 0.6, 0.5))

            neighbor = create_word_arrow(word, pos, color)
            neighbors.append(neighbor)

            # Fade previous neighbor
            faded_neighbor = last_neighbor.copy()
            faded_neighbor.set_opacity(0.3)

            self.add(faded_neighbor, seed_vect, neighbor)
            self.play(
                FadeIn(item),
                FadeIn(neighbor),
                FadeOut(last_neighbor),
                FadeIn(faded_neighbor),
                run_time=0.5
            )
            last_neighbor = neighbor
            self.wait(0.3)

        # Fade last neighbor
        self.play(last_neighbor.animate.set_opacity(0.3))
        self.wait(2)

        # Show all neighbors together
        all_neighbors = VGroup(*neighbors)
        self.play(all_neighbors.animate.set_opacity(1))
        self.wait()

        # Draw circle to show clustering
        cluster_center = axes.c2p(*seed_pos)
        cluster_circle = Circle(radius=1.2)
        cluster_circle.move_to(cluster_center)
        cluster_circle.set_stroke(YELLOW, 2)
        cluster_circle.set_fill(YELLOW, 0.1)

        self.play(ShowCreation(cluster_circle))
        self.wait()

        # Add clustering label
        cluster_label = Text("Semantic cluster", font_size=36, color=YELLOW)
        cluster_label.fix_in_frame()
        cluster_label.next_to(items, DOWN, buff=1.0)

        self.play(Write(cluster_label))
        self.wait(3)

        # Show contrasting words far away
        contrast_words = ["banana", "running", "purple"]
        contrast_positions = [
            np.array([-3, -2, -1]),
            np.array([-2, 3, 0]),
            np.array([0, -3, 2]),
        ]

        contrast_label = Text("Unrelated words", font_size=30, color=RED)
        contrast_label.fix_in_frame()
        contrast_label.next_to(cluster_label, DOWN, buff=0.3)

        contrast_vects = VGroup()
        for word, pos in zip(contrast_words, contrast_positions):
            vect = create_word_arrow(word, pos, RED)
            vect.set_opacity(0.6)
            contrast_vects.add(vect)

        self.play(
            LaggedStartMap(FadeIn, contrast_vects, lag_ratio=0.3),
            Write(contrast_label),
            run_time=2
        )
        self.wait(3)

        # Rotate scene to show 3D structure
        frame.clear_updaters()
        self.play(
            frame.animate.reorient(-100, 60, 100, (0, 0, 0), 6),
            run_time=5
        )
        self.wait(2)
