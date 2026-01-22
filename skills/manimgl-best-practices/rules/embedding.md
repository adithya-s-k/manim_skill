# Interactive Embedding in ManimGL

ManimGL's `self.embed()` feature drops you into an interactive IPython shell during scene execution, making debugging and experimentation incredibly powerful.

## Basic Usage

### Adding embed() to Your Scene

```python
from manimlib import *

class MyScene(Scene):
    def construct(self):
        circle = Circle()
        self.play(ShowCreation(circle))

        # Drop into interactive shell here
        self.embed()

        # Code continues after you exit the shell
        self.play(circle.animate.shift(RIGHT))
        self.wait()
```

### Running with Embed

```bash
# Run scene - will pause at embed() point
manimgl scene.py MyScene
```

## Interactive Commands

### Available in Shell

When `self.embed()` opens the IPython shell, you have access to:

```python
# Scene methods (abbreviated - no 'self.' needed)
play(animation)              # Play animation
add(mobject)                 # Add mobject to scene
remove(mobject)              # Remove mobject
wait(duration)               # Wait for duration
clear()                      # Clear scene

# Camera/frame control
frame                        # Access camera frame
play(frame.animate.shift(RIGHT))

# All local variables from construct()
circle, square, text, etc.   # Your mobjects

# Interactive camera
touch()                      # Enter touch mode (press 'q' to exit)
                            # Press 'd' + mouse to rotate
                            # Press 'z' + scroll to zoom
                            # Press 'r' to reset

# Exit shell and continue
exit()                       # Continue scene execution
```

## Practical Examples

### Debugging Animation

```python
class DebugScene(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        self.add(circle, square)

        # Problem with this animation?
        self.play(circle.animate.move_to(square))

        # Debug it interactively
        self.embed()

        # In the shell:
        # >>> play(circle.animate.set_color(RED))
        # >>> circle.get_center()
        # >>> square.get_center()
```

### Experimenting with Positioning

```python
class PositioningExperiment(Scene):
    def construct(self):
        shapes = VGroup(*[
            Circle(radius=0.5) for _ in range(5)
        ])

        # Try different arrangements interactively
        self.add(shapes)
        self.embed()

        # In the shell, try:
        # >>> play(shapes.animate.arrange(RIGHT, buff=1))
        # >>> play(shapes.animate.arrange(DOWN, buff=0.5))
        # >>> play(shapes.animate.arrange_in_grid(rows=2))
```

### Color and Style Exploration

```python
class StyleExploration(Scene):
    def construct(self):
        text = Text("Experiment", font_size=72)
        self.add(text)
        self.embed()

        # In the shell:
        # >>> play(text.animate.set_color(BLUE))
        # >>> text.set_backstroke(BLACK, width=10)
        # >>> play(text.animate.scale(2))
```

## Advanced embed() Usage

### Multiple Embed Points

```python
class MultipleEmbeds(Scene):
    def construct(self):
        # First checkpoint
        circle = Circle()
        self.play(ShowCreation(circle))
        self.embed()  # First pause

        # Second checkpoint
        square = Square()
        self.play(ShowCreation(square))
        self.embed()  # Second pause

        # Third checkpoint
        self.play(FadeOut(VGroup(circle, square)))
        self.embed()  # Third pause
```

### Conditional Embedding

```python
class ConditionalEmbed(Scene):
    def construct(self):
        DEBUG = True

        circle = Circle()
        self.play(ShowCreation(circle))

        if DEBUG:
            self.embed()  # Only embed in debug mode

        self.play(circle.animate.shift(RIGHT))
```

## Using with -se Flag

### Skip and Embed

The `-se` flag skips to a specific line and embeds:

```python
class LargeScene(Scene):
    def construct(self):
        # Line 5
        circle = Circle()
        self.play(ShowCreation(circle))

        # Line 10
        square = Square()
        self.play(ShowCreation(square))

        # Line 15
        text = Text("Hello")
        self.play(Write(text))

        # Line 20
        self.play(FadeOut(VGroup(circle, square, text)))
```

```bash
# Skip directly to line 15 and embed
manimgl scene.py LargeScene -se 15
```

## checkpoint_paste()

### Interactive Code Execution

`checkpoint_paste()` runs code from your clipboard:

```python
class CheckpointScene(Scene):
    def construct(self):
        circle = Circle()
        self.add(circle)
        self.embed()
```

```bash
# Run the scene
manimgl scene.py CheckpointScene
```

In the shell:

```python
# Copy this code to clipboard first:
"""
square = Square()
play(ShowCreation(square))
play(square.animate.next_to(circle, RIGHT))
"""

# Then in the shell:
>>> checkpoint_paste()              # Runs with animations
>>> checkpoint_paste(skip=True)     # Runs instantly
>>> checkpoint_paste(record=True)   # Records while running
```

## Saving and Restoring State

### save_state() and restore()

