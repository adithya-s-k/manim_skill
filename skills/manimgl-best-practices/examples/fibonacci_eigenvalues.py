"""
Fibonacci Eigenvalues
=====================
Shows how eigenvalues/eigenvectors lead to the closed-form Fibonacci formula.
This is a classic application of diagonalization in linear algebra.

Key concepts:
- Fibonacci recurrence as matrix multiplication
- Golden ratio as eigenvalue
- Binet's formula derivation
"""

from manimlib import *


class FibonacciEigenvalues(Scene):
    """
    Derives the closed-form Fibonacci formula using eigenvalues.
    F_n = (phi^n - psi^n) / sqrt(5)
    """

    def construct(self):
        # Title
        title = Text("Fibonacci via Eigenvalues", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))

        # Fibonacci recurrence
        recurrence = Tex(
            R"F_{n+1} = F_n + F_{n-1}",
            font_size=40
        )
        recurrence.next_to(title, DOWN, buff=0.6)

        self.play(Write(recurrence))
        self.wait()

        # Matrix form
        matrix_form = Tex(
            R"\begin{bmatrix} F_{n+1} \\ F_n \end{bmatrix} = "
            R"\begin{bmatrix} 1 & 1 \\ 1 & 0 \end{bmatrix}"
            R"\begin{bmatrix} F_n \\ F_{n-1} \end{bmatrix}",
            font_size=36
        )
        matrix_form.next_to(recurrence, DOWN, buff=0.5)

        self.play(Write(matrix_form))
        self.wait()

        # Label the matrix
        a_label = Tex(R"A", font_size=36, color=BLUE)
        a_label.next_to(matrix_form[10:16], UP, buff=0.1)

        self.play(FadeIn(a_label, shift=DOWN * 0.2))
        self.wait()

        # Clear and show eigenvalue calculation
        self.play(
            FadeOut(recurrence),
            FadeOut(matrix_form),
            FadeOut(a_label),
        )

        # Characteristic equation
        char_title = Text("Find eigenvalues:", font_size=32)
        char_title.next_to(title, DOWN, buff=0.5)

        char_eq = Tex(
            R"\det(A - \lambda I) = 0",
            font_size=36
        )
        char_eq.next_to(char_title, DOWN, buff=0.3)

        expanded = Tex(
            R"\det\begin{bmatrix} 1-\lambda & 1 \\ 1 & -\lambda \end{bmatrix} = 0",
            font_size=36
        )
        expanded.next_to(char_eq, DOWN, buff=0.3)

        polynomial = Tex(
            R"\lambda^2 - \lambda - 1 = 0",
            font_size=36
        )
        polynomial.next_to(expanded, DOWN, buff=0.3)

        self.play(Write(char_title))
        self.play(Write(char_eq))
        self.wait(0.5)
        self.play(Write(expanded))
        self.wait(0.5)
        self.play(Write(polynomial))
        self.wait()

        # Show eigenvalues (golden ratio!)
        eigenvalues = Tex(
            R"\lambda_1 = \phi = \frac{1 + \sqrt{5}}{2}, \quad "
            R"\lambda_2 = \psi = \frac{1 - \sqrt{5}}{2}",
            font_size=32,
            t2c={R"\phi": TEAL, R"\psi": YELLOW, R"\lambda_1": TEAL, R"\lambda_2": YELLOW}
        )
        eigenvalues.next_to(polynomial, DOWN, buff=0.5)

        golden_note = Text("(Golden Ratio!)", font_size=24, color=TEAL)
        golden_note.next_to(eigenvalues, DOWN, buff=0.2)

        self.play(Write(eigenvalues))
        self.play(FadeIn(golden_note, shift=UP * 0.2))
        self.wait()

        # Clear and show final formula
        self.play(
            FadeOut(char_title),
            FadeOut(char_eq),
            FadeOut(expanded),
            FadeOut(polynomial),
            FadeOut(golden_note),
            eigenvalues.animate.next_to(title, DOWN, buff=0.5)
        )

        # Binet's formula
        binet_title = Text("Binet's Formula:", font_size=32)
        binet_title.next_to(eigenvalues, DOWN, buff=0.5)

        binet = Tex(
            R"F_n = \frac{\phi^n - \psi^n}{\sqrt{5}}",
            font_size=48,
            t2c={R"\phi": TEAL, R"\psi": YELLOW}
        )
        binet.next_to(binet_title, DOWN, buff=0.3)

        # Box around final formula
        box = SurroundingRectangle(binet, buff=0.2, color=BLUE)

        self.play(Write(binet_title))
        self.play(Write(binet))
        self.play(ShowCreation(box))
        self.wait()

        # Note about psi
        note = Tex(
            R"\text{Since } |\psi| < 1, \text{ for large } n: \quad "
            R"F_n \approx \frac{\phi^n}{\sqrt{5}}",
            font_size=28
        )
        note.next_to(box, DOWN, buff=0.5)

        self.play(Write(note))
        self.wait(2)


class FibonacciVisualization(Scene):
    """
    Visual representation of Fibonacci spiral with golden ratio.
    """

    def construct(self):
        # Create Fibonacci squares
        fibs = [1, 1, 2, 3, 5, 8, 13]
        scale = 0.15

        squares = VGroup()
        current_pos = ORIGIN
        directions = [RIGHT, UP, LEFT, DOWN]  # Spiral pattern

        for i, f in enumerate(fibs):
            sq = Square(side_length=f * scale)
            sq.set_stroke(BLUE, 2)
            sq.set_fill(BLUE, 0.2)

            if i == 0:
                sq.move_to(current_pos)
            else:
                direction = directions[(i - 1) % 4]
                prev_sq = squares[-1]
                sq.next_to(prev_sq, direction, buff=0)
                # Adjust position based on size difference
                if direction == RIGHT or direction == LEFT:
                    sq.align_to(prev_sq, DOWN if i % 2 == 1 else UP)
                else:
                    sq.align_to(prev_sq, LEFT if (i - 1) % 4 < 2 else RIGHT)

            # Add number label
            label = Tex(str(f), font_size=max(12, f * 3))
            label.move_to(sq)
            sq.add(label)

            squares.add(sq)

        squares.center()
        squares.set_height(5)

        title = Text("Fibonacci Spiral", font_size=42)
        title.to_edge(UP)

        golden_ratio = Tex(
            R"\phi = \frac{1+\sqrt{5}}{2} \approx 1.618",
            font_size=32
        )
        golden_ratio.to_edge(DOWN)

        self.play(Write(title))
        self.play(
            LaggedStartMap(FadeIn, squares, lag_ratio=0.3),
            run_time=3
        )
        self.play(Write(golden_ratio))
        self.wait(2)
