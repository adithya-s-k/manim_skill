"""
Math visualization in ManimGX: an equation, a colored derivation and a conclusion.

Render:
    manimgx render examples/math_visualization.py MathVisualization -r 1280x720 --fps 30
"""

import manimgx as m


class MathVisualization(m.Scene):
    def construct(self) -> None:
        title = m.Text("Pythagorean theorem", font_size=48).to_edge(m.UP)

        given = m.MathTex(r"a^2 + b^2 = c^2", font_size=64)
        given.next_to(title, m.DOWN, buff=0.8)

        values = m.MathTex(
            r"3^2 + 4^2 = c^2",
            font_size=56,
            substrings_to_isolate=[r"3^2", r"4^2"],
        ).next_to(given, m.DOWN, buff=0.6)
        values.set_color_by_tex(r"3^2", m.BLUE)
        values.set_color_by_tex(r"4^2", m.GREEN)

        result = m.MathTex(r"c = \sqrt{25} = 5", font_size=64, color=m.YELLOW)
        result.next_to(values, m.DOWN, buff=0.6)

        self.play(m.Write(title))
        self.play(m.Write(given))
        self.wait(0.5)
        self.play(m.ReplacementTransform(given, values))
        self.wait(0.5)
        self.play(m.ReplacementTransform(values, result))
        self.play(m.Circumscribe(result))
        self.wait(1)
