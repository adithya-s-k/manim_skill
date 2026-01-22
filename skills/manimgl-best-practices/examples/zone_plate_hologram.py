"""
Zone Plate / Fresnel Zone Plate Visualization

Demonstrates the creation and properties of a Fresnel zone plate,
which is the simplest form of hologram - recording interference
between a point source and a reference wave.

Based on 3Blue1Brown's hologram visualizations.

Run: manimgl zone_plate_hologram.py ZonePlateCreation -w
"""
from manimlib import *
import numpy as np


class ZonePlateCreation(Scene):
    """
    Shows how a zone plate pattern emerges from interference
    between a point source and a plane reference wave.
    """

    def construct(self):
        frame = self.camera.frame

        # Title
        title = Text("Fresnel Zone Plate", font_size=48)
        title.to_edge(UP)
        title.set_backstroke(BLACK, 5)
        self.add(title)

        # Parameters
        source_distance = 4.0  # Distance of point source from plate
        wavelength = 0.3
        plate_size = 6.0

        # Point source position (behind the plate plane)
        source_pos = np.array([0, 0, source_distance])

        # Create zone plate pattern
        def get_zone_plate(resolution=200):
            plate = VGroup()

            # Sample grid on the plate
            for i in range(resolution):
                for j in range(resolution):
                    x = (i / resolution - 0.5) * plate_size
                    y = (j / resolution - 0.5) * plate_size
                    point = np.array([x, y, 0])

                    # Distance from point source
                    r = np.linalg.norm(point - source_pos)

                    # Phase from point source
                    phase_obj = (r / wavelength) % 1

                    # Phase from reference (plane wave from behind)
                    phase_ref = (source_distance / wavelength) % 1

                    # Interference pattern intensity
                    phase_diff = (phase_obj - phase_ref) * TAU
                    intensity = (1 + np.cos(phase_diff)) / 2

                    # Create small square
                    size = plate_size / resolution * 1.1
                    square = Square(side_length=size)
                    square.move_to([x, y, 0])
                    square.set_stroke(width=0)
                    square.set_fill(
                        interpolate_color(BLACK, WHITE, intensity),
                        opacity=1
                    )
                    plate.add(square)

            return plate

        # Create the pattern with increasing resolution
        low_res = get_zone_plate(30)
        self.play(FadeIn(low_res, lag_ratio=0.001))
        self.wait()

        # Show it's made of concentric rings
        ring_explanation = Text("Concentric rings from interference", font_size=32)
        ring_explanation.next_to(title, DOWN)
        ring_explanation.set_backstroke(BLACK, 3)

        self.play(Write(ring_explanation))
        self.wait()

        # Increase resolution
        mid_res = get_zone_plate(60)
        self.play(
            ReplacementTransform(low_res, mid_res),
            run_time=2
        )
        self.wait()

        high_res = get_zone_plate(100)
        self.play(
            ReplacementTransform(mid_res, high_res),
            run_time=2
        )
        self.wait(2)


class ZonePlateFromPointSource(Scene):
    """
    Shows the geometry of how zone plates form from a point source.
    """

    def construct(self):
        frame = self.camera.frame
        frame.reorient(20, 70, 0)

        # 3D setup
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[0, 5, 1],
        )
        axes.set_opacity(0.3)

        # Point source
        source_z = 4.0
        source = Sphere(radius=0.15, color=WHITE)
        source.move_to([0, 0, source_z])

        source_label = Text("Point Source", font_size=24)
        source_label.rotate(PI/2, RIGHT)
        source_label.next_to(source, OUT + UP, buff=0.3)
        source_label.set_backstroke(BLACK, 3)

        # Film plane
        film = Square(side_length=6)
        film.set_fill(GREY_E, opacity=0.5)
        film.set_stroke(WHITE, 1)
        film.move_to(ORIGIN)

        film_label = Text("Film Plane", font_size=24)
        film_label.next_to(film, DOWN)
        film_label.set_backstroke(BLACK, 3)

        # Wavefronts from point source (spherical shells)
        def get_spherical_waves(time, n_waves=6):
            waves = Group()
            for i in range(n_waves):
                radius = 0.5 + i * 0.8 + time * 0.2
                if radius < 6:
                    sphere = Sphere(radius=radius)
                    sphere.move_to([0, 0, source_z])
                    sphere.set_color(BLUE)
                    sphere.set_opacity(0.15 * (1 - radius / 6))
                    waves.add(sphere)
            return waves

        time_tracker = ValueTracker(0)
        waves = always_redraw(lambda: get_spherical_waves(time_tracker.get_value()))

        # Reference wave fronts (planes)
        def get_plane_waves(time, n_waves=8):
            planes = Group()
            for i in range(n_waves):
                z = source_z - 0.5 - i * 0.8 + time * 0.2
                if 0 < z < source_z:
                    plane = Square(side_length=8)
                    plane.set_fill(TEAL, opacity=0.1 * (z / source_z))
                    plane.set_stroke(TEAL, 1, opacity=0.3)
                    plane.move_to([0, 0, z])
                    planes.add(plane)
            return planes

        ref_waves = always_redraw(lambda: get_plane_waves(time_tracker.get_value()))

        self.add(axes)
        self.add(film, film_label)
        self.add(source, source_label)
        self.add(waves)
        self.add(ref_waves)

        # Animate waves
        self.play(
            time_tracker.animate.set_value(10),
            frame.animate.increment_theta(30 * DEGREES),
            run_time=10,
            rate_func=linear
        )
        self.wait()


