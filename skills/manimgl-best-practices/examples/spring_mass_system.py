"""
Spring-Mass System with Live Graph

A physics simulation showing a spring-mass oscillator with real-time
position tracking on a graph. Demonstrates damped harmonic motion.

Run: manimgl spring_mass_system.py SpringMassDemo -w
Preview: manimgl spring_mass_system.py SpringMassDemo -p

Source: Adapted from 3b1b's Laplace transform video (2025)
"""
from manimlib import *
import math


class SpringMassSystem(VGroup):
    """
    A reusable spring-mass system component with physics simulation.

    This is a great example of 3b1b's approach: create a self-contained
    VGroup subclass that handles its own physics and rendering.
    """

    def __init__(
        self,
        x0=0,                      # Initial displacement from equilibrium
        v0=0,                      # Initial velocity
        k=3,                       # Spring constant
        mu=0.1,                    # Damping coefficient
        equilibrium_length=5,     # Rest length of spring
        equilibrium_position=ORIGIN,
        direction=RIGHT,
        spring_stroke_color=GREY_B,
        spring_stroke_width=2,
        spring_radius=0.25,
        n_spring_curls=8,
        mass_width=1.0,
        mass_color=BLUE_E,
        mass_label="m",
    ):
        super().__init__()
        self.equilibrium_position = equilibrium_position
        self.fixed_spring_point = equilibrium_position - (equilibrium_length - 0.5 * mass_width) * direction
        self.direction = direction
        self.rot_off_horizontal = angle_between_vectors(RIGHT, direction)

        # Create visual components
        self.mass = self._create_mass(mass_width, mass_color, mass_label)
        self.spring = self._create_spring(spring_stroke_color, spring_stroke_width, n_spring_curls, spring_radius)
        self.add(self.spring, self.mass)

        # Physics state
        self.k = k
        self.mu = mu
        self.velocity = v0
        self._is_running = True

        # Set initial position
        self.set_x(x0)

        # Add physics updater
        self.add_updater(lambda m, dt: m.time_step(dt))

    def _create_spring(self, stroke_color, stroke_width, n_curls, radius):
        """Create a 3D helix spring using parametric curve."""
        spring = ParametricCurve(
            lambda t: [t, -radius * math.sin(TAU * t), radius * math.cos(TAU * t)],
            t_range=(0, n_curls, 0.01),
            stroke_color=stroke_color,
            stroke_width=stroke_width,
        )
        spring.rotate(self.rot_off_horizontal)
        return spring

    def _create_mass(self, mass_width, mass_color, mass_label):
        """Create the mass block with label."""
        mass = Square(mass_width)
        mass.set_fill(mass_color, 1)
        mass.set_stroke(WHITE, 1)
        mass.set_shading(0.1, 0.1, 0.1)

        label = Tex(mass_label)
        label.set_max_width(0.5 * mass.get_width())
        label.move_to(mass)
        mass.add(label)
        mass.label = label
        return mass

    def set_x(self, x):
        """Set displacement from equilibrium position."""
        self.mass.move_to(self.equilibrium_position + x * self.direction)

        # Stretch spring to connect fixed point to mass
        spring_width = SMALL_BUFF + get_norm(self.mass.get_left() - self.fixed_spring_point)
        self.spring.rotate(-self.rot_off_horizontal)
        self.spring.set_width(spring_width, stretch=True)
        self.spring.rotate(self.rot_off_horizontal)
        self.spring.move_to(self.fixed_spring_point, -self.direction)

    def get_x(self):
        """Get current displacement."""
        return (self.mass.get_center() - self.equilibrium_position)[0]

    def time_step(self, delta_t, dt_size=0.01):
        """Integrate physics using simple Euler method."""
        if not self._is_running or delta_t == 0:
            return

        state = [self.get_x(), self.velocity]
        sub_steps = max(int(delta_t / dt_size), 1)
        true_dt = delta_t / sub_steps

        for _ in range(sub_steps):
            x, v = state
            # Damped harmonic oscillator: x'' = -kx - μv
            acceleration = -self.k * x - self.mu * v
            state[0] += v * true_dt
            state[1] += acceleration * true_dt

        self.set_x(state[0])
        self.velocity = state[1]

    def pause(self):
        self._is_running = False

    def unpause(self):
        self._is_running = True

    def get_velocity_vector(self, scale_factor=0.5, v_offset=-0.25, color=GREEN):
        """Get a dynamic vector showing velocity."""
        vector = Vector(RIGHT, fill_color=color, stroke_color=color)
        v_shift = v_offset * UP
        vector.add_updater(lambda m: m.put_start_and_end_on(
            self.mass.get_center() + v_shift,
            self.mass.get_center() + v_shift + scale_factor * self.velocity * RIGHT
        ))
        return vector

    def get_force_vector(self, scale_factor=0.5, v_offset=0.25, color=RED):
        """Get a dynamic vector showing net force."""
        vector = Vector(RIGHT, fill_color=color, stroke_color=color)
        v_shift = v_offset * UP
        def get_force():
            return -self.k * self.get_x() - self.mu * self.velocity
        vector.add_updater(lambda m: m.put_start_and_end_on(
            self.mass.get_center() + v_shift,
            self.mass.get_center() + v_shift + scale_factor * get_force() * RIGHT
        ))
        return vector


