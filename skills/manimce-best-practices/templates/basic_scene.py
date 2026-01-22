"""
Basic Scene Template for Manim Community

Copy this file and modify to create your own scene.

Render: manim -pql your_file.py YourScene
"""

from manim import *


class YourScene(Scene):
    """
    Basic scene template.

    Attributes to configure:
        - background_color: Scene background (default: BLACK)
    """

    def construct(self):
        # ============================================================
        # SETUP: Configure scene, create initial objects
        # ============================================================

        # Optional: Set background color
        # self.camera.background_color = "#1a1a2e"

        # Create your mobjects
        title = Text("Your Animation Title", font_size=48)
        shape = Circle(color=BLUE, fill_opacity=0.5)

        # Position objects
        title.to_edge(UP)
        shape.move_to(ORIGIN)

        # ============================================================
        # ANIMATION: Animate your objects
        # ============================================================

        # Write title
        self.play(Write(title))
        self.wait(0.5)

        # Create shape
        self.play(Create(shape))
        self.wait(0.5)

        # Transform or animate
        self.play(shape.animate.scale(1.5).set_color(RED))
        self.wait()

        # ============================================================
        # CLEANUP: Final animations, fade out
        # ============================================================

        self.play(
            FadeOut(title),
            FadeOut(shape),
        )
        self.wait()


# Run this specific scene:
# manim -pql basic_scene.py YourScene