```python
class StateManagement(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        self.add(circle, square)

        # Save current state
        self.save_state()

        # Make changes
        self.play(circle.animate.shift(RIGHT * 3))
        self.play(square.animate.shift(LEFT * 3))

        self.embed()

        # In the shell:
        # >>> restore()  # Revert to saved state
```

## Interactive 3D Exploration

### touch() Mode

```python
class Interactive3D(Scene):
    def construct(self):
        frame = self.camera.frame
        frame.reorient(20, 70)

        # Create 3D object
        sphere = Sphere(radius=2, color=BLUE)
        self.add(sphere)

        self.embed()

        # In the shell:
        # >>> touch()
        # Now you can:
        # - Press 'd' and move mouse to rotate
        # - Press 'z' and scroll to zoom
        # - Press 'r' to reset camera
        # - Press 'q' to exit touch mode
```

## Debugging Patterns

### Inspect Mobject Properties

```python
class InspectProperties(Scene):
    def construct(self):
        circle = Circle(radius=2, color=BLUE)
        circle.shift(RIGHT * 3)
        self.add(circle)
        self.embed()

        # In the shell:
        # >>> circle.get_center()
        # >>> circle.get_color()
        # >>> circle.get_width()
        # >>> circle.get_height()
        # >>> circle.get_all_points()
```

### Test Animation Timing

```python
class TimingTest(Scene):
    def construct(self):
        circle = Circle()
        self.add(circle)
        self.embed()

        # In the shell, test different timings:
        # >>> play(circle.animate.shift(RIGHT), run_time=0.5)
        # >>> play(circle.animate.shift(LEFT), run_time=2)
        # >>> play(circle.animate.shift(UP), run_time=1, rate_func=smooth)
```

### Build Complex Scenes Iteratively

```python
class IterativeBuilding(Scene):
    def construct(self):
        self.embed()

        # Build entire scene in the shell:
        # >>> title = Text("My Animation")
        # >>> title.to_edge(UP)
        # >>> add(title)
        #
        # >>> circles = VGroup(*[Circle(radius=0.5) for _ in range(5)])
        # >>> circles.arrange(RIGHT, buff=0.5)
        # >>> play(LaggedStart(*[ShowCreation(c) for c in circles], lag_ratio=0.2))
        #
        # >>> formula = Tex(R"E = mc^2")
        # >>> formula.next_to(circles, DOWN, buff=1)
        # >>> play(Write(formula))
```

## Best Practices

1. **Use for debugging**: Add `self.embed()` when animations don't work as expected
2. **Experiment freely**: Try different approaches in the shell before adding to code
3. **save_state() before experimenting**: Easy to revert if something goes wrong
4. **Use -se for large scenes**: Jump to problem area instead of watching entire animation
5. **checkpoint_paste() for iteration**: Quickly test code snippets
6. **touch() for 3D**: Essential for finding the right camera angle
7. **Remove embed() for final render**: Don't forget to remove debugging embeds

## Common Patterns

### Quick experiment pattern

```python
# Add at problem point
self.embed()

# In shell, test fix
play(mobject.animate.scale(2))  # Test different values

# If it works, add to code
# exit()
```

### Interactive development pattern

```python
# Start with minimal setup
class Scene(Scene):
    def construct(self):
        self.embed()

# Build everything in the shell
# Copy successful commands back to code
```

### 3D camera setup pattern

```python
# Get to 3D scene
frame.reorient(20, 70)
add(sphere)
self.embed()

# Find perfect angle
touch()  # Rotate with mouse
# Press 'q' when done
# Check frame.get_theta(), frame.get_phi()
# Add those values to code
```

## Troubleshooting

### embed() Not Working

- Ensure you're running with `manimgl` command
- Check that IPython is installed
- Verify no syntax errors before embed() point

### Can't Access Variables

- Variables must be defined before `self.embed()`
- Use `locals()` or `globals()` to inspect available variables

### Shell Exits Immediately

- Don't call `exit()` unless you want to continue
- Press Ctrl+D to exit and continue
- Use `quit()` or `exit()` to close shell

## Example: Full Interactive Development

```python
class InteractiveDevelopment(Scene):
    def construct(self):
        # Start with embed
        self.embed()

        # In the shell, build everything:
        """
        # Create title
        title = Text("Interactive Development", font_size=60)
        title.to_edge(UP)
        play(Write(title))

        # Create content
        circle = Circle(radius=1.5, color=BLUE)
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(WHITE, width=3)
        play(ShowCreation(circle))

        # Add label
        label = Text("Circle", font_size=36)
        label.next_to(circle, DOWN)
        play(FadeIn(label, shift=UP))

        # Animate
        play(
            circle.animate.shift(RIGHT * 2),
            label.animate.shift(RIGHT * 2)
        )

        wait(2)

        # When happy, copy all this code to your construct method
        exit()
        """
```

This makes ManimGL incredibly powerful for rapid prototyping and debugging!
