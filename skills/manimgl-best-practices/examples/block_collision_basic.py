"""
Basic block collision simulation demonstrating elastic collisions.
Based on the famous 3b1b pi-computing collision video.
"""
from manimlib import *
import math


LITTLE_BLOCK_COLOR = "#51463E"


class StateTracker(ValueTracker):
    """
    Tracks the state of the block collision process as a 4d vector
    [
        x1 * sqrt(m1),
        x2 * sqrt(m2),
        v1 * sqrt(m1),
        v2 * sqrt(m2),
    ]
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
        """Simple 2D rotation helper"""
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

    def get_scaled_block_velocities(self):
        return self.reflect_vect(self.get_value()[2:4])

    def get_block_velocities(self):
        return self.get_scaled_block_velocities() / self.sqrt_mass_vect

    def get_n_collisions(self):
        state = self.get_value()
        angle = math.atan2(state[1], state[0])
        return int(angle / self.theta)


class BlockCollisionBasic(Scene):
    """
    A simplified block collision demonstration.
    Shows two blocks colliding elastically.
    """
    initial_positions = [10, 7]
    initial_velocities = [-2, 0]
    masses = [100, 1]
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

        # Add collision counter
        count_label = Tex(R"\# \text{Collisions} = 0")
        count = count_label.make_number_changeable("0")
        count.add_updater(lambda m: m.set_value(state_tracker.get_n_collisions()))
        count_label.to_corner(UL)
        self.add(count_label)

        # Run the simulation
        self.play(
            time_tracker.animate.set_value(30),
            run_time=15,
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

        # Add tick marks to wall
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


# Alternative mass ratios for counting pi digits
class BlockCollision1e4(BlockCollisionBasic):
    """Mass ratio 10000:1 gives 314 collisions"""
    masses = [10000, 1]
    widths = [1.5, 0.5]
    colors = [interpolate_color(BLUE_E, BLACK, 0.5), LITTLE_BLOCK_COLOR]


class BlockCollision1e6(BlockCollisionBasic):
    """Mass ratio 1000000:1 gives 3141 collisions"""
    masses = [1000000, 1]
    widths = [2.0, 0.5]
    colors = [interpolate_color(BLUE_E, BLACK, 0.8), LITTLE_BLOCK_COLOR]
