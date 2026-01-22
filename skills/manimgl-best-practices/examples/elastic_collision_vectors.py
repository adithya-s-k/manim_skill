"""
Elastic collision visualization with velocity vectors and conservation equations.
Shows how kinetic energy and momentum are conserved during collisions.
Based on the famous 3b1b pi-computing collision video.
"""
from manimlib import *
import math


LITTLE_BLOCK_COLOR = "#51463E"


class StateTracker(ValueTracker):
    """
    Tracks the state of the block collision process.
    """

    def __init__(self, blocks, initial_positions=[8, 5], initial_velocities=[-1, 0]):
        sqrt_m1, sqrt_m2 = self.sqrt_mass_vect = np.sqrt([b.mass for b in blocks])
        self.theta = math.atan2(sqrt_m2, sqrt_m1)

        self.state0 = np.array([
            *np.array(initial_positions) * self.sqrt_mass_vect,
            *np.array(initial_velocities) * self.sqrt_mass_vect,
        ])

        super().__init__(self.state0.copy())

    def set_time(self, t):
        pos0 = self.state0[0:2]
        vel0 = self.state0[2:4]
        self.set_value([*(pos0 + t * vel0), *vel0])

    def rotate_2d(self, vect, angle):
        c, s = math.cos(angle), math.sin(angle)
        return np.array([c * vect[0] - s * vect[1], s * vect[0] + c * vect[1]])

    def reflect_vect(self, vect):
        n_reflections = self.get_n_collisions()
        rot_angle = -2 * self.theta * ((n_reflections + 1) // 2)
        result = self.rotate_2d(vect, rot_angle)
        result[1] *= (-1)**(n_reflections % 2)
        return result

    def get_block_positions(self):
        scaled_pos = self.get_value()[0:2]
        rot_scaled_pos = self.reflect_vect(scaled_pos)
        return rot_scaled_pos / self.sqrt_mass_vect

    def get_block_velocities(self):
        return self.reflect_vect(self.get_value()[2:4]) / self.sqrt_mass_vect

    def get_kinetic_energy(self):
        v1, v2 = self.get_value()[2:4]
        return v1**2 + v2**2

    def get_momentum(self):
        v1, v2 = self.get_block_velocities()
        m1, m2 = self.sqrt_mass_vect**2
        return m1 * v1 + m2 * v2

    def get_n_collisions(self):
        state = self.get_value()
        angle = math.atan2(state[1], state[0])
        return int(angle / self.theta)


class ElasticCollisionVectors(Scene):
    """
    Visualization of elastic collision with velocity vectors.
    Shows conservation of kinetic energy and momentum.
    """
    initial_positions = [10.5, 8]
    initial_velocities = [-0.975, 0]
    masses = [10, 1]
    widths = [1.0, 0.5]
    colors = [BLUE_E, LITTLE_BLOCK_COLOR]

    def construct(self):
        # Create floor and wall
        floor, wall = self.get_floor_and_wall()
        self.add(floor, wall)

        # Create blocks
        blocks = self.get_blocks(floor)
        self.add(blocks)

        # Set up state tracking
        state_tracker = StateTracker(blocks, self.initial_positions, self.initial_velocities)
        time_tracker = ValueTracker(0)
        state_tracker.add_updater(lambda m: m.set_time(time_tracker.get_value()))

        # Bind blocks to state
        min_x = floor.get_x(LEFT) + blocks[1].get_width()

        def update_blocks(blocks):
            pos = state_tracker.get_block_positions()
            blocks[0].set_x(min_x + pos[0], LEFT)
            blocks[1].set_x(min_x + pos[1], RIGHT)

        blocks.add_updater(update_blocks)
        self.add(state_tracker, time_tracker)

        # Set up equations
        kw = dict(t2c={
            "m_1": BLUE,
            "m_2": BLUE,
            "v_1": RED,
            "v_2": RED,
        })
        ke_equation = Tex(R"\frac{1}{2} m_1 (v_1)^2 + \frac{1}{2}m_2 (v_2)^2 = E", **kw)
        p_equation = Tex(R"m_1 v_1 + m_2 v_2 = P", **kw)
        equations = VGroup(ke_equation, p_equation)
        equations.arrange(DOWN, buff=0.5)
        equations.to_corner(UL, buff=0.5)
        self.add(equations)

        # Create velocity vectors
        velocity_vectors = VGroup(
            self.get_velocity_vector(blocks[0], lambda: state_tracker.get_block_velocities()[0]),
            self.get_velocity_vector(blocks[1], lambda: state_tracker.get_block_velocities()[1]),
        )
        self.add(velocity_vectors)

        # Add collision counter
        count_label = Tex(R"\# \text{Collisions} = 0", font_size=36)
        count = count_label.make_number_changeable("0")
        count.add_updater(lambda m: m.set_value(state_tracker.get_n_collisions()))
        count_label.next_to(equations, DOWN, buff=0.5, aligned_edge=LEFT)
        self.add(count_label)

        # Run simulation
        self.play(
            time_tracker.animate.set_value(12),
            run_time=12,
            rate_func=linear,
        )
        self.wait()

        # Show changing velocities
        dec_equation = Tex(R"\frac{1}{2}(10)(+0.00)^2 + \frac{1}{2}(1)(+0.00)^2 = +0.00", font_size=36)
        terms = dec_equation.make_number_changeable("+0.00", replace_all=True, include_sign=True)
        dec_equation.next_to(ke_equation, DOWN, LARGE_BUFF)
        dec_equation["(1)"].set_color(BLUE)
        dec_equation["(10)"].set_color(BLUE)
        terms[:2].set_color(RED)
        terms[0].add_updater(lambda m: m.set_value(state_tracker.get_block_velocities()[0]))
        terms[1].add_updater(lambda m: m.set_value(state_tracker.get_block_velocities()[1]))
        terms[2].set_value(state_tracker.get_kinetic_energy())

        self.add(dec_equation)

        self.play(
            time_tracker.animate.increment_value(10),
            run_time=10,
            rate_func=linear,
        )
        self.wait()

    def get_floor_and_wall(self, width=13, height=2, stroke_width=2, buff_to_bottom=0.75):
        floor = Line(LEFT, RIGHT)
        floor.set_width(width)
        floor.to_edge(DOWN, buff=buff_to_bottom)
        dl_point = floor.get_left()

        wall = Line(ORIGIN, UP)
        wall.set_height(height)
        wall.move_to(dl_point, DOWN)

        ticks = VGroup()
        tick_spacing = 0.5
        tick_vect = 0.25 * DL
        for y in np.arange(tick_spacing, height + tick_spacing, tick_spacing):
            start = dl_point + y * UP
            ticks.add(Line(start, start + tick_vect))

        result = VGroup(floor, VGroup(wall, ticks))
        result.set_stroke(WHITE, stroke_width)
        return result

    def get_blocks(self, floor):
        blocks = Group()
        for mass, color, width in zip(self.masses, self.colors, self.widths):
            block = Square()
            block.set_stroke(WHITE, 2)
            block.set_fill(color, 1)
            block.set_width(width)
            block.next_to(floor, UP, buff=0.01)
            block.mass = mass

            mass_label = Tex(R"10 \, \text{kg}", font_size=24)
            mass_label.make_number_changeable("10", edge_to_fix=RIGHT).set_value(mass)
            mass_label.next_to(block, UP, buff=SMALL_BUFF)
            block.add(mass_label)
            block.mass_label = mass_label

            blocks.add(block)
        return blocks

    def get_velocity_vector(
        self,
        block,
        vel_function,
        scale_factor=0.5,
        max_width=1.0,
    ):
        """Create a velocity vector that follows a block."""
        vector = Vector(RIGHT, thickness=2)
        vector.set_fill(RED)
        vector.set_backstroke(BLACK, 1)

        def update_vector(vector):
            start = block.get_top() + 0.1 * UP
            vel = vel_function()
            width = max_width * math.tanh(scale_factor * abs(vel))
            if width > 0.05:
                direction = RIGHT if vel > 0 else LEFT
                vector.put_start_and_end_on(start, start + width * direction)
                vector.set_opacity(1)
            else:
                vector.set_opacity(0)
            return vector

        vector.add_updater(update_vector)

        label = DecimalNumber(0, num_decimal_places=2, font_size=18)
        label.set_fill(RED)
        label.set_backstroke(BLACK, 1)
        label.add_updater(lambda m: m.set_value(vel_function()).next_to(
            vector.get_start(), UP, buff=0.1
        ))

        return VGroup(vector, label)


class MomentumConservation(ElasticCollisionVectors):
    """
    Focuses on momentum conservation visualization.
    """

    def construct(self):
        # Create floor and wall
        floor, wall = self.get_floor_and_wall()
        self.add(floor, wall)

        # Create blocks
        blocks = self.get_blocks(floor)
        self.add(blocks)

        # Set up state tracking
        state_tracker = StateTracker(blocks, self.initial_positions, self.initial_velocities)
        time_tracker = ValueTracker(0)
        state_tracker.add_updater(lambda m: m.set_time(time_tracker.get_value()))

        # Bind blocks to state
        min_x = floor.get_x(LEFT) + blocks[1].get_width()

        def update_blocks(blocks):
            pos = state_tracker.get_block_positions()
            blocks[0].set_x(min_x + pos[0], LEFT)
            blocks[1].set_x(min_x + pos[1], RIGHT)

        blocks.add_updater(update_blocks)
        self.add(state_tracker, time_tracker)

        # Momentum equation
        kw = dict(t2c={"m_1": BLUE, "m_2": BLUE, "v_1": RED, "v_2": RED})
        p_equation = Tex(R"m_1 v_1 + m_2 v_2 = P", **kw)
        p_equation.to_corner(UL)
        self.add(p_equation)

        # Numerical momentum
        p_dec_equation = Tex(R"(10)(+0.00) + (1)(+0.00) = +0.00", font_size=42)
        p_terms = p_dec_equation.make_number_changeable("+0.00", replace_all=True, include_sign=True)
        p_terms[:2].set_color(RED)
        p_dec_equation["(1)"].set_color(BLUE)
        p_dec_equation["(10)"].set_color(BLUE)
        p_dec_equation.next_to(p_equation, DOWN, buff=0.75)

        p_terms[0].add_updater(lambda m: m.set_value(state_tracker.get_block_velocities()[0]))
        p_terms[1].add_updater(lambda m: m.set_value(state_tracker.get_block_velocities()[1]))
        p_terms[2].add_updater(lambda m: m.set_value(state_tracker.get_momentum()))

        # Velocity vectors
        velocity_vectors = VGroup(
            self.get_velocity_vector(blocks[0], lambda: state_tracker.get_block_velocities()[0]),
            self.get_velocity_vector(blocks[1], lambda: state_tracker.get_block_velocities()[1]),
        )
        self.add(velocity_vectors)

        # Counter
        count_label = Tex(R"\# \text{Collisions} = 0", font_size=36)
        count = count_label.make_number_changeable("0")
        count.add_updater(lambda m: m.set_value(state_tracker.get_n_collisions()))
        count_label.next_to(p_dec_equation, DOWN, buff=0.5, aligned_edge=LEFT)
        self.add(count_label)

        self.add(p_dec_equation)

        # Run simulation
        self.play(
            time_tracker.animate.set_value(20),
            run_time=15,
            rate_func=linear,
        )
        self.wait()
