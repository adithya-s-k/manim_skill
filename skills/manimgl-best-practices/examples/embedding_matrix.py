"""
Embedding Matrix Visualization
Shows how words map to vectors via an embedding matrix lookup.

Based on: videos/_2024/transformers/embedding.py - IntroduceEmbeddingMatrix
"""
from manimlib import *


class EmbeddingMatrixScene(InteractiveScene):
    """
    Visualizes the embedding matrix concept:
    - Words as columns
    - Each column is a word's vector representation
    """

    def construct(self):
        # Sample vocabulary
        words = [
            'aah', 'aardvark', 'aardwolf', 'aargh', 'ab',
            'aback', 'abacterial', 'abacus', 'abalone', 'abandon',
            'zygoid', 'zygomatic', 'zygomorphic', 'zygosis', 'zygote',
            'zygotic', 'zyme', 'zymogen', 'zymosis', 'zzz'
        ]

        # Create word list
        dots = Tex(R"\vdots")
        shown_words = VGroup(
            *map(Text, words[:10]),
            dots,
            *map(Text, words[-10:]),
        )
        shown_words.arrange(DOWN, aligned_edge=LEFT)
        dots.match_x(shown_words[:5])
        shown_words.set_height(FRAME_HEIGHT - 1)
        shown_words.move_to(LEFT)
        shown_words.set_fill(border_width=0)

        brace = Brace(shown_words, RIGHT)
        brace_text = brace.get_tex(R"\text{All words}")

        # Animate words appearing
        self.play(
            LaggedStartMap(FadeIn, shown_words, shift=0.5 * LEFT, lag_ratio=0.1, run_time=2),
            GrowFromCenter(brace, time_span=(0.5, 2.0)),
            FadeIn(brace_text, time_span=(0.5, 1.5)),
        )
        self.wait()

        # Create embedding matrix
        dots_index = shown_words.submobjects.index(dots)
        matrix = WeightMatrix(
            shape=(8, len(shown_words)),
            ellipses_col=dots_index
        )
        matrix.set_width(13)
        matrix.center()
        columns = matrix.get_columns()

        matrix_name = Text("Embedding Matrix", font_size=72)
        matrix_name.next_to(matrix, DOWN, buff=0.5)

        # Transform words to matrix columns
        shown_words.target = shown_words.generate_target()
        shown_words.target.rotate(PI / 2)
        shown_words.target.next_to(matrix, UP)
        for word, column in zip(shown_words.target, columns):
            word.match_x(column)
            word.rotate(-45 * DEGREES, about_edge=DOWN)
        shown_words.target[dots_index].rotate(45 * DEGREES).move_to(
            shown_words.target[dots_index - 1:dots_index + 2]
        )
        new_brace = Brace(shown_words.target, UP, buff=0.0)

        # Create column highlight rectangles
        column_rects = VGroup(*(
            SurroundingRectangle(column, buff=0.05)
            for column in columns
        ))
        column_rects.set_stroke(WHITE, 1)

        # Animate matrix formation
        self.play(
            MoveToTarget(shown_words),
            brace.animate.become(new_brace),
            brace_text.animate.next_to(new_brace, UP, buff=0.1),
            LaggedStart(*(
                Write(column, lag_ratio=0.01, stroke_width=1)
                for column in columns
            ), lag_ratio=0.2, run_time=2),
            LaggedStartMap(FadeIn, matrix.get_brackets(), scale=0.5, lag_ratio=0)
        )
        self.play(Write(matrix_name, run_time=1))
        self.wait()

        # Highlight columns one by one
        last_rect = VMobject()
        for index in range(min(8, len(columns))):
            for group in shown_words, columns:
                group.target = group.generate_target()
                group.target.set_opacity(0.2)
                group.target[index].set_opacity(1)
            rect = column_rects[index]
            self.play(
                *map(MoveToTarget, [shown_words, columns]),
                FadeIn(rect),
                FadeOut(last_rect),
                run_time=0.5
            )
            last_rect = rect
            self.wait(0.25)

        # Reset opacity
        self.play(
            FadeOut(last_rect),
            shown_words.animate.set_opacity(1),
            columns.animate.set_opacity(1),
        )

        # Add matrix label W_E
        frame = self.frame
        lhs = Tex("W_E = ", font_size=72)
        lhs.next_to(matrix, LEFT)

        self.play(
            frame.animate.set_width(FRAME_WIDTH + 3, about_edge=RIGHT),
            Write(lhs)
        )
        self.wait()

        # Highlight a single word lookup
        index = words.index("aardvark")
        word = shown_words[index].copy()
        vector = VGroup(
            matrix.get_brackets()[0],
            matrix.get_columns()[index],
            matrix.get_brackets()[1],
        ).copy()

        # Animate pulling out the vector
        vector.target = vector.generate_target()
        vector.target.arrange(RIGHT, buff=0.1)
        vector.target.set_height(4)
        vector.target.move_to(3 * RIGHT + DOWN)

        word.target = word.generate_target()
        word.target.rotate(-45 * DEGREES)
        word.target.scale(2)
        word.target.next_to(vector.target, LEFT, buff=1.5)

        arrow = Arrow(word.target, vector.target)

        # Scale down matrix and show lookup
        matrix_group = VGroup(lhs, matrix, shown_words, matrix_name)
        self.play(
            matrix_group.animate.scale(0.5).to_corner(UL),
            FadeOut(brace, UP),
            FadeOut(brace_text, 0.5 * UP),
            MoveToTarget(word),
            MoveToTarget(vector),
            GrowFromPoint(arrow, word.get_center()),
            run_time=2
        )
        self.wait()

        # Add lookup label
        lookup_label = Text("Embedding Lookup", font_size=48)
        lookup_label.to_edge(DOWN)
        self.play(Write(lookup_label))
        self.wait(2)
