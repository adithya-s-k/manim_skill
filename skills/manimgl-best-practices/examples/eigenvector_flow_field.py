"""
Eigenvector Flow Field
======================
Visualizes the flow of a linear dynamical system dx/dt = Ax.
The eigenvectors appear as special directions where flow stays on a line.

This demonstrates:
- VectorField for showing derivative directions
- StreamLines for animated flow
- Computing eigenvalues/eigenvectors with numpy
- Linear algebra visualization
"""

from manimlib import *


class EigenvectorFlowField(Scene):
    """
    Shows the vector field for a linear ODE system dx/dt = Ax.
    The eigenvectors are the special directions where trajectories
    move straight outward or inward.
    """

    def construct(self):
        # Define the matrix for our linear system
        mat = np.array([[1, 2], [3, 1]])

        # Create coordinate plane
        plane = NumberPlane((-4, 4), (-4, 4), faded_line_ratio=1)
        plane.set_height(FRAME_HEIGHT)
        plane.background_lines.set_stroke(BLUE, 1)
        plane.faded_lines.set_stroke(BLUE, 0.5, 0.5)
        plane.add_coordinate_labels(font_size=36)

        self.add(plane)

        # Define the derivative function for the linear system
        def deriv_func(x, y):
            """Returns the derivative at a point: f(v) = Av"""
            v = np.array([x, y])
            result = 0.5 * np.dot(mat, v)
            return result[0], result[1]

        # Create vector field manually using arrows
        vector_field = VGroup()
        for x in np.linspace(-3.5, 3.5, 12):
            for y in np.linspace(-3.5, 3.5, 12):
                if abs(x) < 0.4 and abs(y) < 0.4:
                    continue  # Skip origin area
                dx, dy = deriv_func(x, y)
                start = plane.c2p(x, y)
                direction = np.array([dx, dy, 0])
                norm = np.linalg.norm(direction)
                if norm > 0.1:
                    # Normalize and scale for visibility
                    direction = direction / norm * min(0.5, norm * 0.3)
                    end = start + direction
                    arrow = Arrow(
                        start, end, buff=0,
                        stroke_width=2,
                        max_tip_length_to_length_ratio=0.3
                    )
                    # Color based on magnitude
                    alpha = min(1, norm / 3)
                    arrow.set_color(interpolate_color(BLUE, RED, alpha))
                    vector_field.add(arrow)

        # Show vector field
        self.play(
            LaggedStartMap(GrowArrow, vector_field, lag_ratio=0.01),
            run_time=2
        )
        self.wait(2)

        # Calculate eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(mat)

        # Create eigenvalue lines (extended versions of eigenvectors)
        eigenlines = VGroup()
        eigen_labels = VGroup()

        for i, (ev, eigval) in enumerate(zip(eigenvectors.T, eigenvalues)):
            # Create the line
            line = Line(-ev, ev)
            line.set_length(15)
            color = [TEAL, YELLOW][i]
            line.set_stroke(color, 5)
            eigenlines.add(line)

            # Create label
            label = Tex(
                R"\lambda_" + str(i + 1) + f" = {eigval:.2f}",
                font_size=30
            )
            label.set_color(color)
            label.set_backstroke(width=5)
            # Position label at end of eigenvector
            label.next_to(plane.c2p(*(ev * 2)), RIGHT if ev[0] > 0 else LEFT)
            eigen_labels.add(label)

        # Show eigenvector lines with labels
        self.play(
            LaggedStartMap(ShowCreation, eigenlines, lag_ratio=0.3),
            run_time=2
        )
        self.play(LaggedStartMap(FadeIn, eigen_labels, lag_ratio=0.3))

        # Let it run for a while to see the flow
        self.wait(8)


class LinearSystemPhasePortrait(Scene):
    """
    Shows different types of equilibria based on eigenvalues:
    - Both positive: unstable node (expanding)
    - Both negative: stable node (contracting)
    - Mixed signs: saddle point
    """

    def construct(self):
        # Create three small phase portraits
        matrices = [
            np.array([[2, 0], [0, 1]]),    # Unstable node (both positive)
            np.array([[-2, 0], [0, -1]]),  # Stable node (both negative)
            np.array([[2, 0], [0, -1]]),   # Saddle point (mixed)
        ]
        titles = [
            "Unstable Node",
            "Stable Node",
            "Saddle Point",
        ]
        subtitle_data = [
            (r"\lambda_1 > 0, \lambda_2 > 0", GREEN),
            (r"\lambda_1 < 0, \lambda_2 < 0", RED),
            (r"\lambda_1 > 0, \lambda_2 < 0", YELLOW),
        ]

        portraits = VGroup()
        for mat, title, (subtitle, color) in zip(matrices, titles, subtitle_data):
            portrait = self.create_phase_portrait(mat)
            label = Text(title, font_size=24)
            label.next_to(portrait, UP)

            eigen_label = Tex(subtitle, font_size=20)
            eigen_label.set_color(color)
            eigen_label.next_to(portrait, DOWN)

            group = VGroup(portrait, label, eigen_label)
            portraits.add(group)

        portraits.arrange(RIGHT, buff=0.5)
        portraits.set_width(FRAME_WIDTH - 1)

        main_title = Text("Phase Portraits by Eigenvalue Type", font_size=36)
        main_title.to_edge(UP)

        self.add(main_title)
        self.play(LaggedStartMap(FadeIn, portraits, lag_ratio=0.3))
        self.wait(3)

    def create_phase_portrait(self, mat):
        """Create a small phase portrait for a given matrix."""
        plane = NumberPlane(
            (-2, 2), (-2, 2),
            background_line_style={"stroke_width": 1, "stroke_opacity": 0.5}
        )
        plane.set_height(3)

        def func(point):
            v = np.array([point[0], point[1]])
            result = mat @ v
            return np.array([result[0], result[1], 0]) * 0.3

        # Just show arrows, no animation for static display
        arrows = VGroup()
        for x in np.linspace(-1.5, 1.5, 5):
            for y in np.linspace(-1.5, 1.5, 5):
                if abs(x) < 0.3 and abs(y) < 0.3:
                    continue
                start = plane.c2p(x, y)
                deriv = func(np.array([x, y, 0]))
                if np.linalg.norm(deriv) > 0.1:
                    deriv = deriv / np.linalg.norm(deriv) * 0.3
                end = start + deriv
                arrow = Arrow(start, end, buff=0, stroke_width=2, max_tip_length_to_length_ratio=0.3)
                arrow.set_color(interpolate_color(BLUE, RED, (np.linalg.norm(deriv) / 0.5)))
                arrows.add(arrow)

        return VGroup(plane, arrows)
