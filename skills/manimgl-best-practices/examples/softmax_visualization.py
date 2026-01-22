"""
Softmax function visualization showing probability distributions.
Demonstrates: BarChart, DecimalNumber, animations for probability concepts
"""
from manimlib import *
import numpy as np


def softmax(logits, temperature=1.0):
    """Compute softmax with optional temperature parameter."""
    logits = np.array(logits)
    logits = logits - np.max(logits)  # For numerical stability
    if temperature == 0:
        result = np.zeros_like(logits, dtype=float)
        result[np.argmax(logits)] = 1
        return result
    exps = np.exp(logits / temperature)
    return exps / np.sum(exps)


class SoftmaxVisualization(Scene):
    def construct(self):
        # Example data - logits for different categories
        categories = ['Cat', 'Dog', 'Bird', 'Fish', 'Rabbit', 'Hamster']
        logits = np.array([-0.8, 2.5, 0.5, 1.5, 3.4, -2.3])
        probs = softmax(logits)

        # Create bar chart
        chart = BarChart(probs, width=10, height=5)
        chart.bars.set_stroke(width=1)
        chart.to_edge(DOWN, buff=1)

        # Add category labels
        labels = VGroup()
        for word, bar in zip(categories, chart.bars):
            label = Text(word, font_size=30)
            label.next_to(bar, DOWN)
            labels.add(label)

        # Add probability values above bars
        prob_labels = VGroup()
        for p, bar in zip(probs, chart.bars):
            label = DecimalNumber(p, num_decimal_places=3, font_size=24)
            label.next_to(bar, UP, buff=0.1)
            prob_labels.add(label)

        # Title
        title = Text("Softmax: Converting Logits to Probabilities", font_size=48)
        title.to_edge(UP)

        # Animate
        self.play(FadeIn(title))
        self.wait(0.5)

        # Show logits first
        logit_text = Text("Input logits:", font_size=36)
        logit_values = VGroup(*(
            DecimalNumber(v, include_sign=True, font_size=30)
            for v in logits
        ))
        logit_values.arrange(RIGHT, buff=0.5)
        logit_group = VGroup(logit_text, logit_values)
        logit_group.arrange(RIGHT, buff=0.5)
        logit_group.next_to(title, DOWN)

        self.play(FadeIn(logit_group))
        self.wait()

        # Animate bars growing
        chart.save_state()
        for bar in chart.bars:
            bar.stretch(0, 1, about_edge=DOWN)
        chart.set_opacity(0)

        self.play(
            Restore(chart, lag_ratio=0.1),
            LaggedStartMap(FadeIn, labels),
            run_time=2
        )
        self.play(LaggedStartMap(FadeIn, prob_labels, shift=0.2 * UP))
        self.wait()

        # Show constraint: sum = 1
        sum_text = Tex(R"\sum p_i = 1", font_size=48)
        sum_text.next_to(chart, RIGHT, buff=1)
        self.play(Write(sum_text))
        self.wait()

        # Show line at p=1
        one_line = DashedLine(
            chart.c2p(0, 1),
            chart.c2p(len(categories), 1),
        )
        one_line.set_stroke(RED, 2)

        self.play(ShowCreation(one_line))
        self.wait()

        # Demonstrate temperature effect
        self.play(
            FadeOut(one_line),
            FadeOut(sum_text),
            FadeOut(logit_group),
        )

        temp_label = VGroup(
            Text("Temperature T = ", font_size=36),
            DecimalNumber(1.0, font_size=36)
        )
        temp_label.arrange(RIGHT)
        temp_label.next_to(title, DOWN)
        temp_tracker = ValueTracker(1.0)
        temp_label[1].f_always.set_value(temp_tracker.get_value)

        self.play(FadeIn(temp_label))
        self.wait()

        # Update function for bars
        def update_chart(chart):
            t = temp_tracker.get_value()
            new_probs = softmax(logits, t)
            for bar, p, label in zip(chart.bars, new_probs, prob_labels):
                target_height = p * chart.y_axis.get_unit_size()
                bar.set_height(max(target_height, 0.01), stretch=True, about_edge=DOWN)
                label.set_value(p)
                label.next_to(bar, UP, buff=0.1)

        chart.add_updater(update_chart)
        prob_labels.add_updater(lambda m: None)  # Keep visible

        # Vary temperature
        self.play(temp_tracker.animate.set_value(0.5), run_time=3)
        self.wait()
        self.play(temp_tracker.animate.set_value(2.0), run_time=3)
        self.wait()
        self.play(temp_tracker.animate.set_value(0.1), run_time=3)
        self.wait()

        # Low temperature = more confident
        confident_text = Text("Low T = More confident", font_size=30, color=YELLOW)
        confident_text.next_to(chart, RIGHT)
        self.play(FadeIn(confident_text))
        self.wait()

        self.play(temp_tracker.animate.set_value(5.0), run_time=3)
        self.play(FadeOut(confident_text))

        uniform_text = Text("High T = More uniform", font_size=30, color=YELLOW)
        uniform_text.next_to(chart, RIGHT)
        self.play(FadeIn(uniform_text))
        self.wait(2)
