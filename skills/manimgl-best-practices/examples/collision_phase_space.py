"""
Phase space visualization of elastic block collisions.
Shows how conservation laws constrain the state to a circle.
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

    def get_scaled_block_velocities(self):
        return self.reflect_vect(self.get_value()[2:4])

    def get_block_velocities(self):
        return self.get_scaled_block_velocities() / self.sqrt_mass_vect

    def get_n_collisions(self):
        state = self.get_value()
        angle = math.atan2(state[1], state[0])
        return int(angle / self.theta)


class CollisionPhaseSpace(Scene):
    """
    Shows block collisions with a phase space diagram.
    The state point traces a path on a circle as collisions occur.
    """
    initial_positions = [9.5, 8]
    initial_velocities = [-1, 0]
    masses = [10, 1]
    widths = [1.0, 0.5]
    colors = [BLUE_E, LITTLE_BLOCK_COLOR]

    def construct(self):
        # Create floor and blocks (simplified)
        floor = Line(13 * LEFT / 2, 13 * RIGHT / 2)
        floor.to_edge(DOWN, buff=0.75)
        floor.set_stroke(WHITE, 2)

        blocks = self.get_blocks(floor)
        self.add(floor, blocks)

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

        # Create phase space plane
        plane = NumberPlane((-4, 4, 1), (-4, 4, 1), faded_line_ratio=1)
        plane.set_height(4.5)
        plane.to_corner(UR, buff=0.5)
        plane.axes.set_stroke(WHITE, 1)
        plane.background_lines.set_stroke(BLUE, 1, 0.5)
        plane.faded_lines.set_stroke(BLUE, 0.5, 0.25)
        self.add(plane)

        # Add axis labels
        kw = dict(t2c={"v_1": RED, "v_2": RED}, font_size=24)
        x_label = Tex("x = v_1", **kw)
        y_label = Tex("y = v_2", **kw)
        x_label.next_to(plane.x_axis.get_right(), UR, SMALL_BUFF)
        y_label.next_to(plane.y_axis.get_top(), DR, SMALL_BUFF)
        self.add(x_label, y_label)

        # Create state point tracking velocity
        marked_velocity = ValueTracker(state_tracker.get_block_velocities())
        marked_velocity.add_updater(lambda m: m.set_value(state_tracker.get_block_velocities()))
        self.add(marked_velocity)

        state_point = Group(
            TrueDot(radius=0.05).make_3d(),
            GlowDot(radius=0.2),
        )
        state_point.set_color(RED)
        state_point.add_updater(lambda m: m.move_to(plane.c2p(*marked_velocity.get_value())))
        self.add(state_point)

        # Add energy circle (ellipse before scaling)
        ellipse = Circle(radius=plane.x_axis.get_unit_size())
        ellipse.set_stroke(YELLOW, 2)
        ellipse.stretch(math.sqrt(10), 1)  # sqrt(m1/m2)
        ellipse.move_to(plane.c2p(0, 0))
        self.add(ellipse)

        # Add traced path
        traced_path = TracedPath(state_point.get_center, stroke_color=RED, stroke_width=1)
        self.add(traced_path)

        # Add collision counter
        count_label = Tex(R"\# \text{Collisions} = 0", font_size=30)
        count = count_label.make_number_changeable("0")
        count.add_updater(lambda m: m.set_value(state_tracker.get_n_collisions()))
        count_label.to_corner(UL)
        self.add(count_label)

        # Add energy equation
        ke_equation = Tex(
            R"\frac{1}{2} m_1 (v_1)^2 + \frac{1}{2}m_2 (v_2)^2 = E",
            t2c={"m_1": BLUE, "m_2": BLUE, "v_1": RED, "v_2": RED},
            font_size=28
        )
        ke_equation.next_to(count_label, DOWN, buff=0.5, aligned_edge=LEFT)
        self.add(ke_equation)

        # Run simulation
        self.play(
            time_tracker.animate.set_value(25),
            run_time=15,
            rate_func=linear,
        )
        self.wait()

    def get_blocks(self, floor):
        blocks = Group()
        for mass, color, width in zip(self.masses, self.colors, self.widths):
            block = Square()
            block.set_stroke(WHITE, 2)
            block.set_fill(color, 1)
            block.set_width(width)
            block.next_to(floor, UP, buff=0.01)
            block.mass = mass

            mass_label = Tex(R"10 \, \text{kg}", font_size=20)
            mass_label.make_number_changeable("10", edge_to_fix=RIGHT).set_value(mass)
            mass_label.next_to(block, UP, buff=SMALL_BUFF)
            block.add(mass_label)

            blocks.add(block)
        return blocks


class CirclePuzzle(Scene):
    """
    Shows the geometric puzzle: counting lines bouncing between a circle and a line.
    This is the geometric interpretation of the collision counting.
    """
    def construct(self):
        # Add axes
        axes = VGroup(Line(1.5 * LEFT, 1.5 * RIGHT), Line(UP, DOWN))
        axes.set_stroke(WHITE, 2, 0.33)
        axes.set_height(6)
        self.add(axes)

        # Add circle
        circle = Circle(radius=2.5)
        circle.set_stroke(YELLOW, 2)
        self.play(ShowCreation(circle))
        self.wait()

        # Add state point
        state_point = Group(
            TrueDot(radius=0.05).make_3d(),
            GlowDot(radius=0.2),
        )
        state_point.set_color(RED)
        state_point.move_to(circle.get_left())
        self.play(FadeIn(state_point, shift=0.5 * DR, scale=0.5))
        self.wait()

        # Add bouncing lines with slope = -sqrt(m1/m2)
        slope = -math.sqrt(10)  # For mass ratio 10:1
        lines = self.get_bounce_lines(circle, slope)

        # Animate each bounce
        count_label = Tex(R"\# \text{Bounces} = 0", font_size=36)
        count = count_label.make_number_changeable("0")
        count_label.to_corner(UL)
        self.add(count_label)

        for i, line in enumerate(lines):
            self.play(
                ShowCreation(line),
                state_point.animate.move_to(line.get_end()),
                ChangeDecimalToValue(count, i + 1),
                run_time=0.5
            )
        self.wait()

        # Show end zone
        theta = math.atan(1 / abs(slope))
        endzone_line = Line(ORIGIN, 4 * np.array([math.cos(theta), math.sin(theta), 0]))
        endzone_line.set_stroke(WHITE, 2)

        endzone = Polygon(
            endzone_line.get_end(),
            ORIGIN,
            4 * RIGHT,
        )
        endzone.set_fill(GREEN, 0.25)
        endzone.set_stroke(width=0)

        self.play(FadeIn(endzone), ShowCreation(endzone_line))
        self.wait(2)

    def get_bounce_lines(self, circle, slope, max_bounces=10):
        """Generate lines bouncing between circle and x-axis reflection"""
        lines = VGroup()
        point = circle.get_left()
        direction = np.array([1, slope, 0])
        direction = direction / np.linalg.norm(direction)

        for i in range(max_bounces):
            # Find intersection with circle or x-axis
            if i % 2 == 0:
                # Bounce off x-axis (reflect y)
                t = -point[1] / direction[1] if abs(direction[1]) > 1e-6 else 1e6
                next_point = point + t * direction
                # Check if still inside circle
                if np.linalg.norm(next_point[:2]) > circle.get_width() / 2:
                    break
            else:
                # Find circle intersection
                # Solve |point + t*direction|^2 = r^2
                r = circle.get_width() / 2
                a = direction[0]**2 + direction[1]**2
                b = 2 * (point[0] * direction[0] + point[1] * direction[1])
                c = point[0]**2 + point[1]**2 - r**2
                disc = b**2 - 4 * a * c
                if disc < 0:
                    break
                t = (-b + math.sqrt(disc)) / (2 * a)
                next_point = point + t * direction

                # Check end condition (first quadrant)
                if next_point[0] > 0 and next_point[1] > 0:
                    lines.add(Line(point, next_point).set_stroke(WHITE, 2))
                    break

            lines.add(Line(point, next_point).set_stroke(WHITE, 2))
            point = next_point

            # Reflect direction
            if i % 2 == 0:
                direction[1] = -direction[1]  # Bounce off x-axis
            else:
                # Reflect off circle (tangent)
                normal = point[:2] / np.linalg.norm(point[:2])
                normal = np.array([*normal, 0])
                direction = direction - 2 * np.dot(direction, normal) * normal

        return lines
