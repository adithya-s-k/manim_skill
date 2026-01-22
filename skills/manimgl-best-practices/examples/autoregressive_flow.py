"""
Autoregressive Flow Visualization

Demonstrates the flow of text through a transformer model,
showing how text enters and probability distributions emerge.

Run with: manimgl autoregressive_flow.py AutoregressiveFlow
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


class AutoregressiveFlow(InteractiveScene):
    """
    Shows how text flows through a transformer-like machine,
    demonstrating the autoregressive generation process.
    """

    def construct(self):
        # Create the "machine" visualization
        machine = self.get_transformer_drawing()
        machine.set_height(3.5)
        machine.to_edge(LEFT, buff=0.5)

        # Input text
        input_text = "The quick brown fox"
        text_mob = Text(input_text, font_size=32)
        text_mob.to_edge(UP, buff=1.0)
        text_mob.set_color(BLUE_B)

        # Sample predictions
        predictions = [" jumps", " ran", " leaped", " went", " moved"]
        probs = np.array([0.42, 0.28, 0.15, 0.10, 0.05])

        # Build distribution
        bar_groups = self.build_distribution(predictions, probs)
        bar_groups.next_to(machine, RIGHT, buff=1.5)
        bar_groups.align_to(machine, UP)

        # Arrows
        in_arrow = Arrow(text_mob.get_bottom(), machine[0][0].get_top(), buff=0.2)
        in_arrow.set_color(BLUE)
        out_arrow = Arrow(machine[0][-1].get_right(), bar_groups.get_left(), buff=0.3)
        out_arrow.set_color(TEAL)

        # Labels
        input_label = Text("Input Context", font_size=24)
        input_label.next_to(text_mob, LEFT)
        output_label = Text("Output\nProbabilities", font_size=24, alignment="CENTER")
        output_label.next_to(bar_groups, RIGHT)

        # Animate
        self.play(FadeIn(machine))
        self.wait(0.5)

        self.play(Write(text_mob), FadeIn(input_label))
        self.play(GrowArrow(in_arrow))

        # Animate text flowing into machine
        text_copy = text_mob.copy()
        self.play(
            text_copy.animate.scale(0.5).move_to(machine[0][0].get_top()),
            run_time=0.5
        )
        self.play(
            FadeOut(text_copy, shift=DOWN),
            self.animate_machine_processing(machine),
            run_time=1.5
        )

        # Output emerges
        self.play(GrowArrow(out_arrow))
        self.play(
            LaggedStart(
                *(FadeIn(bg, shift=RIGHT) for bg in bar_groups),
                lag_ratio=0.1,
                run_time=1.5
            ),
            FadeIn(output_label)
        )
        self.wait(2)

    def get_transformer_drawing(self):
        """Create a 3D-like stack of blocks representing the transformer."""
        blocks = VGroup(*(
            VGroup(
                Rectangle(2.5, 0.3).set_fill(GREY_D, 1).set_stroke(WHITE, 1),
            )
            for n in range(8)
        ))
        blocks.arrange(DOWN, buff=0.05)

        # Add "Transformer" label
        label = Text("Transformer", font_size=28)
        label.next_to(blocks, UP, buff=0.3)

        return VGroup(blocks, label)

    def animate_machine_processing(self, machine):
        """Animate the blocks lighting up in sequence."""
        blocks = machine[0]
        return LaggedStart(
            *(
                block[0].animate.set_fill(TEAL, 0.8).set_anim_args(
                    rate_func=there_and_back
                )
                for block in blocks
            ),
            lag_ratio=0.15,
            run_time=1.5
        )

    def build_distribution(self, words, probs, font_size=24, width_100p=2.0, bar_height=0.25):
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

        return bar_groups


class TextToMachineFlow(InteractiveScene):
    """
    Simpler version showing text entering a machine block.
    """

    def construct(self):
        # Machine box
        machine = Rectangle(3, 2)
        machine.set_fill(GREY_D, 0.8)
        machine.set_stroke(WHITE, 2)
        machine_label = Text("LLM", font_size=36)
        machine_label.move_to(machine)
        machine_group = VGroup(machine, machine_label)
        machine_group.center()

        # Input text
        input_words = ["The", "weather", "today", "is"]
        word_mobs = VGroup(*(Text(w, font_size=28) for w in input_words))
        word_mobs.arrange(RIGHT, buff=0.3)
        word_mobs.next_to(machine, UP, buff=1.5)
        word_mobs.set_color(BLUE_B)

        # Output predictions
        output_words = ["sunny", "rainy", "cloudy", "warm"]
        output_probs = [0.45, 0.25, 0.20, 0.10]
        output_mobs = VGroup()
        for word, prob in zip(output_words, output_probs):
            text = Text(f"{word}: {int(prob*100)}%", font_size=24)
            output_mobs.add(text)
        output_mobs.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        output_mobs.next_to(machine, DOWN, buff=1.0)
        output_mobs.set_color(TEAL)

        # Arrows
        in_arrow = Arrow(word_mobs.get_bottom(), machine.get_top(), buff=0.1)
        out_arrow = Arrow(machine.get_bottom(), output_mobs.get_top(), buff=0.1)

        # Animate
        self.play(FadeIn(machine_group))
        self.play(
            LaggedStart(
                *(FadeIn(w, shift=DOWN) for w in word_mobs),
                lag_ratio=0.2
            )
        )
        self.play(GrowArrow(in_arrow))

        # Words flow in
        self.play(
            LaggedStart(
                *(
                    w.animate.scale(0.3).move_to(machine.get_center())
                    for w in word_mobs.copy()
                ),
                lag_ratio=0.1
            ),
            machine.animate.set_fill(TEAL, 0.3).set_anim_args(rate_func=there_and_back),
            run_time=1.5
        )

        # Output emerges
        self.play(GrowArrow(out_arrow))
        self.play(
            LaggedStart(
                *(FadeIn(o, shift=DOWN) for o in output_mobs),
                lag_ratio=0.15
            )
        )
        self.wait(2)
