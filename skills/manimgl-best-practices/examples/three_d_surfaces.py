"""
3D Surfaces and Camera Movement

Demonstrates 3D surface creation, parametric surfaces,
and camera manipulation in ManimGL.

Run: manimgl three_d_surfaces.py ParametricSurface3D -w
Preview: manimgl three_d_surfaces.py ParametricSurface3D -p

Source: Inspired by 3b1b's 3D visualizations
"""
from manimlib import *
import numpy as np


class ParametricSurface3D(InteractiveScene):
    """
    Creates a beautiful 3D parametric surface with camera rotation.
    """

    def construct(self):
        frame = self.frame

        # Create 3D axes
        axes = ThreeDAxes(
            x_range=(-3, 3, 1),
            y_range=(-3, 3, 1),
            z_range=(-2, 2, 1),
        )

        # Parametric surface: z = sin(x) * cos(y)
        surface = ParametricSurface(
            lambda u, v: [u, v, np.sin(u) * np.cos(v)],
            u_range=(-3, 3),
            v_range=(-3, 3),
            resolution=(30, 30),
        )
        # Color by z value
        surface.set_color(BLUE)
        surface.set_opacity(0.8)

        self.add(axes)

        # Rotate camera to good initial position
        frame.reorient(-30, 70, 0)
        frame.set_height(10)

        # Create surface
        self.play(ShowCreation(surface, run_time=3))
        self.wait()

        # Rotate camera around
        self.play(
            frame.animate.reorient(30, 60, 0),
            run_time=3
        )
        self.play(
            frame.animate.reorient(-60, 80, 0),
            run_time=3
        )
        self.wait()


class SphereSurface(InteractiveScene):
    """
    Creates a sphere and demonstrates 3D transformations.
    """

    def construct(self):
        frame = self.frame
        frame.reorient(-20, 70, 0)

        # Create sphere
        sphere = Sphere(radius=2)
        sphere.set_color(BLUE)
        sphere.set_opacity(0.7)

        # Create latitude/longitude lines
        lat_lines = VGroup(*[
            ParametricCurve(
                lambda t, phi=phi: 2 * np.array([
                    np.cos(t) * np.cos(phi),
                    np.sin(t) * np.cos(phi),
                    np.sin(phi)
                ]),
                t_range=(0, TAU, 0.1),
                color=WHITE,
                stroke_width=1,
                stroke_opacity=0.5,
            )
            for phi in np.linspace(-PI/2 + 0.3, PI/2 - 0.3, 6)
        ])

        long_lines = VGroup(*[
            ParametricCurve(
                lambda t, theta=theta: 2 * np.array([
                    np.cos(theta) * np.cos(t),
                    np.sin(theta) * np.cos(t),
                    np.sin(t)
                ]),
                t_range=(-PI/2, PI/2, 0.1),
                color=WHITE,
                stroke_width=1,
                stroke_opacity=0.5,
            )
            for theta in np.linspace(0, TAU, 12, endpoint=False)
        ])

        self.play(ShowCreation(sphere))
        self.play(
            ShowCreation(lat_lines, run_time=2),
            ShowCreation(long_lines, run_time=2),
        )

        # Rotate
        self.play(
            Rotate(sphere, TAU, axis=OUT, run_time=4),
            Rotate(lat_lines, TAU, axis=OUT, run_time=4),
            Rotate(long_lines, TAU, axis=OUT, run_time=4),
        )
        self.wait()


class ConeUnfolding(InteractiveScene):
    """
    A cone that unfolds into a flat sector.
    Demonstrates surface transformation.
    """

    def construct(self):
        frame = self.frame
        frame.reorient(-30, 70, 0)
        frame.set_height(8)

        # Create cone
        height = 3
        radius = 2

        cone = ParametricSurface(
            lambda u, v: [
                v * radius / height * np.cos(u),
                v * radius / height * np.sin(u),
                height - v
            ],
            u_range=(0, TAU),
            v_range=(0, height),
            resolution=(30, 10),
        )
        cone.set_color(BLUE_E)
        cone.set_opacity(0.8)

        self.play(ShowCreation(cone, run_time=2))
        self.wait()

        # Animate camera
        self.play(
            frame.animate.reorient(0, 0, 0).set_height(10),
            run_time=2
        )
        self.wait()


class SaddleSurface(InteractiveScene):
    """
    Hyperbolic paraboloid (saddle surface).
    Classic example of negative Gaussian curvature.
    """

    def construct(self):
        frame = self.frame
        frame.reorient(-40, 70, 0)

        # Create saddle: z = x^2 - y^2
        surface = ParametricSurface(
            lambda u, v: [u, v, 0.3 * (u**2 - v**2)],
            u_range=(-2, 2),
            v_range=(-2, 2),
            resolution=(20, 20),
        )
        # Color gradient based on z
        surface.set_color(BLUE)
        surface.set_opacity(0.9)

        # Axes
        axes = ThreeDAxes(
            x_range=(-3, 3, 1),
            y_range=(-3, 3, 1),
            z_range=(-2, 2, 1),
        )

        self.play(ShowCreation(axes))
        self.play(ShowCreation(surface, run_time=2))

        # Show cross sections
        x_section = ParametricCurve(
            lambda t: [t, 0, 0.3 * t**2],
            t_range=(-2, 2, 0.1),
            color=RED,
            stroke_width=4,
        )

        y_section = ParametricCurve(
            lambda t: [0, t, -0.3 * t**2],
            t_range=(-2, 2, 0.1),
            color=BLUE,
            stroke_width=4,
        )

        self.play(ShowCreation(x_section))
        self.play(ShowCreation(y_section))

        # Rotate view
        self.play(
            frame.animate.reorient(60, 60, 0),
            run_time=4
        )
        self.wait()


class TorusSurface(InteractiveScene):
    """
    Creates a torus (donut shape).
    Classic example of parametric surface.
    """

    def construct(self):
        frame = self.frame
        frame.reorient(-30, 70, 0)

        # Torus parameters
        R = 2  # Major radius
        r = 0.7  # Minor radius

        torus = ParametricSurface(
            lambda u, v: [
                (R + r * np.cos(v)) * np.cos(u),
                (R + r * np.cos(v)) * np.sin(u),
                r * np.sin(v)
            ],
            u_range=(0, TAU),
            v_range=(0, TAU),
            resolution=(40, 20),
        )
        torus.set_color(BLUE_D)
        torus.set_opacity(0.8)

        self.play(ShowCreation(torus, run_time=3))

        # Rotate the torus
        self.play(
            Rotate(torus, TAU, axis=UP, run_time=6, rate_func=linear),
        )

        # Camera orbit
        self.play(
            frame.animate.reorient(150, 50, 0),
            run_time=4
        )
        self.wait()
