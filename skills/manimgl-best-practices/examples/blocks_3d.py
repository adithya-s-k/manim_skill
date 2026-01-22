"""
3D block collision simulation with floor and wall.
Demonstrates 3D scene setup with physics simulation.
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

    def get_n_collisions(self):
        state = self.get_value()
        angle = math.atan2(state[1], state[0])
        return int(angle / self.theta)


class Blocks3D(Scene):
    """
    3D visualization of colliding blocks with floor and wall.
    """
    initial_positions = [10, 7]
    initial_velocities = [-2, 0]
    masses = [100, 1]
    widths = [1.0, 0.5]
    colors = [BLUE_E, LITTLE_BLOCK_COLOR]
    floor_width = 15
    floor_depth = 6
    wall_height = 5
    block_shading = (0.5, 0.5, 0)

    def construct(self):
        # Set up 3D camera
        frame = self.frame
        frame.set_field_of_view(10 * DEGREES)
        frame.reorient(-10, 5, 0)

        # Create 3D floor and wall
        floor, wall = self.get_floor_and_wall_3d()
        self.add(floor, wall)

        # Create 3D blocks
        blocks = self.get_blocks_3d(floor)
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

        # Add collision counter (fixed to frame)
        count_label = Tex(R"\# \text{Collisions} = 0")
        count = count_label.make_number_changeable("0")
        count.add_updater(lambda m: m.set_value(state_tracker.get_n_collisions()))
        count_label.to_corner(UL)
        count_label.fix_in_frame()
        self.add(count_label)

        # Run simulation with camera movement
        self.play(
            time_tracker.animate.set_value(30),
            frame.animate.reorient(-5, 3, 0),
            run_time=15,
            rate_func=linear,
        )
        self.wait()

    def get_floor_and_wall_3d(self, buff_to_bottom=0.75, color=GREY_D, shading=(0.2, 0.2, 0.2)):
        floor = Square3D(resolution=(20, 20))
        floor.rotate(90 * DEGREES, LEFT)
        floor.set_shape(self.floor_width, 0, self.floor_depth)
        floor.to_edge(DOWN, buff=buff_to_bottom)

        wall = Square3D()
        wall.rotate(90 * DEGREES, UP)
        wall.set_shape(0, self.wall_height, self.floor_depth)
        wall.move_to(floor.get_left(), DOWN)

        result = Group(floor, wall)
        result.set_color(color)
        result.set_shading(*shading)
        result.to_corner(DL)

        return result

    def get_blocks_3d(self, floor, floor_buff=0.01):
        blocks = Group()
        for mass, color, width in zip(self.masses, self.colors, self.widths):
            # Create 3D cube body
            body = Cube()
            body.set_color(color)
            body.set_shading(*self.block_shading)

            # Add wireframe shell
            shell = VCube()
            shell.set_fill(opacity=0)
            shell.set_stroke(WHITE, width=1)
            shell.replace(body)
            shell.apply_depth_test()

            block = Group(body, shell)
            block.set_width(width)
            block.next_to(floor, UP, buff=floor_buff)
            block.mass = mass

            # Mass label
            mass_label = Tex(R"10 \, \text{kg}", font_size=24)
            mass_label.make_number_changeable("10", edge_to_fix=RIGHT).set_value(mass)
            mass_label.next_to(block, UP, buff=SMALL_BUFF)
            mass_label.set_backstroke(BLACK, 1)
            block.add(mass_label)
            block.mass_label = mass_label

            blocks.add(block)
        return blocks


class PreviewClip3D(Blocks3D):
    """
    Cinematic preview shot with camera movement.
    """
    initial_velocities = [-0.75, 0]
    masses = [100, 1]
    widths = [2.0, 0.5]
    initial_positions = [10, 7]
    floor_depth = 2
    wall_height = 2

    def construct(self):
        frame = self.frame
        frame.set_field_of_view(15 * DEGREES)

        # Create scene
        floor, wall = self.get_floor_and_wall_3d()
        self.add(floor, wall)

        blocks = self.get_blocks_3d(floor)
        self.add(blocks)

        state_tracker = StateTracker(blocks, self.initial_positions, self.initial_velocities)
        time_tracker = ValueTracker(0)
        state_tracker.add_updater(lambda m: m.set_time(time_tracker.get_value()))

        min_x = floor.get_x(LEFT) + blocks[1].get_width()

        def update_blocks(blocks):
            pos = state_tracker.get_block_positions()
            blocks[0].set_x(min_x + pos[0], LEFT)
            blocks[1].set_x(min_x + pos[1], RIGHT)

        blocks.add_updater(update_blocks)
        self.add(state_tracker, time_tracker)

        # Counter
        count_label = Tex(R"\# \text{Collisions} = 0")
        count = count_label.make_number_changeable("0")
        count.add_updater(lambda m: m.set_value(state_tracker.get_n_collisions()))
        count_label.to_corner(UL)
        count_label.fix_in_frame()
        self.add(count_label)

        # Start with dramatic angle
        frame.reorient(-46, -6, 0, (0.41, -2.47, 1.07), 3.59)

        # Automatic time update
        time_tracker.add_updater(lambda m, dt: m.increment_value(dt))

        # Cinematic camera movements
        self.play(
            frame.animate.reorient(-46, -4, 0, (-0.78, -2.2, -0.17), 5.41),
            run_time=8
        )
        self.play(
            frame.animate.reorient(-4, -4, 0, (-2.38, -1.95, -0.99), 6.58),
            run_time=12,
        )
        self.wait()
