"""
Visualization of sqrt(rand()) process showing how the square root
transforms a uniform distribution.
"""
from manimlib import *
import random
import math


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


class SqrtRandomProcess(InteractiveScene):
    """
    Visualizes the sqrt(rand()) process.

    Shows two intervals:
    - x = rand() (blue)
    - sqrt(x) (teal)

    Demonstrates that sqrt(rand()) has the same distribution as max(rand(), rand()).
    """
    def construct(self):
        # Set up intervals
        intervals = VGroup(UnitInterval() for _ in range(2))
        intervals.set_width(3)
        intervals.arrange(DOWN, buff=3.5)
        intervals.shift(2 * LEFT)
        for interval in intervals:
            interval.add_numbers(np.arange(0, 1.1, 0.2), font_size=16, buff=0.1, direction=UP)
            interval.numbers.set_opacity(0.75)

        colors = [BLUE, TEAL]
        x_group, sqrt_group = groups = Group(
            get_random_var_label_group(interval, "", color=color)
            for interval, color in zip(intervals, colors)
        )
        x_tracker, x_tip, x_label = x_group
        sqrt_tracker, sqrt_tip, sqrt_label = sqrt_group
        sqrt_tracker.add_updater(lambda m: m.set_value(math.sqrt(x_tracker.get_value())))

        self.add(intervals)
        self.add(groups)

        # Add labels
        tex_to_color = {"x": BLUE}
        labels = VGroup(
            Tex(tex + R"\rightarrow 0.00", t2c=tex_to_color)
            for tex in [
                R"x = \text{rand}()",
                R"\sqrt{x}",
            ]
        )
        for label, group, interval in zip(labels, groups, intervals):
            label.next_to(interval, RIGHT, buff=0.5)
            num = label.make_number_changeable("0.00")
            num.tracker = group[0]
            num.add_updater(lambda m: m.set_value(m.tracker.get_value()))

        self.add(labels)

        # Big arrow
        arrow = Arrow(*intervals, buff=0.5, thickness=5)
        label = Text(R"sqrt", font_size=60)
        label.next_to(arrow, RIGHT)

        self.add(arrow, label)

        # Animate the random process
        self.play(
            Randomize(x_tracker, frequency=4, run_time=15),
            TrackingDots(x_tip.get_top, color=colors[0]),
            TrackingDots(sqrt_tip.get_top, color=colors[1]),
        )