class SpringMassDemo(InteractiveScene):
    """
    Main demonstration scene showing spring-mass oscillation.
    """

    def construct(self):
        # Create spring system with initial displacement
        spring = SpringMassSystem(
            x0=2,
            mu=0.15,
            k=3,
            equilibrium_position=2 * LEFT,
            equilibrium_length=5,
        )
        self.add(spring)

        # Create number line to show position
        number_line = NumberLine(x_range=(-4, 4, 1))
        number_line.next_to(spring.equilibrium_position, DOWN, buff=2.0)
        number_line.add_numbers(font_size=24)

        # Arrow tip indicator on number line
        arrow_tip = ArrowTip(length=0.2, width=0.1)
        arrow_tip.rotate(-90 * DEG)
        arrow_tip.set_fill(TEAL)
        arrow_tip.add_updater(lambda m: m.move_to(number_line.n2p(spring.get_x()), DOWN))

        # Let it oscillate for a moment
        self.wait(2)

        # Fade in tracking elements
        self.play(
            FadeIn(number_line),
            FadeIn(arrow_tip),
        )
        self.wait(5)

        # Add velocity vector
        v_vect = spring.get_velocity_vector(color=GREEN, scale_factor=0.25)

        self.play(FadeIn(v_vect))
        self.wait(5)

        # Add force vector
        f_vect = spring.get_force_vector(color=RED, scale_factor=0.25)

        self.play(FadeIn(f_vect))
        self.wait(8)


class SpringWithGraph(InteractiveScene):
    """
    Spring-mass system with real-time x(t) graph plotting.
    Shows how position evolves over time.
    """

    def construct(self):
        # Create spring
        spring = SpringMassSystem(
            x0=2,
            mu=0.2,
            k=4,
            equilibrium_position=3 * LEFT + DOWN,
            equilibrium_length=4,
        )

        # Create axes for position-time graph
        axes = Axes(
            x_range=(0, 15, 1),
            y_range=(-2.5, 2.5, 1),
            width=10,
            height=3,
            axis_config={"stroke_color": GREY}
        )
        axes.next_to(spring.equilibrium_position, UP, buff=1.5)
        axes.shift(RIGHT)

        # Axis labels
        t_label = Text("Time (t)", font_size=24)
        t_label.next_to(axes.x_axis, RIGHT, buff=0.1)
        x_label = Tex("x(t)", font_size=24)
        x_label.next_to(axes.y_axis.get_top(), RIGHT, buff=0.1)

        # Time tracker
        time_tracker = ValueTracker(0)
        time_tracker.add_updater(lambda m, dt: m.increment_value(dt))

        # Tracking point for graph
        tracking_point = Point()
        tracking_point.add_updater(lambda p: p.move_to(
            axes.c2p(time_tracker.get_value(), spring.get_x())
        ))

        # Traced path creates the graph line
        position_graph = TracedPath(
            tracking_point.get_center,
            stroke_color=BLUE,
            stroke_width=3,
        )

        # Start paused to set up
        spring.pause()

        self.add(spring)
        self.play(
            FadeIn(axes),
            Write(t_label),
            Write(x_label),
        )

        # Start simulation and graphing
        self.add(tracking_point, position_graph, time_tracker)
        spring.unpause()

        # Let it run and trace
        self.wait(12)


class MultipleSprings(InteractiveScene):
    """
    Multiple springs with different parameters side by side.
    Great for comparing effects of mass, spring constant, damping.
    """

    def construct(self):
        # Create three springs with different damping
        springs = VGroup()
        damping_values = [0.0, 0.2, 0.5]
        labels_text = ["No damping", "Light damping", "Heavy damping"]
        colors = [BLUE, GREEN, RED]

        for i, (mu, label_text, color) in enumerate(zip(damping_values, labels_text, colors)):
            spring = SpringMassSystem(
                x0=1.5,
                mu=mu,
                k=4,
                equilibrium_position=4 * LEFT + (2 - i * 2) * UP,
                equilibrium_length=4,
                mass_color=color,
            )

            label = Text(label_text, font_size=24, color=color)
            label.next_to(spring.mass, RIGHT, buff=2)
            label.add_updater(lambda m, s=spring, t=label_text, c=color: m.become(
                Text(t, font_size=24, color=c).next_to(s.mass, RIGHT, buff=2)
            ))

            springs.add(spring)
            self.add(label)

        self.add(springs)
        self.wait(12)
