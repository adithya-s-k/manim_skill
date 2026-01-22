"""
ManimGL Interactive Scene Template

Run with: manimgl scene.py MyScene
Interactive: manimgl scene.py MyScene -se 15
"""
from manimlib import *


class MyInteractiveScene(InteractiveScene):
    def construct(self):
        # Setup - runs before interactive mode
        circle = Circle(color=BLUE)
        circle.set_fill(BLUE, opacity=0.5)

        square = Square(color=RED)
        square.next_to(circle, RIGHT, buff=1)

        self.play(ShowCreation(circle))
        self.play(ShowCreation(square))

        # Drop into interactive shell here
        # Use: manimgl file.py MyInteractiveScene -se 15
        self.embed()

        # Code below runs after exiting shell
        # Or paste code in shell with checkpoint_paste()

        # Example animations to paste:
        self.play(circle.animate.shift(LEFT * 2))
        self.play(Transform(circle, square))
        self.play(FadeOut(circle))


class My3DInteractiveScene(InteractiveScene):
    def construct(self):
        # Setup 3D
        frame = self.camera.frame
        frame.set_euler_angles(phi=70 * DEGREES, theta=-45 * DEGREES)

        # Fixed elements
        title = Text("3D Scene")
        title.to_edge(UP)
        title.fix_in_frame()
        self.add(title)

        # 3D content
        axes = ThreeDAxes()
        self.add(axes)

        surface = Surface(
            lambda u, v: np.array([u, v, np.sin(u) * np.cos(v)]),
            u_range=[-3, 3],
            v_range=[-3, 3],
        )
        surface.set_color(BLUE, opacity=0.8)
        self.play(ShowCreation(surface))

        # Interactive point
        self.embed()

        # Camera animation
        self.play(
            frame.animate.increment_theta(-30 * DEGREES),
            run_time=3
        )
