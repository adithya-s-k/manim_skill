"""
Visualization of max(rand(), rand()) process with animated tracking dots.
Shows how the maximum of two random uniform values behaves over time.
"""
from manimlib import *
import random


class Randomize(Animation):
    """Animation that randomizes a ValueTracker's value at a given frequency."""
    def __init__(self, value_tracker, frequency=8, rand_func=random.random, final_value=None, **kwargs):
        self.value_tracker = value_tracker
        self.rand_func = rand_func
        self.frequency = frequency
        self.final_value = final_value if final_value is not None else rand_func()
        self.last_alpha = 0
        self.running_tally = 0
        super().__init__(value_tracker, **kwargs)

    def interpolate_mobject(self, alpha):
        if not self.new_step(alpha):
            return
        value = self.rand_func() if alpha < 1 else self.final_value
        self.value_tracker.set_value(value)

    def new_step(self, alpha):
        d_alpha = alpha - self.last_alpha
        self.last_alpha = alpha
        self.running_tally += self.frequency * d_alpha * self.run_time
        if self.running_tally > 1:
            self.running_tally = self.running_tally % 1
            return True
        return False


class TrackingDots(Animation):
    """Animation that leaves a trail of fading dots at specified positions."""
    def __init__(self, point_func, fade_factor=0.95, radius=0.25, color=YELLOW, **kwargs):
        self.point_func = point_func
        self.fade_factor = fade_factor
        self.dots = GlowDot(point_func(), color=color, radius=radius)
        kwargs.update(remover=True)
        super().__init__(self.dots, **kwargs)

    def interpolate_mobject(self, alpha):
        opacities = self.dots.get_opacities()
        point = self.point_func()
        if not np.isclose(self.dots.get_end(), point).all():
            self.dots.add_point(point)
            opacities = np.hstack([opacities, [1]])
        opacities *= self.fade_factor
        self.dots.set_opacity(opacities)


def get_random_var_label_group(axis, label_name, color=GREY, initial_value=None, font_size=36, direction=None):
    """Create a group with a tracker, arrow tip indicator, and label for a random variable on an axis."""
    if initial_value is None:
        initial_value = random.uniform(*axis.x_range[:2])
    tracker = ValueTracker(initial_value)
    tip = ArrowTip(angle=90 * DEGREES)
    tip.set_height(0.15)
    tip.set_fill(color)
    tip.rotate(-axis.get_angle())
    if direction is None:
        direction = np.round(rotate_vector(UP, -axis.get_angle()), 1)
    tip.add_updater(lambda m: m.move_to(axis.n2p(tracker.get_value()), direction))
    label = Tex(label_name, font_size=font_size)
    label.set_color(color)
    label.set_backstroke(BLACK, 5)
    label.always.next_to(tip, -direction, buff=0.1)
    return Group(tracker, tip, label)


class MaxRandomProcess(InteractiveScene):
    """
    Visualizes the max(rand(), rand()) process.

    Shows three intervals:
    - x1 = rand() (blue)
    - x2 = rand() (yellow)
    - max(x1, x2) (green)

    Animated tracking dots show the distribution of values over time.
    """
    def construct(self):
        # Set up intervals
        intervals = VGroup(UnitInterval() for _ in range(3))
        intervals.set_width(3)
        intervals.arrange(DOWN, buff=2.5)
        intervals.shift(2 * LEFT)
        intervals[1].shift(0.5 * UP)
        for interval in intervals:
            interval.add_numbers(np.arange(0, 1.1, 0.2), font_size=16, buff=0.1, direction=UP)
            interval.numbers.set_opacity(0.75)

        colors = [BLUE, YELLOW, GREEN]
        x1_group, x2_group, max_group = groups = Group(
            get_random_var_label_group(interval, "", color=color)
            for interval, color in zip(intervals, colors)
        )
        x1_tracker, x1_tip, x1_label = x1_group
        x2_tracker, x2_tip, x2_label = x2_group
        max_tracker, max_tip, max_label = max_group
        max_tracker.add_updater(lambda m: m.set_value(max(x1_tracker.get_value(), x2_tracker.get_value())))

        self.add(intervals)
        self.add(groups)

        # Add labels
        tex_to_color = {"x_1": BLUE, "x_2": YELLOW}
        labels = VGroup(
            Tex(tex + R"\rightarrow 0.00", t2c=tex_to_color)
            for tex in [
                R"x_1 = \text{rand}()",
                R"x_2 = \text{rand}()",
                R"\max(x_1, x_2)",
            ]
        )
        for label, group, interval in zip(labels, groups, intervals):
            label.next_to(interval, RIGHT, buff=0.5)
            num = label.make_number_changeable("0.00")
            num.tracker = group[0]
            num.add_updater(lambda m: m.set_value(m.tracker.get_value()))

        self.add(labels)

        # Add rectangles
        top_rect = SurroundingRectangle(intervals[:2], buff=0.25)
        top_rect.stretch(1.1, 1)
        top_rect.set_stroke(WHITE, 2)
        top_rect.set_fill(GREY_E, 1)

        arrow = Vector(1.5 * DOWN, thickness=5)
        arrow.next_to(top_rect, DOWN)
        arrow_label = Text("max", font_size=60)
        arrow_label.next_to(arrow, RIGHT)

        self.add(top_rect, intervals, groups)
        self.add(arrow, arrow_label)

        # Line connecting max to its source
        def get_line():
            x1 = x1_tracker.get_value()
            x2 = x2_tracker.get_value()
            tip = x1_tip if x1 > x2 else x2_tip
            line = DashedLine(max_tip.get_top(), tip.get_top())
            line.set_stroke(GREY, 2, opacity=0.5)
            return line

        line = always_redraw(get_line)
        self.add(line)

        # Animate the random process
        self.play(
            Randomize(x1_tracker, frequency=4, run_time=15),
            Randomize(x2_tracker, frequency=4, run_time=15),
            TrackingDots(x1_tip.get_top, color=BLUE),
            TrackingDots(x2_tip.get_top, color=YELLOW),
            TrackingDots(max_tip.get_top, color=GREEN),
        )
