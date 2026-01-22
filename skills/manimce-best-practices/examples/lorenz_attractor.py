"""
Lorenz Attractor - Converted from 3b1b ManimGL to ManimCE

Original: videos/_2024/manim_demo/lorenz.py
This demonstrates a chaotic system visualization with 3D curves and tracing dots.

Run with: manim -pql lorenz_attractor.py LorenzAttractor
"""

from manim import *
from scipy.integrate import solve_ivp
import numpy as np


def lorenz_system(t, state, sigma=10, rho=28, beta=8 / 3):
    """The Lorenz system of differential equations."""
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]


def ode_solution_points(function, state0, time, dt=0.01):
    """Solve ODE and return solution points."""
    solution = solve_ivp(
        function,
        t_span=(0, time),
        y0=state0,
        t_eval=np.arange(0, time, dt)
    )
    return solution.y.T


class LorenzAttractor(ThreeDScene):
    """
    Visualization of the Lorenz attractor - a classic chaotic system.

    Shows multiple trajectories starting from nearly identical initial conditions
    that diverge chaotically over time.
    """

    def construct(self):
        # Set up 3D axes
        axes = ThreeDAxes(
            x_range=(-50, 50, 10),
            y_range=(-50, 50, 10),
            z_range=(0, 50, 10),
            x_length=12,
            y_length=12,
            z_length=6,
        )
        axes.center()

        # Set camera orientation
        self.set_camera_orientation(phi=76 * DEGREES, theta=43 * DEGREES)

        self.add(axes)

        # Add the equations (fixed to screen)
        equations = MathTex(
            r"\frac{dx}{dt} &= \sigma(y-x) \\",
            r"\frac{dy}{dt} &= x(\rho-z)-y \\",
            r"\frac{dz}{dt} &= xy-\beta z",
            font_size=30
        )
        equations.to_corner(UL)
        self.add_fixed_in_frame_mobjects(equations)
        self.play(Write(equations))

        # Compute a set of solutions with slightly different initial conditions
        epsilon = 1e-5
        evolution_time = 20  # Reduced for faster rendering
        n_points = 5  # Reduced for performance

        states = [
            [10, 10, 10 + n * epsilon]
            for n in range(n_points)
        ]
        colors = color_gradient([BLUE_E, BLUE_A], len(states))

        # Create curves from ODE solutions
        curves = VGroup()
        for state, color in zip(states, colors):
            points = ode_solution_points(lorenz_system, state, evolution_time)
            # Scale points to fit axes
            scaled_points = [axes.c2p(p[0], p[1], p[2]) for p in points]
            curve = VMobject()
            curve.set_points_smoothly(scaled_points)
            curve.set_stroke(color, width=2, opacity=0.8)
            curves.add(curve)

        # Create dots that will trace the curves
        dots = VGroup(*[
            Dot3D(color=color, radius=0.15)
            for color in colors
        ])

        # Position dots at start of curves
        for dot, curve in zip(dots, curves):
            dot.move_to(curve.get_start())

        self.add(dots)

        # Start ambient camera rotation
        self.begin_ambient_camera_rotation(rate=0.1)

        # Animate curves being drawn with dots following
        self.play(
            *[Create(curve, rate_func=linear) for curve in curves],
            *[MoveAlongPath(dot, curve, rate_func=linear) for dot, curve in zip(dots, curves)],
            run_time=evolution_time,
        )

        self.wait(2)


class LorenzAttractorSimple(ThreeDScene):
    """
    Simplified version with just one trajectory and traced path.
    Better for understanding the basic pattern.
    """

    def construct(self):
        # Set up axes
        axes = ThreeDAxes(
            x_range=(-50, 50, 10),
            y_range=(-50, 50, 10),
            z_range=(0, 50, 10),
            x_length=10,
            y_length=10,
            z_length=5,
        )

        self.set_camera_orientation(phi=70 * DEGREES, theta=45 * DEGREES)
        self.add(axes)

        # Compute single trajectory
        evolution_time = 15
        points = ode_solution_points(lorenz_system, [10, 10, 10], evolution_time)
        scaled_points = [axes.c2p(p[0], p[1], p[2]) for p in points]

        # Create curve
        curve = VMobject()
        curve.set_points_smoothly(scaled_points)
        curve.set_stroke(BLUE, width=2)

        # Create moving dot with traced path
        dot = Dot3D(color=RED, radius=0.2)
        dot.move_to(curve.get_start())

        # Traced path follows the dot
        traced_path = TracedPath(
            dot.get_center,
            stroke_color=YELLOW,
            stroke_width=3,
        )

        self.add(traced_path, dot)

        # Title
        title = Text("Lorenz Attractor", font_size=36)
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)

        # Animate
        self.begin_ambient_camera_rotation(rate=0.15)
        self.play(
            MoveAlongPath(dot, curve, rate_func=linear),
            run_time=evolution_time,
        )
        self.wait(2)
