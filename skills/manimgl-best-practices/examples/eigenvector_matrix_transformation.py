"""
Eigenvector Matrix Transformation
=================================
Demonstrates how a matrix transformation looks in standard basis vs eigenbasis.
In the eigenbasis, the transformation becomes a simple scaling along each axis.

Key concepts demonstrated:
- Matrix transformation of a number plane
- Eigenvector computation with numpy
- Change of basis visualization
- Updated vectors that follow coordinate system changes
"""

from manimlib import *


class EigenvectorMatrixTransformation(Scene):
    """
    Shows a matrix transformation in two perspectives:
    1. Standard basis (i-hat, j-hat) - complex shearing transformation
    2. Eigenbasis - simple scaling along eigenvector directions
    """

    def construct(self):
        # Define the transformation matrix
        # This matrix has eigenvalues -1 and 3
        mat = np.array([[1, 2], [3, 1]])

        # Create ghost plane to show original grid
        ghost_plane = NumberPlane(faded_line_ratio=0)
        ghost_plane.set_stroke(GREY, 1)

        # Create main plane that will be transformed
        plane = self.get_plane()

        # Create basis vectors that update with the plane
        basis = VGroup(
            self.get_updated_vector((1, 0), plane, GREEN),
            self.get_updated_vector((0, 1), plane, RED),
        )

        # Add label
        title = Text("Standard Basis Transformation", font_size=36)
        title.to_corner(UL)
        title.set_backstroke(width=5)

        self.add(ghost_plane, plane, basis, title)

        # Animate the transformation in standard basis
        self.play(
            plane.animate.apply_matrix(mat),
            run_time=4
        )
        self.wait()

        # Fade out standard basis view
        self.play(FadeOut(VGroup(ghost_plane, plane, basis, title)))

        # Now show the same transformation in eigenbasis
        # Calculate eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(mat)

        # Create a plane already in the eigenbasis
        eigenplane = self.get_plane()
        eigenplane.apply_matrix(eigenvectors, about_point=ORIGIN)

        # Create eigenbasis vectors
        eigenbasis = VGroup(
            self.get_updated_vector((1, 0), eigenplane, TEAL),
            self.get_updated_vector((0, 1), eigenplane, YELLOW),
        )

        # Add new title
        eigen_title = Text("Eigenbasis Transformation", font_size=36)
        eigen_title.to_corner(UL)
        eigen_title.set_backstroke(width=5)

        # Show eigenvalue labels
        eigen_labels = VGroup(
            Tex(R"\lambda_1 = " + f"{eigenvalues[0]:.1f}", font_size=30).set_color(TEAL),
            Tex(R"\lambda_2 = " + f"{eigenvalues[1]:.1f}", font_size=30).set_color(YELLOW),
        )
        eigen_labels.arrange(DOWN, aligned_edge=LEFT)
        eigen_labels.to_corner(UR)
        eigen_labels.set_backstroke(width=5)

        self.add(eigenplane, eigenbasis, eigen_title, eigen_labels)

        # In eigenbasis, transformation is just scaling by eigenvalues!
        self.play(
            eigenplane.animate.apply_matrix(mat),
            run_time=4
        )
        self.wait()

    def get_plane(self, x_range=(-16, 16), y_range=(-8, 8)):
        """Create a number plane for visualization."""
        return NumberPlane(x_range, y_range, faded_line_ratio=1)

    def get_updated_vector(self, coords, coord_system, color=YELLOW, thickness=4, **kwargs):
        """
        Create a vector that automatically updates its position based on
        the coordinate system it's attached to. This is useful for showing
        how basis vectors transform with the plane.
        """
        vect = Vector(RIGHT, fill_color=color, thickness=thickness, **kwargs)
        vect.add_updater(lambda m: m.put_start_and_end_on(
            coord_system.get_origin(),
            coord_system.c2p(*coords),
        ))
        return vect


class EigenvectorScaling(Scene):
    """
    Shows that eigenvectors only get scaled by their eigenvalue.
    Multiple vectors are shown - eigenvectors stay on their line,
    other vectors rotate.
    """

    def construct(self):
        # Matrix with eigenvalues 4 and -1
        mat = np.array([[1, 2], [3, 1]])
        eigenvalues, eigenvectors = np.linalg.eig(mat)

        # Create coordinate plane
        plane = NumberPlane((-4, 4), (-4, 4))
        plane.set_height(6)
        plane.add_coordinate_labels(font_size=24)

        # Create eigenvector lines (extended to infinity)
        eigenlines = VGroup()
        for i, ev in enumerate(eigenvectors.T):
            line = Line(-ev * 5, ev * 5)
            line.set_stroke([TEAL, YELLOW][i], 3, 0.5)
            eigenlines.add(line)

        # Create test vectors - some along eigenvectors, some not
        test_vectors = VGroup()
        colors = [TEAL, YELLOW, BLUE, RED, PURPLE]
        directions = [
            eigenvectors.T[0],      # First eigenvector direction
            eigenvectors.T[1],      # Second eigenvector direction
            np.array([1, 0]),       # Standard basis i
            np.array([0, 1]),       # Standard basis j
            np.array([1, 1]) / np.sqrt(2),  # Diagonal
        ]

        for direction, color in zip(directions, colors):
            vect = Arrow(
                plane.c2p(0, 0),
                plane.c2p(*direction),
                buff=0,
                fill_color=color,
                stroke_width=3,
            )
            test_vectors.add(vect)

        # Labels
        title = Text("Eigenvectors Stay on Their Line", font_size=36)
        title.to_corner(UL)
        title.set_backstroke(width=5)

        self.add(plane, eigenlines, title)
        self.play(LaggedStartMap(GrowArrow, test_vectors, lag_ratio=0.2))
        self.wait()

        # Transform all vectors
        transformed_vectors = VGroup()
        for i, (direction, color) in enumerate(zip(directions, colors)):
            new_dir = mat @ direction
            new_vect = Arrow(
                plane.c2p(0, 0),
                plane.c2p(*new_dir),
                buff=0,
                fill_color=color,
                stroke_width=3,
            )
            transformed_vectors.add(new_vect)

        self.play(
            Transform(test_vectors, transformed_vectors),
            run_time=3
        )
        self.wait(2)
