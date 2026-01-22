"""
Moving Camera Scene Template for Manim Community

Use this for scenes that require zooming, panning, or following objects.

Render: manim -pql your_file.py YourCameraScene
"""

from manim import *


class YourCameraScene(MovingCameraScene):
    """
    Template for scenes with camera movement.

    Inherits from MovingCameraScene which provides:
        - self.camera.frame: The camera frame mobject
        - Ability to zoom, pan, and follow objects
    """

    def construct(self):
        # ============================================================
        # SETUP: Create objects to showcase camera movement
        # ============================================================

        # Create a grid of shapes to demonstrate camera movement
        shapes = VGroup(*[
            Circle(radius=0.3, color=color, fill_opacity=0.5)
            for color in [RED, BLUE, GREEN, YELLOW, PURPLE]
        ]).arrange(RIGHT, buff=1)

        # Add labels
        labels = VGroup(*[
            Text(str(i + 1), font_size=24).move_to(shape)
            for i, shape in enumerate(shapes)
        ])

        # Title
        title = Text("Camera Movement Demo", font_size=36).to_edge(UP)

        self.add(shapes, labels)
        self.play(Write(title))
        self.wait()

        # ============================================================
        # CAMERA OPERATIONS: Zoom, pan, follow
        # ============================================================

        # --- ZOOM IN ---
        # Save original camera state
        self.camera.frame.save_state()

        # Zoom into first shape
        self.play(
            self.camera.frame.animate.set(width=4).move_to(shapes[0])
        )
        self.wait()

        # --- PAN ---
        # Move camera to another shape
        self.play(
            self.camera.frame.animate.move_to(shapes[2])
        )
        self.wait()

        # --- ZOOM OUT ---
        # Restore original camera
        self.play(Restore(self.camera.frame))
        self.wait()

        # --- FOLLOW OBJECT ---
        # Create moving dot
        dot = Dot(color=RED, radius=0.15).move_to(LEFT * 5)
        self.add(dot)

        # Set camera to follow the dot
        self.camera.frame.add_updater(
            lambda m: m.move_to(dot.get_center())
        )

        # Move the dot (camera follows automatically)
        self.play(dot.animate.move_to(RIGHT * 5), run_time=3)
        self.wait()

        # Stop following
        self.camera.frame.clear_updaters()

        # ============================================================
        # CLEANUP: Reset and fade out
        # ============================================================

        self.play(
            self.camera.frame.animate.move_to(ORIGIN).set(width=14)
        )
        self.play(FadeOut(shapes, labels, title, dot))
        self.wait()


# Run this specific scene:
# manim -pql camera_scene.py YourCameraScene
