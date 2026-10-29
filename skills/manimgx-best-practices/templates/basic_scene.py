"""
Basic Scene Template for ManimGX

Copy this file and modify it to create your own scene.

Render:
    manimgx render templates/basic_scene.py YourScene -r 1280x720 --fps 30
"""

import manimgx as m


class YourScene(m.Scene):
    """
    A basic 2D scene template.

    Configure the scene in setup(), build mobjects in construct(), animate with self.play().
    """

    def setup(self) -> None:
        # Optional: white background for the whole file
        # m.config.background_color = m.WHITE
        pass

    def construct(self) -> None:
        # ============================================================
        # SETUP: create initial objects
        # ============================================================
        title = m.Text("Your Animation Title", font_size=48)
        shape = m.Circle(radius=1.5, color=m.BLUE, fill_opacity=0.5)

        title.to_edge(m.UP)
        shape.move_to(m.ORIGIN)

        # ============================================================
        # ANIMATION: show them
        # ============================================================
        self.play(m.Write(title))
        self.wait(0.5)
        self.play(m.Create(shape))
        self.wait(0.5)
        self.play(shape.animate.scale(1.4).set_color(m.RED))
        self.wait(1)

        # ============================================================
        # CLEANUP
        # ============================================================
        self.play(m.FadeOut(title), m.FadeOut(shape))
        self.wait(0.5)
