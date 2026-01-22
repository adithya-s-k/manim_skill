"""
Eigenvalue Equations
====================
Shows the key mathematical equations for eigenvalues and eigenvectors.
Demonstrates LaTeX typesetting with color coding for mathematical concepts.

Key concepts:
- Eigenvalue equation: Av = lambda * v
- Diagonalization: A = S * D * S^(-1)
- Change of basis transformation
"""

from manimlib import *


class EigenvalueEquations(Scene):
    """
    Displays the fundamental eigenvalue/eigenvector equations
    with proper color coding to highlight mathematical relationships.
    """

    def construct(self):
        # Title
        title = Text("Eigenvalue Equations", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))

        # Main eigenvalue equation
        eigen_eq = Tex(
            R"A \vec{\mathbf{v}} = \lambda \vec{\mathbf{v}}",
            font_size=60
        )
        eigen_eq.set_color_by_tex(R"\lambda", TEAL)
        eigen_eq.set_color_by_tex(R"\vec{\mathbf{v}}", YELLOW)

        # Description
        eigen_desc = Text(
            "Eigenvector is scaled by eigenvalue",
            font_size=28
        )
        eigen_desc.set_color(GREY_B)

        eigen_group = VGroup(eigen_eq, eigen_desc)
        eigen_group.arrange(DOWN, buff=0.3)
        eigen_group.next_to(title, DOWN, buff=0.8)

        self.play(Write(eigen_eq))
        self.play(FadeIn(eigen_desc, shift=UP * 0.3))
        self.wait()

        # Move up and show diagonalization
        self.play(
            eigen_group.animate.shift(UP * 0.5).scale(0.8)
        )

        # Diagonalization equation
        diag_eq = Tex(
            R"A = S \Lambda S^{-1}",
            font_size=48
        )
        diag_eq.set_color_by_tex(R"\Lambda", TEAL)
        diag_eq.set_color_by_tex("S", YELLOW)

        # Where clause
        where_clause = Tex(
            R"\text{where } \Lambda = "
            R"\begin{bmatrix} \lambda_1 & 0 \\ 0 & \lambda_2 \end{bmatrix}",
            font_size=36
        )
        where_clause.set_color_by_tex(R"\lambda_1", TEAL)
        where_clause.set_color_by_tex(R"\lambda_2", YELLOW)

        # S matrix explanation
        s_clause = Tex(
            R"S = \begin{bmatrix} \vert & \vert \\ "
            R"\vec{\mathbf{v}}_1 & \vec{\mathbf{v}}_2 \\ "
            R"\vert & \vert \end{bmatrix}",
            font_size=36
        )
        s_clause.set_color_by_tex(R"\vec{\mathbf{v}}_1", TEAL)
        s_clause.set_color_by_tex(R"\vec{\mathbf{v}}_2", YELLOW)

        diag_group = VGroup(diag_eq, where_clause, s_clause)
        diag_group.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        diag_group.next_to(eigen_group, DOWN, buff=0.6)

        self.play(Write(diag_eq))
        self.wait(0.5)
        self.play(FadeIn(where_clause, shift=UP * 0.2))
        self.wait(0.5)
        self.play(FadeIn(s_clause, shift=UP * 0.2))
        self.wait(2)


class DiagonalMatrixPowers(Scene):
    """
    Shows the key insight: diagonal matrices are easy to raise to powers.
    This makes computing A^n efficient when A is diagonalizable.
    """

    def construct(self):
        # Title
        title = Text("Power of Diagonal Matrices", font_size=42)
        title.to_edge(UP)
        self.add(title)

        # Show diagonal matrix power
        diag_power = Tex(
            R"\begin{bmatrix} \lambda_1 & 0 \\ 0 & \lambda_2 \end{bmatrix}^n = "
            R"\begin{bmatrix} \lambda_1^n & 0 \\ 0 & \lambda_2^n \end{bmatrix}",
            font_size=44,
            t2c={R"\lambda_1": TEAL, R"\lambda_2": YELLOW}
        )
        diag_power.next_to(title, DOWN, buff=0.8)

        self.play(Write(diag_power))
        self.wait()

        # Therefore A^n equation
        therefore = Tex(
            R"\therefore \quad A^n = S \Lambda^n S^{-1}",
            font_size=40
        )
        therefore.next_to(diag_power, DOWN, buff=0.6)

        self.play(Write(therefore))
        self.wait()

        # Example with Fibonacci matrix
        fib_title = Text("Example: Fibonacci Matrix", font_size=32)
        fib_title.next_to(therefore, DOWN, buff=0.8)

        fib_matrix = Tex(
            R"A = \begin{bmatrix} 0 & 1 \\ 1 & 1 \end{bmatrix}",
            font_size=36
        )
        fib_matrix.next_to(fib_title, DOWN, buff=0.3)

        fib_result = Tex(
            R"A^n \begin{bmatrix} 0 \\ 1 \end{bmatrix} = "
            R"\begin{bmatrix} F_n \\ F_{n+1} \end{bmatrix}",
            font_size=36
        )
        fib_result.next_to(fib_matrix, DOWN, buff=0.3)

        self.play(Write(fib_title))
        self.play(Write(fib_matrix))
        self.wait(0.5)
        self.play(Write(fib_result))
        self.wait(2)


