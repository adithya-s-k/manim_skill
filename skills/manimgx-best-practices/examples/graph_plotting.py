"""
Graph plotting in ManimGX: axes, a function and the area under it.

Render:
    manimgx render examples/graph_plotting.py GraphPlotting -r 1280x720 --fps 30
"""

import manimgx as m


class GraphPlotting(m.Scene):
    def construct(self) -> None:
        axes = m.Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 5, 1],
            x_length=8,
            y_length=5,
            axis_config={"include_tip": True},
        )
        labels = axes.get_axis_labels(x_label="x", y_label="y")

        curve = axes.plot(lambda x: x**2, x_range=[-2.2, 2.2], color=m.BLUE)
        area = axes.get_area(curve, x_range=[0, 2], color=m.BLUE, opacity=0.35)

        self.play(m.Create(axes), m.Write(labels))
        self.play(m.Create(curve), run_time=1.5)
        self.play(m.FadeIn(area))
        self.wait(1)
