"""
Basic animations in ManimGX: shapes, text, a LaggedStart and a transform.

Render:
    manimgx render examples/basic_animations.py BasicAnimations -r 1280x720 --fps 30
"""

import manimgx as m


class BasicAnimations(m.Scene):
    def construct(self) -> None:
        title = m.Text("ManimGX basics", font_size=52).to_edge(m.UP)

        circle = m.Circle(radius=1.2, color=m.BLUE, fill_opacity=0.4)
        square = m.Square(side_length=2, color=m.GREEN, fill_opacity=0.4)
        triangle = m.Triangle(color=m.YELLOW, fill_opacity=0.4)
        shapes = m.VGroup(circle, square, triangle).arrange(m.RIGHT, buff=1)

        self.play(m.Write(title))
        self.play(m.LaggedStart(*[m.Create(s) for s in shapes], lag_ratio=0.25))
        self.wait(0.5)

        self.play(m.Transform(circle, m.Star(color=m.RED, fill_opacity=0.6)))
        self.play(m.Indicate(square), m.Circumscribe(triangle))
        self.wait(0.5)

        self.play(m.FadeOut(title), m.FadeOut(shapes))
        self.wait(0.5)
