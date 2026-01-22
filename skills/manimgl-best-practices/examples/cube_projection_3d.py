"""
Visualization of 3D cube projection along the diagonal.
Shows how projecting a cube along the [1,1,1] direction creates a hexagonal pattern.
"""
from manimlib import *
import itertools as it


class CubeProjection3D(InteractiveScene):
    """
    Demonstrates projecting a 3D cube along its main diagonal [1,1,1].

    Shows:
    1. Building the cube from vertices
    2. Showing coordinates
    3. Looking down the diagonal
    4. The projected hexagonal pattern
    5. Face projections
    """
    def construct(self):
        # Set axes
        frame = self.frame
        light_source = self.camera.light_source

        frame.reorient(28, 68, 0, (0.99, 0.63, 0.66), 2.89)
        light_source.move_to([3, 5, 7])

        axes = ThreeDAxes(
            (-3, 3), (-3, 3), (-3, 3),
            axis_config=dict(tick_size=0.05)
        )
        axes.set_stroke(GREY_A, 1)
        plane = NumberPlane((-3, 3), (-3, 3))
        plane.axes.set_stroke(GREY_A, 1)
        plane.background_lines.set_stroke(BLUE_E, 0.5)
        plane.faded_lines.set_stroke(BLUE_E, 0.5, 0.25)

        self.add(plane, axes)

        # Add cube
        vertices = np.array(list(it.product(*3 * [[0, 1]])))
        vert_dots = DotCloud(vertices)
        vert_dots.make_3d()
        vert_dots.set_radius(0.025)
        vert_dots.set_color(TEAL)

        cube_shell = VGroup(
            Line(vertices[i], vertices[j])
            for i, p1 in enumerate(vertices)
            for j, p2 in enumerate(vertices[i + 1:], start=i + 1)
            if get_norm(p2 - p1) == 1
        )
        cube_shell.set_stroke(YELLOW, 1)
        cube_shell.set_anti_alias_width(1)
        cube_shell.set_width(1)
        cube_shell.move_to(ORIGIN, [-1, -1, -1])

        self.play(Write(cube_shell, lag_ratio=0.1, run_time=2))
        self.wait()

        # Show the coordinates
        labels = VGroup()
        for vert in vertices:
            coords = vert.astype(int)
            label = Tex(str(tuple(coords)), font_size=12)
            label.next_to(vert, DR, buff=0.05)
            label.rotate(45 * DEGREES, RIGHT, about_point=vert)
            label.set_backstroke(BLACK, 2)
            labels.add(label)

        self.play(
            LaggedStartMap(FadeIn, labels),
            FadeIn(vert_dots),
            frame.animate.reorient(10, 61, 0, (0.9, 0.51, 0.48), 2.44),
            run_time=3,
        )
        self.wait()

        # Show base and top square
        edges = VGroup(*cube_shell)
        edges.sort(lambda p: p[2])

        self.play(
            edges[4:].animate.set_stroke(width=0.5, opacity=0.25),
            labels[1::2].animate.set_opacity(0.1)
        )
        self.wait()
        self.play(
            edges[8:].animate.set_stroke(width=2, opacity=1),
            labels[1::2].animate.set_opacity(1),
            edges[:4].animate.set_stroke(width=0.5, opacity=0.25),
            labels[0::2].animate.set_opacity(0.1)
        )
        self.wait()
        self.play(
            edges.animate.set_stroke(width=1, opacity=1),
            labels.animate.set_opacity(1)
        )

        self.play(FadeOut(labels))

        # Orient to look down the corner
        self.play(frame.animate.reorient(135.795, 55.795, 0, (-0.02, -0.08, 0.05), 3.61), run_time=4)
        self.wait(2)
        self.play(frame.animate.reorient(50, 68, 0, (-0.46, 0.29, 0.23), 3.45), run_time=4)

        # Show the flat projection
        diag_vect = Vector([1, 1, 1], thickness=2)
        diag_vect.set_perpendicular_to_camera(frame)
        diag_label = labels[-1].copy()

        proj_mat = self.construct_proj_matrix()
        proj_cube_shell = cube_shell.copy().apply_matrix(proj_mat)
        proj_vert_dots = vert_dots.copy().apply_matrix(proj_mat)

        self.play(
            GrowArrow(diag_vect),
            FadeIn(diag_label, shift=np.ones(3)),
            cube_shell.animate.set_stroke(opacity=0.25),
        )
        self.wait()
        self.play(
            TransformFromCopy(cube_shell, proj_cube_shell),
            TransformFromCopy(vert_dots, proj_vert_dots),
        )

        self.wait(3)
        frame.save_state()
        self.play(
            frame.animate.reorient(134.75, 54.47, 0, (-0.46, 0.29, 0.23), 3.45).set_field_of_view(1 * DEGREES),
            run_time=4
        )
        self.wait()
        self.play(Restore(frame, run_time=3))
        self.wait()

        # Project more cubes down
        cube_grid = VGroup(
            cube_shell.copy().shift(vect)
            for vect in it.product(*3 * [[0, 1, 2]])
        )
        cube_grid.remove(cube_grid[0])
        proj_cube_grid = cube_grid.copy().apply_matrix(proj_mat)
        proj_cube_grid.set_stroke(YELLOW, 2, 0.5)

        ghost_cube = cube_shell.copy().set_opacity(0)
        self.play(
            LaggedStart(
                (TransformFromCopy(ghost_cube, new_cube)
                for new_cube in cube_grid),
                lag_ratio=0.05,
            ),
            frame.animate.reorient(40, 72, 0, (1.25, 1.69, 0.99), 5.10),
            run_time=5
        )
        self.wait()
        self.play(
            TransformFromCopy(cube_grid, proj_cube_grid),
            frame.animate.reorient(60, 68, 0, (0.81, 1.09, 0.94), 5.36),
            run_time=3
        )
        self.wait()
        self.play(
            FadeOut(cube_grid),
            FadeOut(proj_cube_grid),
            FadeOut(diag_label),
            FadeOut(diag_vect),
            FadeOut(vert_dots),
            FadeOut(proj_vert_dots),
            frame.animate.reorient(42, 62, 0, (0.68, 0.48, 0.41), 2.34),
            run_time=2,
        )

        # Show cube faces
        cube = Cube()
        cube.set_color(BLUE_E, 1)
        cube.set_shading(0.75, 0.25, 0.5)
        cube.replace(cube_shell)
        cube.sort(lambda p: np.dot(p, np.ones(3)))
        inner_faces = cube[:3]

        for mob in [cube_shell, proj_cube_shell, plane]:
            mob.apply_depth_test()
        self.add(axes, cube, cube_shell, plane, proj_cube_shell)
        self.play(
            FadeIn(cube),
            proj_cube_shell.animate.set_stroke(width=1, opacity=0.2),
        )
        self.wait(3)

    def construct_proj_matrix(self):
        diag = normalize(np.ones(3))
        id3 = np.identity(3)
        return np.array([self.project(basis, diag) for basis in id3]).T

    def project(self, vect, unit_norm):
        """Project v1 onto the orthogonal subspace of norm"""
        return vect - np.dot(unit_norm, vect) * unit_norm
