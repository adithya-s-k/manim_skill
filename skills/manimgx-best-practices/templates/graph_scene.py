"""
Graph Scene Template for ManimGX

Axes, a plotted function and its label.

Render:
    manimgx render templates/graph_scene.py GraphScene -r 1280x720 --fps 30
"""

import manimgx as m


class GraphScene(m.Scene):
    def construct(self) -> None:
        axes = m.Axes(
            x_range=[-4, 4, 1],
            y_range=[-2, 6, 1],
            x_length=9,
            y_length=5,
            axis_config={"include_tip": True},
        )
        labels = axes.get_axis_labels(x_label="x", y_label="y")

        curve = axes.plot(lambda x: x**2 - 1, x_range=[-2.4, 2.4], color=m.YELLOW)
        name = m.MathTex(r"y = x^2 - 1", font_size=40).to_corner(m.UR)

        self.play(m.Create(axes), m.Write(labels))
        self.play(m.Create(curve), m.Write(name), run_time=2)
        self.wait(1)
