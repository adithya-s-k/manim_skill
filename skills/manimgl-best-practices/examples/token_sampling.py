"""
Token Sampling Animation

Demonstrates the random sampling process used in autoregressive generation,
where the next token is sampled from the probability distribution.

Run with: manimgl token_sampling.py TokenSamplingAnimation
"""
from manimlib import *
import numpy as np
import random


class TokenSamplingAnimation(InteractiveScene):
    """
    Shows how tokens are randomly sampled from a probability distribution.
    The highlight rectangle bounces between options before settling.
    """

    def construct(self):
        # Title
        title = Text("Sampling from Distribution", font_size=36)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))

        # Create distribution
        words = [" habitat", " environment", " forest", " home", " land"]
        probs = np.array([0.35, 0.28, 0.20, 0.12, 0.05])
        probs = probs / probs.sum()  # Normalize

        bar_groups = self.build_distribution(words, probs)
        bar_groups.center()
        bar_groups.shift(0.5 * DOWN)

        self.play(FadeIn(bar_groups, lag_ratio=0.1))
        self.wait(0.5)

        # Create highlight rectangle
        highlight = SurroundingRectangle(bar_groups[0], buff=0.05)
        highlight.set_stroke(YELLOW, 3)
        highlight.set_fill(YELLOW, 0.25)

        # Animate random sampling
        seed = random.randint(0, 1000)

        def highlight_randomly(rect, alpha):
            np.random.seed(seed + int(15 * alpha))
            index = np.random.choice(len(words), p=probs)
            rect.surround(bar_groups[index], buff=0.05)
            rect.stretch(1.05, 0)

        self.play(FadeIn(highlight))
        self.play(
            UpdateFromAlphaFunc(
                highlight,
                lambda r, a: highlight_randomly(r, a)
            ),
            run_time=2.5,
            rate_func=linear
        )

        # Final selection
        final_index = np.random.choice(len(words), p=probs)
        final_highlight = SurroundingRectangle(bar_groups[final_index], buff=0.05)
        final_highlight.set_stroke(GREEN, 4)
        final_highlight.set_fill(GREEN, 0.3)

        self.play(Transform(highlight, final_highlight))

        # Show selected word
        selected_word = Text(words[final_index].strip(), font_size=48)
        selected_word.set_color(GREEN)
        selected_word.next_to(bar_groups, RIGHT, buff=1.0)

        selected_label = Text("Selected:", font_size=28)
        selected_label.next_to(selected_word, UP)

        self.play(
            Write(selected_label),
            FadeIn(selected_word, scale=1.5)
        )
        self.wait(2)

    def build_distribution(self, words, probs, font_size=28, width_100p=4.0, bar_height=0.35):
        """Build bar chart visualization."""
        bar_groups = VGroup()
        for word, prob in zip(words, probs):
            label = Text(word, font_size=font_size)
            bar = Rectangle(prob * width_100p, bar_height)
            bar.set_fill(interpolate_color(BLUE_E, TEAL, prob / max(probs)), opacity=0.9)
            bar.set_stroke(WHITE, 1)
            prob_label = Integer(int(100 * prob), unit="%", font_size=font_size * 0.8)
            prob_label.next_to(bar, RIGHT, buff=SMALL_BUFF)
            label.next_to(bar, LEFT)
            bar_groups.add(VGroup(label, bar, prob_label))

        bar_groups.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        return bar_groups


class TemperatureSampling(InteractiveScene):
    """
    Demonstrates how temperature affects the sampling distribution.
    Higher temperature = more uniform, lower = more peaked.
    """

    def construct(self):
        def softmax(logits, temperature=1.0):
            """Compute softmax with temperature scaling."""
            logits = np.array(logits, dtype=float)
            logits = logits - np.max(logits)
            if temperature == 0:
                result = np.zeros_like(logits)
                result[np.argmax(logits)] = 1.0
                return result
            exps = np.exp(logits / temperature)
            return exps / np.sum(exps)

        # Base logits (before softmax)
        logits = np.array([2.5, 2.0, 1.5, 1.0, 0.5])
        words = ["word1", "word2", "word3", "word4", "word5"]

        # Different temperatures
        temperatures = [0.5, 1.0, 2.0]
        temp_labels = ["T = 0.5 (focused)", "T = 1.0 (normal)", "T = 2.0 (creative)"]

        # Create three distributions side by side
        dist_groups = VGroup()
        for temp, label in zip(temperatures, temp_labels):
            probs = softmax(logits, temp)
            bars = self.build_mini_distribution(probs)
            title = Text(label, font_size=22)
            title.next_to(bars, UP, buff=0.3)
            dist_groups.add(VGroup(title, bars))

        dist_groups.arrange(RIGHT, buff=1.0)
        dist_groups.center()

        # Main title
        main_title = Text("Temperature Effect on Sampling", font_size=36)
        main_title.to_edge(UP, buff=0.5)

        # Animate
        self.play(Write(main_title))
        self.play(
            LaggedStart(
                *(FadeIn(dg, shift=UP) for dg in dist_groups),
                lag_ratio=0.3
            )
        )
        self.wait()

        # Highlight differences
        arrows = VGroup()
        for i, (dg, temp) in enumerate(zip(dist_groups, temperatures)):
            if temp == 0.5:
                note = Text("More deterministic", font_size=18, color=BLUE)
            elif temp == 2.0:
                note = Text("More random", font_size=18, color=RED)
            else:
                note = Text("Balanced", font_size=18, color=GREEN)
            note.next_to(dg, DOWN, buff=0.3)
            arrows.add(note)

        self.play(FadeIn(arrows, lag_ratio=0.2))
        self.wait(2)

    def build_mini_distribution(self, probs, bar_width=1.5, bar_height=0.2):
        """Build a compact bar chart."""
        bars = VGroup()
        for prob in probs:
            bar = Rectangle(prob * bar_width, bar_height)
            bar.set_fill(interpolate_color(GREY_D, TEAL, prob), opacity=0.9)
            bar.set_stroke(WHITE, 1)
            bars.add(bar)
        bars.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        return bars
