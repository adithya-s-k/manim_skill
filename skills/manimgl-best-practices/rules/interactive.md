# ManimGL Interactive Development

ManimGL's killer feature is interactive development mode, allowing you to iterate rapidly without re-rendering the entire scene.

## Starting Interactive Mode

Use the `-se` (skip and embed) flag with a line number:

```bash
# Enter interactive mode at line 20
manimgl scene.py MyScene -se 20

# Enter at the beginning
manimgl scene.py MyScene -se 1
```

The scene runs up to that line, then drops into an IPython shell.

## checkpoint_paste()

The core workflow function. Copy code to your clipboard, then:

```python
# Run code from clipboard with full animations
checkpoint_paste()

# Run instantly without animations (for quick iteration)
checkpoint_paste(skip=True)

# Record animations while running
checkpoint_paste(record=True)
```

### Typical Workflow

1. Write your scene with placeholder line
2. Run with `-se` at that line
3. Copy animation code to clipboard
4. Call `checkpoint_paste()` to test
5. Iterate until satisfied
6. Move code into the actual file

## self.embed()

Drop into IPython shell programmatically:

```python
class MyScene(InteractiveScene):
    def construct(self):
        circle = Circle()
        self.play(ShowCreation(circle))

        self.embed()  # Pause here, enter shell

        # Code below runs after you exit the shell
        self.play(FadeOut(circle))
```

In the shell, you have full access to:
- `self` - the scene
- All mobjects in scope
- All ManimGL functions

## Interactive Shell Commands

Once in the shell:

```python
# Inspect current mobjects
self.mobjects

# Add something new
square = Square()
self.play(ShowCreation(square))

# Clear and try again
self.clear()

# Exit shell and continue scene
exit()
# or Ctrl+D
```

## Quick Iteration Pattern

```python
class DevelopScene(InteractiveScene):
    def construct(self):
        # Setup that doesn't change often
        axes = Axes()
        self.add(axes)

        # Breakpoint for development
        self.embed()

        # Code you're iterating on goes here
        # (Or use checkpoint_paste() in the shell)
```

## Recording Mode

When you want to capture what you're doing interactively:

```python
# Start recording
checkpoint_paste(record=True)

# All animations are now recorded
# When done, video is saved
```

## Useful Shell Variables

```python
# Current frame (camera)
self.frame

# All mobjects
self.mobjects

# Specific mobjects by type
[m for m in self.mobjects if isinstance(m, Circle)]

# Frame center
self.frame.get_center()
```

## Debugging Tips

```python
# Print mobject info
print(circle.get_center())
print(circle.get_height())
print(circle.get_color())

# Highlight a mobject
circle.set_color(YELLOW)
self.wait(0.1)

# Check what's in the scene
print(len(self.mobjects))
```

## Exit and Continue

```python
# After interactive session, continue scene
exit()  # or Ctrl+D

# The scene continues from where it left off
```

## Best Practices

1. **Use `-se` during development** - Much faster than re-rendering
2. **Keep setup code before the embed** - Reuse state
3. **Use `checkpoint_paste(skip=True)`** - For quick tests
4. **Use `checkpoint_paste(record=True)`** - When you've got it right
5. **Organize code into functions** - Easier to paste and test