class ChangeOfBasisVisualization(Scene):
    """
    Shows how the change of basis matrix S transforms coordinates
    between standard basis and eigenbasis.
    """

    def construct(self):
        # Title
        title = Text("Change of Basis", font_size=42)
        title.to_edge(UP)

        # Main equation
        cob_eq = Tex(
            R"x \hat{\mathbf{i}} + y \hat{\mathbf{j}} = "
            R"\tilde{x} \vec{\mathbf{v}}_1 + \tilde{y} \vec{\mathbf{v}}_2",
            font_size=40,
            t2c={
                R"\hat{\mathbf{i}}": GREEN,
                R"\hat{\mathbf{j}}": RED,
                R"\vec{\mathbf{v}}_1": TEAL,
                R"\vec{\mathbf{v}}_2": YELLOW,
            }
        )
        cob_eq.next_to(title, DOWN, buff=0.6)

        # Standard basis label
        std_label = Text("Standard Basis", font_size=24, color=GREY_B)
        std_label.next_to(cob_eq[:6], DOWN, buff=0.3)

        # Eigenbasis label
        eigen_label = Text("Eigenbasis", font_size=24, color=GREY_B)
        eigen_label.next_to(cob_eq[7:], DOWN, buff=0.3)

        # Show transformation
        self.play(Write(title))
        self.play(Write(cob_eq))
        self.play(
            FadeIn(std_label, shift=UP * 0.2),
            FadeIn(eigen_label, shift=UP * 0.2),
        )
        self.wait()

        # Simplified ODE in eigenbasis
        ode_title = Text("ODE becomes simple in eigenbasis:", font_size=28)
        ode_title.next_to(eigen_label, DOWN, buff=0.8)

        ode_original = Tex(
            R"\frac{d}{dt}\begin{bmatrix} x \\ y \end{bmatrix} = "
            R"A \begin{bmatrix} x \\ y \end{bmatrix}",
            font_size=32
        )
        ode_original.next_to(ode_title, DOWN, buff=0.3)

        arrow = Tex(R"\Downarrow", font_size=40)
        arrow.next_to(ode_original, DOWN, buff=0.3)

        ode_simple = Tex(
            R"\frac{d}{dt}\begin{bmatrix} \tilde{x} \\ \tilde{y} \end{bmatrix} = "
            R"\begin{bmatrix} \lambda_1 & 0 \\ 0 & \lambda_2 \end{bmatrix}"
            R"\begin{bmatrix} \tilde{x} \\ \tilde{y} \end{bmatrix}",
            font_size=32,
            t2c={R"\lambda_1": TEAL, R"\lambda_2": YELLOW}
        )
        ode_simple.next_to(arrow, DOWN, buff=0.3)

        self.play(Write(ode_title))
        self.play(Write(ode_original))
        self.play(Write(arrow))
        self.play(Write(ode_simple))
        self.wait()

        # Solution
        solution = Tex(
            R"\tilde{x}(t) = \tilde{x}_0 e^{\lambda_1 t}, \quad "
            R"\tilde{y}(t) = \tilde{y}_0 e^{\lambda_2 t}",
            font_size=32,
            t2c={R"\lambda_1": TEAL, R"\lambda_2": YELLOW}
        )
        solution.next_to(ode_simple, DOWN, buff=0.5)

        self.play(Write(solution))
        self.wait(2)
