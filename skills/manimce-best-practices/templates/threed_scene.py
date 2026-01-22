"""
3D Scene Template for Manim Community

Use this for 3D visualizations with camera rotation and surfaces.

Render: manim -pql your_file.py Your3DScene
"""

from manim import *
import numpy as np


class Your3DScene(ThreeDScene):
    """
    Template for 3D scenes.

    Inherits from ThreeDScene which provides:
        - set_camera_orientation(phi, theta, gamma)
        - move_camera()
        - begin_ambient_camera_rotation() / stop_ambient_camera_rotation()
        - add_fixed_in_frame_mobjects() for 2D overlays
    """

    def construct(self):
        # ============================================================
        # CAMERA SETUP
        # ============================================================

        # Set initial camera orientation
        # phi: angle from z-axis (0 = top-down, 90 = side view)
        # theta: rotation around z-axis
        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=-45 * DEGREES
        )

        # ============================================================
        # 3D AXES
        # ============================================================

        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-2, 2, 1],
            x_length=6,
            y_length=6,
            z_length=4,
        )

        # Axis labels (stay fixed to camera orientation)
        axis_labels = axes.get_axis_labels(
            x_label="x",
            y_label="y",
            z_label="z"
        )

        self.play(Create(axes))
        self.add(axis_labels)
        self.wait()

        # ============================================================
        # 3D OBJECTS
        # ============================================================

        # --- Basic 3D shapes ---
        sphere = Sphere(radius=0.5, color=BLUE).shift(LEFT * 2)
        cube = Cube(side_length=0.8, color=RED, fill_opacity=0.8)

        self.play(Create(sphere), Create(cube))
        self.wait()

        # --- 3D Surface ---
        # z = sin(sqrt(x^2 + y^2))
        surface = Surface(
            lambda u, v: axes.c2p(
                u, v,
                np.sin(np.sqrt(u ** 2 + v ** 2))
            ),
            u_range=[-2.5, 2.5],
            v_range=[-2.5, 2.5],
            resolution=(20, 20),
            fill_opacity=0.6,
        )
        surface.set_color_by_gradient(BLUE, TEAL, GREEN)

        self.play(
            FadeOut(sphere),
            FadeOut(cube),
            Create(surface),
            run_time=2
        )
        self.wait()

        # ============================================================
        # 2D OVERLAY (Fixed to screen)
        # ============================================================

        # Title that stays fixed to screen (doesn't rotate with 3D scene)
        title = Text("3D Surface Visualization", font_size=36)
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        # Math equation overlay
        equation = MathTex(r"z = \sin\sqrt{x^2 + y^2}")
        equation.to_corner(UR)
        self.add_fixed_in_frame_mobjects(equation)
        self.play(Write(equation))

        # ============================================================
        # CAMERA MOVEMENT
        # ============================================================

        # --- Manual camera movement ---
        self.move_camera(phi=45 * DEGREES, theta=30 * DEGREES, run_time=2)
        self.wait()

        # --- Continuous rotation ---
        self.begin_ambient_camera_rotation(rate=0.2)  # radians per second
        self.wait(5)
        self.stop_ambient_camera_rotation()

        # ============================================================
        # CLEANUP
        # ============================================================

        self.play(
            FadeOut(surface),
            FadeOut(axes),
            FadeOut(axis_labels),
            FadeOut(title),
            FadeOut(equation),
        )
        self.wait()


# Run this specific scene:
# manim -pql threed_scene.py Your3DScene
