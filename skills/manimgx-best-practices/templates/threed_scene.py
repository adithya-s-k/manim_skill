"""
3D Scene Template for ManimGX

A ThreeDScene with axes and a turning camera.

Render:
    manimgx render templates/threed_scene.py ThreeDSceneTemplate -r 1280x720 --fps 30
"""

import manimgx as m


class ThreeDSceneTemplate(m.ThreeDScene):
    def construct(self) -> None:
        self.set_camera_orientation(phi=70 * m.DEGREES, theta=-45 * m.DEGREES)

        axes = m.ThreeDAxes()
        surface = m.Surface(
            lambda u, v: [u, v, u * v / 4],
            u_range=[-2, 2],
            v_range=[-2, 2],
            fill_opacity=0.6,
        )
        label = m.Text("z = xy / 4", font_size=32).to_corner(m.UL)
        self.add_fixed_in_frame_mobjects(label)

        self.play(m.Create(axes), m.Create(surface), m.Write(label), run_time=2)
        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        self.wait(0.5)
