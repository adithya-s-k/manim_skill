"""
Lorenz Attractor Visualization

Demonstrates the classic Lorenz strange attractor with multiple trajectories
showing sensitivity to initial conditions (chaos theory).

Run: manimgl lorenz_attractor.py LorenzAttractor
"""
from manimlib import *
from scipy.integrate import solve_ivp


def lorenz_system(t, state, sigma=10, rho=28, beta=8 / 3):
    """
    The Lorenz system of differential equations.

    These equations model atmospheric convection and exhibit
    chaotic behavior for certain parameter values.
    """
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]


def ode_solution_points(function, state0, time, dt=0.01):
    """
    Solve an ODE system and return the trajectory points.

    Args:
        function: The ODE system function
        state0: Initial state [x0, y0, z0]
        time: Total evolution time
        dt: Time step for output points

    Returns:
        Array of shape (n_points, 3) with trajectory points
    """
    solution = solve_ivp(
        function,
        t_span=(0, time),
        y0=state0,
        t_eval=np.arange(0, time, dt)
    )
    return solution.y.T


class LorenzAttractor(InteractiveScene):
    """
    Visualizes the Lorenz attractor with multiple trajectories.

    Shows how nearby initial conditions diverge over time,
    demonstrating the butterfly effect in chaotic systems.
    """

    def construct(self):
        # Set up 3D axes
        axes = ThreeDAxes(
            x_range=(-50, 50, 5),
            y_range=(-50, 50, 5),
            z_range=(-0, 50, 5),
            width=16,
            height=16,
            depth=8,
        )
        axes.set_width(FRAME_WIDTH)
        axes.center()

        # Set up camera rotation for 3D viewing
        self.frame.reorient(43, 76, 1, IN, 10)
        self.frame.add_updater(lambda m, dt: m.increment_theta(dt * 3 * DEGREES))
        self.add(axes)

        # Add the Lorenz equations
        equations = Tex(
            R"""
            \begin{aligned}
            \frac{\mathrm{d} x}{\mathrm{~d} t} & =\sigma(y-x) \\
            \frac{\mathrm{d} y}{\mathrm{~d} t} & =x(\rho-z)-y \\
            \frac{\mathrm{d} z}{\mathrm{~d} t} & =x y-\beta z
            \end{aligned}
            """,
            t2c={
                "x": RED,
                "y": GREEN,
                "z": BLUE,
            },
            font_size=30
        )
        equations.fix_in_frame()
        equations.to_corner(UL)
        equations.set_backstroke()
        self.play(Write(equations))

        # Compute trajectories with slightly different initial conditions
        epsilon = 1e-5
        evolution_time = 30
        n_points = 10
        states = [
            [10, 10, 10 + n * epsilon]
            for n in range(n_points)
        ]
        colors = color_gradient([BLUE_E, BLUE_A], len(states))

        # Create curves from solutions
        curves = VGroup()
        for state, color in zip(states, colors):
            points = ode_solution_points(lorenz_system, state, evolution_time)
            curve = VMobject().set_points_smoothly(axes.c2p(*points.T))
            curve.set_stroke(color, 1, opacity=0.25)
            curves.add(curve)

        curves.set_stroke(width=2, opacity=1)

        # Create glowing dots that follow the trajectories
        dots = Group(GlowDot(color=color, radius=0.25) for color in colors)

        def update_dots(dots, curves=curves):
            for dot, curve in zip(dots, curves):
                dot.move_to(curve.get_end())

        dots.add_updater(update_dots)

        # Add tracing tails for visual effect
        tail = VGroup(
            TracingTail(dot, time_traced=3).match_color(dot)
            for dot in dots
        )

        self.add(dots)
        self.add(tail)
        curves.set_opacity(0)

        # Animate the trajectories
        self.play(
            *(
                ShowCreation(curve, rate_func=linear)
                for curve in curves
            ),
            run_time=evolution_time,
        )


class LorenzSimple(Scene):
    """
    A simpler version of the Lorenz attractor without equations overlay.
    Good for demonstrations focused on the attractor itself.
    """

    def construct(self):
        frame = self.camera.frame

        # Set up 3D axes
        axes = ThreeDAxes(
            x_range=(-50, 50, 10),
            y_range=(-50, 50, 10),
            z_range=(0, 50, 10),
            width=12,
            height=12,
            depth=6,
        )
        axes.center()
        self.add(axes)

        # Set camera angle
        frame.set_euler_angles(
            phi=70 * DEGREES,
            theta=-45 * DEGREES
        )

        # Add continuous rotation
        frame.add_updater(lambda m, dt: m.increment_theta(dt * 2 * DEGREES))

        # Compute single trajectory
        evolution_time = 40
        initial_state = [10, 10, 10]
        points = ode_solution_points(lorenz_system, initial_state, evolution_time)

        # Create the curve
        curve = VMobject()
        curve.set_points_smoothly(axes.c2p(*points.T))
        curve.set_stroke(
            color=color_gradient([BLUE, TEAL, GREEN, YELLOW, RED], 100),
            width=2
        )

        # Animate drawing the curve
        self.play(
            ShowCreation(curve, rate_func=linear),
            run_time=evolution_time,
        )
        self.wait(2)
