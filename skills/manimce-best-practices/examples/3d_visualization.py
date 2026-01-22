"""
3D Visualization Patterns for Manim Community

Demonstrates ThreeDScene, 3D axes, surfaces, and camera control.
Adapted from 3b1b patterns for ManimCE.

Run with: manim -pql 3d_visualization.py SceneName
"""

from manim import *
import numpy as np


class Basic3DScene(ThreeDScene):
    """Basic 3D scene with shapes."""

    def construct(self):
        # Set camera orientation
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)

        # 3D shapes
        sphere = Sphere(radius=1, color=BLUE)
        cube = Cube(side_length=1.5, color=RED, fill_opacity=0.7)
        cone = Cone(base_radius=0.8, height=1.5, color=GREEN)

        # Position shapes
        sphere.shift(LEFT * 3)
        cone.shift(RIGHT * 3)

        self.play(Create(sphere), Create(cube), Create(cone))
        self.wait()

        # Rotate camera
        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(4)
        self.stop_ambient_camera_rotation()


class ThreeDAxesExample(ThreeDScene):
    """3D coordinate axes and plotting."""

    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        # Create 3D axes
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-2, 2, 1],
            x_length=6,
            y_length=6,
            z_length=4,
        )

        # Axis labels
        x_label = axes.get_x_axis_label(r"x")
        y_label = axes.get_y_axis_label(r"y")
        z_label = axes.get_z_axis_label(r"z")

        self.play(Create(axes))
        self.add_fixed_orientation_mobjects(x_label, y_label, z_label)
        self.wait()

        # Add a point
        point = Dot3D(axes.c2p(2, 1, 1.5), color=RED, radius=0.1)
        self.play(Create(point))

        # Camera rotation
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)


class ParametricSurfaceExample(ThreeDScene):
    """3D parametric surface visualization."""

    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=-60 * DEGREES)

        axes = ThreeDAxes(
            x_range=[-3, 3],
            y_range=[-3, 3],
            z_range=[-2, 2],
        )

        # Saddle surface: z = x^2 - y^2
        surface = Surface(
            lambda u, v: axes.c2p(u, v, u ** 2 - v ** 2),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(20, 20),
            fill_opacity=0.7,
        )
        surface.set_color_by_gradient(BLUE, GREEN, YELLOW)

        self.play(Create(axes))
        self.play(Create(surface), run_time=2)

        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(5)


class SphereVisualization(ThreeDScene):
    """Sphere with parametric representation."""

    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)

        # Parametric sphere
        sphere = Surface(
            lambda u, v: np.array([
                np.cos(v) * np.sin(u),
                np.sin(v) * np.sin(u),
                np.cos(u)
            ]),
            u_range=[0, PI],
            v_range=[0, 2 * PI],
            resolution=(20, 40),
        )
        sphere.set_color_by_gradient(BLUE_E, BLUE, TEAL)

        self.play(Create(sphere), run_time=2)

        # Animate camera
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)


class Function3DPlot(ThreeDScene):
    """Plotting z = f(x, y) surfaces."""

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)

        axes = ThreeDAxes(
            x_range=[-3, 3],
            y_range=[-3, 3],
            z_range=[-1, 1],
        )

        # Sine wave surface
        surface = Surface(
            lambda u, v: axes.c2p(
                u, v,
                np.sin(np.sqrt(u ** 2 + v ** 2))
            ),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(30, 30),
        )
        surface.set_color_by_gradient(PURPLE, RED, ORANGE)

        self.play(Create(axes))
        self.play(Create(surface), run_time=2)

        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(6)


class VectorField3D(ThreeDScene):
    """3D vector field visualization."""

    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)

        axes = ThreeDAxes(
            x_range=[-3, 3],
            y_range=[-3, 3],
            z_range=[-3, 3],
        )

        # Create arrows representing a vector field
        arrows = VGroup()
        for x in np.arange(-2, 3, 1):
            for y in np.arange(-2, 3, 1):
                for z in np.arange(-2, 3, 1):
                    # Vector field: F = (-y, x, z)
                    start = axes.c2p(x, y, z)
                    direction = np.array([-y, x, z]) * 0.3
                    end = start + direction

                    arrow = Arrow3D(
                        start=start,
                        end=end,
                        color=interpolate_color(
                            BLUE, RED,
                            (z + 2) / 4
                        ),
                    )
                    arrows.add(arrow)

        self.play(Create(axes))
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.02))

        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)


