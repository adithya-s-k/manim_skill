"""
A 3D scene in ManimGX: axes, a sphere and a moving camera.

Render:
    manimgx render examples/three_d.py ThreeD -r 1280x720 --fps 30
"""

import manimgx as m


class ThreeD(m.ThreeDScene):
    def construct(self) -> None:
        self.set_camera_orientation(phi=65 * m.DEGREES, theta=-45 * m.DEGREES)

        axes = m.ThreeDAxes()
        sphere = m.Sphere(radius=1.4, fill_opacity=0.5, color=m.BLUE)
        label = m.Text("a sphere", font_size=32).to_corner(m.UL)
        self.add_fixed_in_frame_mobjects(label)

        self.play(m.Create(axes), m.Create(sphere), m.Write(label), run_time=2)
        self.begin_ambient_camera_rotation(rate=0.35)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        self.wait(0.5)
