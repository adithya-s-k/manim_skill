"""
Token Probability Distribution Visualization

Demonstrates how to visualize next-token probability distributions
as animated bar charts - a key component of autoregressive generation.

Run with: manimgl token_probability_distribution.py TokenProbabilityDistribution
"""
from manimlib import *
import numpy as np


def get_paragraph(words, line_len=40, font_size=48):
    """Handle word wrapping for text display."""
    words = list(map(str.strip, words))
    word_lens = list(map(len, words))
    lines = []
    lh, rh = 0, 0
    while rh < len(words):
        rh += 1
        if sum(word_lens[lh:rh]) > line_len:
            rh -= 1
            lines.append(words[lh:rh])
            lh = rh
    lines.append(words[lh:])
    text = "\n".join([" ".join(line).strip() for line in lines])
    return Text(text, alignment="LEFT", font_size=font_size)


class TokenProbabilityDistribution(InteractiveScene):
    """
    Visualizes a probability distribution over next tokens.
    Shows how language models output probabilities for each possible next word.
    """

    def construct(self):
        # Sample predictions with probabilities
        predictions = [" habitat", " environment", " forest", " home", " land", " world", " area"]
        probs = np.array([0.35, 0.25, 0.15, 0.10, 0.08, 0.05, 0.02])

        # Input context
        context = "Behold, a wild pi creature, foraging in its native"
        context_mob = get_paragraph(context.split(" "), line_len=35, font_size=36)
        context_mob.to_edge(UP, buff=0.5)
        context_mob.set_color(BLUE_B)

        # Next word indicator
        next_word_line = Underline(context_mob[-6:])
        next_word_line.set_stroke(TEAL, 2)
        next_word_line.next_to(context_mob[-1], RIGHT, SMALL_BUFF, aligned_edge=DOWN)

        # Build the distribution visualization
        bar_groups = self.build_distribution(predictions, probs)
        bar_groups.next_to(context_mob, DOWN, buff=1.0)
        bar_groups.shift(RIGHT)

        # Title
        title = Text("Next Token Probabilities", font_size=42)
        title.to_edge(UP, buff=0.1)
        title.set_color(YELLOW)

        # Animate
        self.play(Write(title))
        self.play(
            FadeIn(context_mob, lag_ratio=0.02),
            ShowCreation(next_word_line),
        )
        self.wait(0.5)

        # Animate bars appearing
        self.play(
            LaggedStart(
                *(FadeIn(bg, shift=LEFT) for bg in bar_groups),
                lag_ratio=0.1,
                run_time=2
            )
        )
        self.wait()

        # Highlight top prediction
        highlight = SurroundingRectangle(bar_groups[0], buff=0.05)
        highlight.set_stroke(YELLOW, 3)
        highlight.set_fill(YELLOW, 0.2)

        self.play(ShowCreation(highlight))
        self.wait()

        # Show that probabilities sum to 1
        sum_label = Tex(R"\sum P = 1", font_size=36)
        sum_label.next_to(bar_groups, RIGHT, buff=0.5)

        self.play(Write(sum_label))
        self.wait(2)

    def build_distribution(
        self,
        words,
        probs,
        font_size=24,
        width_100p=3.0,
        bar_height=0.3
    ):
        """Build bar chart visualization of token probabilities."""
        labels = VGroup(*(Text(word, font_size=font_size) for word in words))
        bars = VGroup(*(
            Rectangle(prob * width_100p, bar_height)
            for prob in probs
        ))
        bars.arrange(DOWN, aligned_edge=LEFT, buff=0.4 * bar_height)
        bars.set_fill(opacity=1)
        bars.set_submobject_colors_by_gradient(TEAL, YELLOW)
        bars.set_stroke(WHITE, 1)

        bar_groups = VGroup()
        for label, bar, prob in zip(labels, bars, probs):
            prob_label = Integer(int(100 * prob), unit="%", font_size=0.75 * font_size)
            prob_label.next_to(bar, RIGHT, buff=SMALL_BUFF)
            label.next_to(bar, LEFT)
            bar_groups.add(VGroup(label, bar, prob_label))

        # Add ellipsis to indicate more tokens
        ellipses = Tex(R"\vdots", font_size=font_size)
        ellipses.next_to(bar_groups[-1][0], DOWN)
        bar_groups.add(ellipses)

        return bar_groups


class AnimatedDistributionBars(InteractiveScene):
    """
    Shows probability distribution bars animating as context changes.
    Demonstrates how the distribution shifts based on input.
    """

    def construct(self):
        # Two different contexts
        context1 = "The cat sat on the"
        context2 = "The astronaut floated in"

        # Different probability distributions for each context
        predictions1 = [" mat", " floor", " chair", " bed", " couch"]
        probs1 = np.array([0.40, 0.25, 0.15, 0.12, 0.08])

        predictions2 = [" space", " air", " void", " capsule", " orbit"]
        probs2 = np.array([0.45, 0.20, 0.18, 0.10, 0.07])

        # Create context displays
        ctx1_mob = Text(context1, font_size=32)
        ctx1_mob.to_edge(UP, buff=1.0)
        ctx1_mob.set_color(BLUE_B)

        # Build first distribution
        bar_groups1 = self.build_simple_distribution(predictions1, probs1)
        bar_groups1.center()
        bar_groups1.shift(0.5 * DOWN)

        # Show first context and distribution
        self.play(Write(ctx1_mob))
        self.play(FadeIn(bar_groups1, lag_ratio=0.1))
        self.wait()

        # Transform to second context
        ctx2_mob = Text(context2, font_size=32)
        ctx2_mob.to_edge(UP, buff=1.0)
        ctx2_mob.set_color(GREEN_B)

        bar_groups2 = self.build_simple_distribution(predictions2, probs2)
        bar_groups2.center()
        bar_groups2.shift(0.5 * DOWN)

        self.play(
            ReplacementTransform(ctx1_mob, ctx2_mob),
            ReplacementTransform(bar_groups1, bar_groups2),
            run_time=2
        )
        self.wait(2)

    def build_simple_distribution(self, words, probs, font_size=28, width_100p=4.0, bar_height=0.4):
        """Build a simple bar chart for probabilities."""
        bar_groups = VGroup()
        for word, prob in zip(words, probs):
            label = Text(word, font_size=font_size)
            bar = Rectangle(prob * width_100p, bar_height)
            bar.set_fill(interpolate_color(RED, GREEN, prob), opacity=0.8)
            bar.set_stroke(WHITE, 1)
            prob_label = Integer(int(100 * prob), unit="%", font_size=font_size * 0.8)
            prob_label.next_to(bar, RIGHT, buff=SMALL_BUFF)
            label.next_to(bar, LEFT)
            bar_groups.add(VGroup(label, bar, prob_label))

        bar_groups.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        return bar_groups