class CameraMovement3D(ThreeDScene):
    """Demonstrating 3D camera controls."""

    def construct(self):
        # Start with a default view
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # Create a 3D object
        torus = Torus(
            major_radius=2,
            minor_radius=0.5,
            color=BLUE,
            fill_opacity=0.8
        )

        self.play(Create(torus))
        self.wait()

        # Move camera to different angles
        self.move_camera(phi=30 * DEGREES, theta=0, run_time=2)
        self.wait()

        self.move_camera(phi=90 * DEGREES, theta=90 * DEGREES, run_time=2)
        self.wait()

        # Zoom by adjusting frame
        self.move_camera(zoom=1.5, run_time=1)
        self.wait()

        self.move_camera(zoom=0.7, run_time=1)
        self.wait()


class Line3DExample(ThreeDScene):
    """3D lines and curves."""

    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        axes = ThreeDAxes()

        # 3D helix
        helix = ParametricFunction(
            lambda t: np.array([
                np.cos(t),
                np.sin(t),
                t / 4
            ]),
            t_range=[0, 4 * PI],
            color=YELLOW,
        )

        # Line in 3D
        line = Line3D(
            start=axes.c2p(-2, -2, -1),
            end=axes.c2p(2, 2, 1),
            color=RED,
        )

        self.play(Create(axes))
        self.play(Create(helix), run_time=2)
        self.play(Create(line))

        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(5)


class TextIn3D(ThreeDScene):
    """Text and math in 3D scenes."""

    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)

        axes = ThreeDAxes()

        # 3D text (stays fixed to camera)
        title = Text("3D Visualization", font_size=48)
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)

        # Math label fixed to camera
        equation = MathTex(r"z = x^2 + y^2")
        equation.to_corner(UR)
        self.add_fixed_in_frame_mobjects(equation)

        # Surface
        paraboloid = Surface(
            lambda u, v: axes.c2p(u, v, u ** 2 + v ** 2),
            u_range=[-1.5, 1.5],
            v_range=[-1.5, 1.5],
            resolution=(15, 15),
        )
        paraboloid.set_color_by_gradient(BLUE, GREEN)

        self.play(Write(title), Write(equation))
        self.play(Create(axes))
        self.play(Create(paraboloid))

        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)


class AnimatedSurface(ThreeDScene):
    """Surface that changes over time."""

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)

        axes = ThreeDAxes(
            x_range=[-3, 3],
            y_range=[-3, 3],
            z_range=[-2, 2],
        )

        # Time parameter
        time = ValueTracker(0)

        # Animated wave surface
        surface = always_redraw(
            lambda: Surface(
                lambda u, v: axes.c2p(
                    u, v,
                    np.sin(np.sqrt(u ** 2 + v ** 2) - time.get_value())
                ),
                u_range=[-3, 3],
                v_range=[-3, 3],
                resolution=(25, 25),
            ).set_color_by_gradient(BLUE, TEAL)
        )

        self.add(axes, surface)

        # Animate
        self.play(
            time.animate.set_value(4 * PI),
            run_time=8,
            rate_func=linear
        )


class MultipleObjects3D(ThreeDScene):
    """Combining multiple 3D objects."""

    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=-30 * DEGREES)

        # Create various 3D shapes
        sphere = Sphere(radius=0.5, color=RED).shift(LEFT * 2 + UP)
        cube = Cube(side_length=0.8, color=BLUE).shift(RIGHT * 2)
        cylinder = Cylinder(
            radius=0.4,
            height=1.2,
            color=GREEN
        ).shift(DOWN + LEFT)

        # Arrows connecting them
        arrow1 = Arrow3D(
            start=sphere.get_center(),
            end=cube.get_center(),
            color=YELLOW
        )
        arrow2 = Arrow3D(
            start=cube.get_center(),
            end=cylinder.get_center(),
            color=YELLOW
        )

        self.play(
            Create(sphere),
            Create(cube),
            Create(cylinder),
        )
        self.play(Create(arrow1), Create(arrow2))

        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)