class ZonePlateAsLens(Scene):
    """
    Demonstrates how a zone plate acts as a lens, focusing light.
    """

    def construct(self):
        # Title
        title = Text("Zone Plate as Focusing Element", font_size=42)
        title.to_edge(UP)
        title.set_backstroke(BLACK, 5)
        self.add(title)

        # Zone plate representation
        plate_x = -2
        plate = VGroup()
        n_rings = 12
        for i in range(n_rings):
            r_outer = 0.15 * (i + 1)
            r_inner = 0.15 * i if i > 0 else 0
            if i % 2 == 0:
                ring = Annulus(inner_radius=r_inner, outer_radius=r_outer)
                ring.set_fill(GREY_D, opacity=1)
                ring.set_stroke(width=0)
                plate.add(ring)
            else:
                ring = Annulus(inner_radius=r_inner, outer_radius=r_outer)
                ring.set_fill(WHITE, opacity=0.8)
                ring.set_stroke(width=0)
                plate.add(ring)
        plate.move_to([plate_x, 0, 0])

        plate_label = Text("Zone Plate", font_size=24)
        plate_label.next_to(plate, DOWN)

        # Focal point
        focal_x = 3
        focal_point = Dot([focal_x, 0, 0], color=YELLOW, radius=0.15)
        focal_label = Text("Focus", font_size=24, color=YELLOW)
        focal_label.next_to(focal_point, DOWN)

        # Incoming parallel rays
        incoming_rays = VGroup()
        ray_positions = np.linspace(-1.5, 1.5, 7)
        for y in ray_positions:
            ray = Arrow([-6, y, 0], [plate_x - 0.2, y, 0], buff=0, stroke_width=2)
            ray.set_color(BLUE)
            incoming_rays.add(ray)

        # Diffracted rays converging to focus
        diffracted_rays = VGroup()
        for y in ray_positions:
            ray = Line([plate_x + 0.2, y, 0], [focal_x, 0, 0])
            ray.set_stroke(RED, 2)
            diffracted_rays.add(ray)

        self.add(plate, plate_label)
        self.play(
            LaggedStartMap(GrowArrow, incoming_rays, lag_ratio=0.1),
            run_time=2
        )
        self.wait()

        incoming_label = Text("Parallel Light", font_size=24, color=BLUE)
        incoming_label.next_to(incoming_rays, UP)

        self.play(Write(incoming_label))
        self.wait()

        # Show diffraction
        self.play(
            LaggedStartMap(ShowCreation, diffracted_rays, lag_ratio=0.1),
            FadeIn(focal_point),
            Write(focal_label),
            run_time=2
        )
        self.wait()

        # Explanation
        explanation = Text(
            "Zone plate diffracts light to focal point",
            font_size=28
        )
        explanation.next_to(title, DOWN)
        self.play(Write(explanation))
        self.wait(2)


class InterferenceBands(Scene):
    """
    Shows the intensity pattern resulting from two-wave interference.
    A simplified representation of holographic recording.
    """

    def construct(self):
        # Title
        title = Text("Interference Pattern on Film", font_size=42)
        title.to_edge(UP)
        title.set_backstroke(BLACK, 5)
        self.add(title)

        # Parameters
        wavelength = 0.4
        angle = 15 * DEGREES  # Angle between reference and object beams

        # Create interference pattern
        def get_interference_bands(width=12, height=6, resolution=200):
            bands = VGroup()

            # The spacing of fringes depends on the angle between beams
            fringe_spacing = wavelength / (2 * np.sin(angle / 2))

            for i in range(resolution):
                x = (i / resolution - 0.5) * width

                # Intensity from interference
                intensity = (1 + np.cos(TAU * x / fringe_spacing)) / 2

                # Create vertical strip
                strip = Rectangle(width=width / resolution * 1.05, height=height)
                strip.move_to([x, 0, 0])
                strip.set_stroke(width=0)
                strip.set_fill(
                    interpolate_color(BLACK, WHITE, intensity),
                    opacity=1
                )
                bands.add(strip)

            return bands

        bands = get_interference_bands()
        border = Rectangle(width=12, height=6)
        border.set_stroke(WHITE, 2)

        self.play(FadeIn(bands), ShowCreation(border))
        self.wait()

        # Labels
        spacing_label = Text("Fringe spacing depends on beam angle", font_size=28)
        spacing_label.next_to(border, DOWN, buff=0.5)

        formula = Tex(
            R"d = \frac{\lambda}{2\sin(\theta/2)}",
            font_size=36
        )
        formula.next_to(spacing_label, DOWN)

        self.play(Write(spacing_label))
        self.play(Write(formula))
        self.wait(2)

        # Show changing angle effect
        angle_label = Text("Decreasing angle = wider fringes", font_size=24)
        angle_label.to_corner(DR)

        for new_angle in [10 * DEGREES, 5 * DEGREES]:
            wavelength_local = wavelength
            fringe_spacing = wavelength_local / (2 * np.sin(new_angle / 2))

            new_bands = VGroup()
            for i in range(200):
                x = (i / 200 - 0.5) * 12
                intensity = (1 + np.cos(TAU * x / fringe_spacing)) / 2
                strip = Rectangle(width=12 / 200 * 1.05, height=6)
                strip.move_to([x, 0, 0])
                strip.set_stroke(width=0)
                strip.set_fill(
                    interpolate_color(BLACK, WHITE, intensity),
                    opacity=1
                )
                new_bands.add(strip)

            self.play(
                Transform(bands, new_bands),
                FadeIn(angle_label) if new_angle == 10 * DEGREES else Animation(angle_label),
                run_time=2
            )
            self.wait()

        self.wait()
