"""
Basic gradient descent visualization on a 2D loss landscape.
Demonstrates: Surface plots, 3D camera, path animation, optimization concepts
"""
from manimlib import *
import numpy as np


class GradientDescentBasic(Scene):
    def construct(self):
        # Create a simple 2D loss landscape (contour view)
        axes = Axes(
            x_range=(-3, 3, 1),
            y_range=(-3, 3, 1),
            width=8,
            height=8
        )
        axes.to_edge(LEFT)

        # Loss function: simple quadratic bowl
        def loss_func(x, y):
            return 0.5 * x**2 + 0.8 * y**2 + 0.3 * x * y

        # Create contour lines
        contours = VGroup()
        for level in np.linspace(0.5, 8, 8):
            # Approximate contour as ellipse
            a = np.sqrt(2 * level / 0.5)  # x scale
            b = np.sqrt(2 * level / 0.8)  # y scale
            ellipse = Ellipse(width=a, height=b)
            ellipse.move_to(axes.get_origin())
            ellipse.set_stroke(
                color=interpolate_color(BLUE, RED, level / 8),
                width=2,
                opacity=0.7
            )
            contours.add(ellipse)

        # Title
        title = Text("Gradient Descent", font_size=60)
        title.to_edge(UP)

        # Labels
        w1_label = Tex("w_1")
        w1_label.next_to(axes.x_axis.get_right(), DOWN)
        w2_label = Tex("w_2")
        w2_label.next_to(axes.y_axis.get_top(), LEFT)

        self.play(FadeIn(title))
        self.play(FadeIn(axes), FadeIn(w1_label), FadeIn(w2_label))
        self.play(LaggedStartMap(FadeIn, contours, lag_ratio=0.1))
        self.wait()

        # Add minimum marker
        min_dot = Dot(axes.get_origin(), color=GREEN)
        min_label = Text("Minimum", font_size=24, color=GREEN)
        min_label.next_to(min_dot, DOWN)

        self.play(FadeIn(min_dot, scale=2), FadeIn(min_label))
        self.wait()

        # Starting point
        start_point = axes.c2p(2.5, -2)
        current_dot = Dot(start_point, color=YELLOW)
        current_dot.set_z_index(1)

        start_label = Text("Start", font_size=24)
        start_label.next_to(current_dot, UR, buff=0.1)

        self.play(FadeIn(current_dot, scale=2), FadeIn(start_label))
        self.wait()

        # Gradient descent path
        learning_rate = 0.2
        path_points = [np.array([2.5, -2.0])]
        current = path_points[0].copy()

        for _ in range(20):
            # Gradient of loss: [x + 0.15*y, 1.6*y + 0.15*x]
            grad = np.array([
                current[0] + 0.15 * current[1],
                1.6 * current[1] + 0.15 * current[0]
            ])
            current = current - learning_rate * grad
            path_points.append(current.copy())
            if np.linalg.norm(current) < 0.01:
                break

        # Create path
        path = VMobject()
        path.set_points_smoothly([axes.c2p(p[0], p[1]) for p in path_points])
        path.set_stroke(YELLOW, 3)

        # Animation info panel
        info_panel = VGroup()
        iter_text = Text("Iteration: 0", font_size=30)
        loss_text = Text("Loss: {:.3f}".format(loss_func(*path_points[0])), font_size=30)
        info_panel.add(iter_text, loss_text)
        info_panel.arrange(DOWN, aligned_edge=LEFT)
        info_panel.to_corner(UR)

        self.play(FadeIn(info_panel), FadeOut(start_label))

        # Animate gradient descent
        path_so_far = VMobject()
        path_so_far.set_stroke(YELLOW, 3)

        for i, (p1, p2) in enumerate(zip(path_points[:-1], path_points[1:])):
            # Draw gradient arrow
            p1_screen = axes.c2p(p1[0], p1[1])
            p2_screen = axes.c2p(p2[0], p2[1])

            arrow = Arrow(
                p1_screen, p2_screen,
                buff=0,
                stroke_width=3,
                color=RED
            )

            # Update info
            new_iter = Text(f"Iteration: {i + 1}", font_size=30)
            new_loss = Text(f"Loss: {loss_func(*p2):.3f}", font_size=30)
            new_info = VGroup(new_iter, new_loss)
            new_info.arrange(DOWN, aligned_edge=LEFT)
            new_info.move_to(info_panel)

            self.play(
                GrowArrow(arrow),
                current_dot.animate.move_to(p2_screen),
                Transform(info_panel, new_info),
                run_time=0.5
            )
            self.play(FadeOut(arrow), run_time=0.2)

            if i > 15:
                break

        self.wait()

        # Final message
        converged = Text("Converged!", font_size=48, color=GREEN)
        converged.next_to(title, DOWN)
        self.play(FadeIn(converged, scale=1.5))
        self.wait()

        # Show the full path
        self.play(
            ShowCreation(path),
            run_time=2
        )
        self.wait(2)


class GradientDescent3D(ThreeDScene):
    """3D visualization of gradient descent on a loss surface."""

    def construct(self):
        # Set up 3D view
        frame = self.camera.frame
        frame.set_euler_angles(theta=30 * DEGREES, phi=70 * DEGREES)

        # Create 3D axes
        axes = ThreeDAxes(
            x_range=(-3, 3, 1),
            y_range=(-3, 3, 1),
            z_range=(0, 5, 1),
            width=8,
            height=8,
            depth=4
        )

        # Loss surface
        def loss_func(x, y):
            return 0.3 * x**2 + 0.4 * y**2

        surface = axes.get_graph(
            loss_func,
            u_range=(-3, 3),
            v_range=(-3, 3),
        )
        surface.set_color_by_gradient(BLUE, GREEN, YELLOW, RED)
        surface.set_opacity(0.7)

        # Labels
        title = Text("Loss Landscape", font_size=48)
        title.to_corner(UL)
        title.fix_in_frame()

        self.play(
            FadeIn(axes),
            FadeIn(surface),
            FadeIn(title),
        )
        self.wait()

        # Rotate view
        self.play(
            frame.animate.set_euler_angles(theta=-30 * DEGREES),
            run_time=3
        )
        self.wait()

        # Gradient descent ball
        start = np.array([2.5, 2.0])
        ball = Sphere(radius=0.15, color=YELLOW)
        ball.move_to(axes.c2p(start[0], start[1], loss_func(*start)))

        self.play(FadeIn(ball, scale=2))

        # Animate descent
        learning_rate = 0.15
        current = start.copy()

        for _ in range(15):
            grad = np.array([0.6 * current[0], 0.8 * current[1]])
            new_pos = current - learning_rate * grad
            new_point = axes.c2p(new_pos[0], new_pos[1], loss_func(*new_pos))

            self.play(
                ball.animate.move_to(new_point),
                run_time=0.4
            )
            current = new_pos

        self.wait()

        # Final rotation
        self.play(
            frame.animate.set_euler_angles(theta=60 * DEGREES, phi=60 * DEGREES),
            run_time=3
        )
        self.wait(2)
