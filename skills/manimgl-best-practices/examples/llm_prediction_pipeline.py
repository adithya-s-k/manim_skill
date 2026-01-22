"""
LLM Prediction Pipeline Visualization

Demonstrates the complete flow of an LLM making predictions:
input context -> model processing -> probability distribution -> sampled output.

Run with: manimgl llm_prediction_pipeline.py LLMPredictionPipeline
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


class LLMPredictionPipeline(InteractiveScene):
    """
    Full visualization of the LLM prediction pipeline:
    1. Input text is shown
    2. Text flows into the model
    3. Model processes (blocks light up)
    4. Distribution appears
    5. Token is sampled and added to text
    """

    def construct(self):
        # Initial setup
        seed_text = "Michael Jordan plays the sport of"

        # Create input text
        input_text = get_paragraph(seed_text.split(), line_len=30, font_size=32)
        input_text.to_edge(UP, buff=0.8)
        input_text.set_color(BLUE_B)

        # Create model visualization
        model = self.create_llm_model()
        model.set_height(3.0)
        model.center()
        model.shift(0.5 * DOWN)

        # Create prediction data
        predictions = [" basketball", " baseball", " golf", " tennis", " football"]
        probs = np.array([0.65, 0.15, 0.08, 0.07, 0.05])

        # Distribution visualization
        bar_groups = self.build_distribution(predictions, probs)
        bar_groups.to_edge(RIGHT, buff=0.5)
        bar_groups.align_to(model, UP)

        # Input arrow
        in_arrow = Arrow(
            input_text.get_bottom() + 0.2 * DOWN,
            model.get_top() + 0.2 * UP,
            buff=0
        )
        in_arrow.set_color(BLUE)

        # Output arrow
        out_arrow = Arrow(
            model.get_right() + 0.2 * RIGHT,
            bar_groups.get_left() + 0.2 * LEFT,
            buff=0
        )
        out_arrow.set_color(TEAL)

        # Step 1: Show input
        step1 = Text("1. Input Context", font_size=24, color=YELLOW)
        step1.to_corner(UL)

        self.play(Write(step1))
        self.play(Write(input_text))
        self.wait(0.5)

        # Step 2: Feed to model
        step2 = Text("2. Feed to Model", font_size=24, color=YELLOW)
        step2.next_to(step1, DOWN, aligned_edge=LEFT)

        self.play(Write(step2))
        self.play(FadeIn(model))
        self.play(GrowArrow(in_arrow))

        # Animate text flowing into model
        text_copy = input_text.copy()
        self.play(
            text_copy.animate.scale(0.3).move_to(model.get_top()),
            rate_func=rush_into,
            run_time=0.8
        )
        self.play(FadeOut(text_copy, shift=DOWN, scale=0.5))

        # Step 3: Model processes
        step3 = Text("3. Process", font_size=24, color=YELLOW)
        step3.next_to(step2, DOWN, aligned_edge=LEFT)

        self.play(Write(step3))
        self.play(self.animate_model_processing(model))
        self.wait(0.3)

        # Step 4: Output distribution
        step4 = Text("4. Output Distribution", font_size=24, color=YELLOW)
        step4.next_to(step3, DOWN, aligned_edge=LEFT)

        self.play(Write(step4))
        self.play(GrowArrow(out_arrow))
        self.play(
            LaggedStart(
                *(FadeIn(bg, shift=LEFT) for bg in bar_groups),
                lag_ratio=0.08
            )
        )
        self.wait(0.5)

        # Step 5: Sample and add
        step5 = Text("5. Sample Token", font_size=24, color=YELLOW)
        step5.next_to(step4, DOWN, aligned_edge=LEFT)

        # Highlight top prediction
        highlight = SurroundingRectangle(bar_groups[0], buff=0.05)
        highlight.set_stroke(GREEN, 3)
        highlight.set_fill(GREEN, 0.2)

        self.play(Write(step5))
        self.play(ShowCreation(highlight))

        # Add word to text
        new_word = Text(" basketball", font_size=32)
        new_word.set_color(GREEN)
        new_word.next_to(input_text, RIGHT, buff=0.1)

        self.play(
            FadeIn(new_word, shift=LEFT, scale=1.2),
        )
        self.wait(2)

    def create_llm_model(self):
        """Create a visual representation of the LLM."""
        # Stack of blocks
        blocks = VGroup()
        for i in range(6):
            block = Rectangle(3.5, 0.35)
            block.set_fill(GREY_D, 0.9)
            block.set_stroke(WHITE, 1)
            blocks.add(block)
        blocks.arrange(DOWN, buff=0.08)

        # Label
        label = Text("Large Language Model", font_size=24)
        label.next_to(blocks, UP, buff=0.2)

        # Dials/parameters hint
        dots = VGroup()
        for block in blocks[:3]:
            row_dots = VGroup(*(
                Dot(radius=0.03).set_fill(random_bright_color(), 0.7)
                for _ in range(8)
            ))
            row_dots.arrange(RIGHT, buff=0.15)
            row_dots.move_to(block)
            dots.add(row_dots)

        return VGroup(blocks, label, dots)

    def animate_model_processing(self, model):
        """Animate the model blocks lighting up."""
        blocks = model[0]
        return LaggedStart(
            *(
                block.animate.set_fill(TEAL, 0.8).set_anim_args(
                    rate_func=there_and_back
                )
                for block in blocks
            ),
            lag_ratio=0.15,
            run_time=1.2
        )

    def build_distribution(self, words, probs, font_size=22, width_100p=2.0, bar_height=0.25):
        """Build probability distribution bars."""
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

        bar_groups.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        return bar_groups


class IterativeGeneration(InteractiveScene):
    """
    Shows multiple iterations of token generation,
    demonstrating the autoregressive nature of LLMs.
    """

    def construct(self):
        # Starting text
        tokens = ["The", " sun", " rises"]
        next_tokens = [" in", " the", " east"]

        # Display area
        text_display = VGroup()
        for token in tokens:
            t = Text(token, font_size=36)
            t.set_color(BLUE_B)
            text_display.add(t)
        text_display.arrange(RIGHT, buff=0.05)
        text_display.to_edge(UP, buff=1.5)

        # Model box (simplified)
        model_box = Rectangle(2.5, 1.5)
        model_box.set_fill(GREY_D, 0.8)
        model_box.set_stroke(WHITE, 2)
        model_label = Text("LLM", font_size=28)
        model_label.move_to(model_box)
        model = VGroup(model_box, model_label)
        model.center()

        self.play(FadeIn(text_display, lag_ratio=0.2))
        self.play(FadeIn(model))
        self.wait(0.5)

        # Generate tokens one by one
        for i, next_token in enumerate(next_tokens):
            # Arrow from text to model
            in_arrow = Arrow(
                text_display.get_bottom(),
                model.get_top(),
                buff=0.2
            )
            in_arrow.set_color(BLUE)

            # Show input flowing
            self.play(GrowArrow(in_arrow), run_time=0.4)

            # Model processes
            self.play(
                model_box.animate.set_fill(TEAL, 0.5).set_anim_args(
                    rate_func=there_and_back
                ),
                run_time=0.5
            )

            # New token emerges
            new_token = Text(next_token, font_size=36)
            new_token.set_color(GREEN)
            new_token.next_to(text_display, RIGHT, buff=0.05)

            out_arrow = Arrow(
                model.get_top(),
                new_token.get_bottom(),
                buff=0.2,
                path_arc=-60 * DEGREES
            )
            out_arrow.set_color(GREEN)

            self.play(
                GrowArrow(out_arrow),
                FadeIn(new_token, scale=1.3),
                run_time=0.6
            )

            # Add to display and clean up
            text_display.add(new_token)
            new_token.set_color(BLUE_B)

            self.play(
                FadeOut(in_arrow),
                FadeOut(out_arrow),
                run_time=0.3
            )

        # Final result
        self.wait()
        final_text = VGroup(*text_display).copy()
        final_text.generate_target()
        final_text.target.center()
        final_text.target.shift(UP)
        final_text.target.scale(1.2)

        self.play(
            FadeOut(model),
            MoveToTarget(final_text)
        )

        result_label = Text("Generated Text", font_size=28)
        result_label.next_to(final_text, DOWN, buff=0.5)
        self.play(Write(result_label))
        self.wait(2)
