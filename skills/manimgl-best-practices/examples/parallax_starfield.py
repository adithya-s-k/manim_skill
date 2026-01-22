"""
Parallax Effect with 3D Starfield

Demonstrates the parallax effect - how nearby objects appear to move more
than distant objects when the observer moves. This is a fundamental concept
in astronomy for measuring distances to stars.

Run: manimgl parallax_starfield.py ParallaxStarfield -w
Preview: manimgl parallax_starfield.py ParallaxStarfield -p

Source: Adapted from 3b1b's cosmic_distance video (2025)
"""
from manimlib import *
import numpy as np


class ParallaxStarfield(InteractiveScene):
    """
    A 3D scene showing parallax effect with stars at different distances.

    Key techniques demonstrated:
    - GlowDots for efficient star rendering
    - 3D camera manipulation with frame.animate.reorient()
    - VCube as a visual reference box
    - Observer movement to demonstrate parallax
    """

    def construct(self):
        # Setup 3D environment
        frame = self.frame
        self.set_floor_plane("xz")  # Set z as vertical axis

        # Create a reference cube to help visualize 3D space
        height = 4
        cube = VCube(height)
        cube.set_fill(opacity=0)
        cube.set_stroke(BLUE, 2)

        # Create stars as GlowDots - efficient for many point lights
        n_stars = 200
        # Random positions in a cube
        star_positions = np.random.uniform(-1, 1, (n_stars, 3))
        stars = GlowDots(star_positions)
        stars.scale(height / 2)  # Scale to fit within our cube
        stars.set_color(WHITE)
        stars.set_glow_factor(2)
        # Vary star sizes for visual interest
        stars.set_radii(np.random.uniform(0, 0.075, n_stars))

        self.add(cube)
        self.add(stars)

        # Animate stars appearing
        self.play(ShowCreation(stars, run_time=3))

        # Add an observer (using a simple 3D sphere)
        observer = Sphere(radius=0.3)
        observer.set_color(BLUE_E)
        observer.set_shading(0.5, 0.5, 0.5)
        observer.next_to(cube, LEFT, buff=1)

        # Add an arrow to show viewing direction
        eye_arrow = Arrow(
            observer.get_center(),
            observer.get_center() + 1.5 * RIGHT,
            buff=0,
            stroke_color=YELLOW,
            stroke_width=4,
        )
        eye_arrow.add_updater(lambda m: m.put_start_and_end_on(
            observer.get_center(),
            observer.get_center() + 1.5 * RIGHT
        ))

        self.play(
            FadeIn(observer),
            ShowCreation(eye_arrow),
        )

        # Rotate camera for better 3D view
        self.play(frame.animate.reorient(-40, -26, 0), run_time=2)

        # Key demonstration: Move observer up and down
        # Watch how nearby stars shift more than distant ones
        for dy in [1.5, -3, 3, -3, 1.5]:
            self.play(
                observer.animate.shift(dy * IN),  # IN = into screen = Z axis
                run_time=3
            )

        self.wait()


class ParallaxFromObserverPOV(InteractiveScene):
    """
    Same parallax demo but from the observer's point of view.

    This variant shows what the observer would actually see -
    the apparent motion of stars against the background.
    """

    def construct(self):
        frame = self.frame
        self.set_floor_plane("xz")

        # Create starfield
        height = 4
        cube = VCube(height)
        cube.set_fill(opacity=0)
        cube.set_stroke(BLUE, 2)

        n_stars = 200
        star_positions = np.random.uniform(-1, 1, (n_stars, 3))
        stars = GlowDots(star_positions)
        stars.scale(height / 2)
        stars.set_color(WHITE)
        stars.set_glow_factor(2)
        stars.set_radii(np.random.uniform(0, 0.075, n_stars))

        self.add(cube, stars)
        self.play(ShowCreation(stars, run_time=2))

        # Add observer as a tracking point
        observer = Sphere(radius=0.3)
        observer.set_color(BLUE_E)
        observer.next_to(cube, LEFT, buff=1)

        self.play(FadeIn(observer))

        # Move camera to observer's perspective
        self.play(
            frame.animate.reorient(-89, -4, 0, (0.01, 0.21, 0.0), 3.05),
            observer.animate.set_opacity(0),
            cube.animate.set_stroke(width=5).set_anti_alias_width(10),
            run_time=3,
        )

        # Camera follows observer's z position
        frame.always.match_z(observer)

        # Move observer - camera follows, showing parallax from their view
        for dy in [1.5, -3, 3, -3, 1.5]:
            self.play(observer.animate.shift(dy * IN), run_time=4)

        self.wait()


class LayeredParallax(InteractiveScene):
    """
    Demonstrates parallax with explicitly layered star planes.

    Shows three distinct layers at different distances to make
    the parallax effect more obvious and educational.
    """

    def construct(self):
        frame = self.frame
        self.set_floor_plane("xz")

        # Create three layers of stars at different distances
        layers = []
        colors = [RED, YELLOW, BLUE]
        distances = [2, 5, 10]  # Distance from origin
        n_stars_per_layer = 50

        for color, dist in zip(colors, distances):
            # Create stars in an XY plane at distance Z
            positions = np.random.uniform(-3, 3, (n_stars_per_layer, 3))
            positions[:, 2] = dist  # Set all Z to this layer's distance

            layer = GlowDots(positions)
            layer.set_color(color)
            layer.set_glow_factor(1.5)
            layer.set_radii(np.full(n_stars_per_layer, 0.05))
            layers.append(layer)

        all_stars = Group(*layers)

        # Add distance labels
        labels = VGroup()
        for color, dist in zip(colors, distances):
            label = Text(f"{dist} units away", color=color, font_size=24)
            label.to_corner(UL)
            label.shift(DOWN * (distances.index(dist) * 0.5))
            labels.add(label)

        self.add(all_stars, labels)

        # Position camera to see all layers
        frame.reorient(-30, -20, 0)
        frame.set_height(12)

        # Create observer dot
        observer = Sphere(radius=0.2)
        observer.set_color(GREEN)
        observer.move_to(ORIGIN)

        self.add(observer)
        self.wait()

        # Move observer laterally - watch the layers shift differently
        for dx in [2, -4, 4, -2]:
            self.play(
                observer.animate.shift(dx * RIGHT),
                run_time=3,
                rate_func=smooth
            )

        self.wait()
