---
name: cli
description: Command-line interface, rendering options, and quality flags
metadata:
  tags: cli, render, quality, preview, command, terminal
---

# Manim CLI

The `manim` command-line interface for rendering scenes.

## Basic Usage

```bash
# Render a scene
manim file.py SceneName

# With preview (opens video after rendering)
manim -p file.py SceneName

# Preview with low quality (fast)
manim -pql file.py SceneName
```

## Quality Flags

Quality presets for different use cases:

```bash
# Low Quality: 854x480, 15fps (fast for testing)
manim -ql file.py SceneName

# Medium Quality: 1280x720, 30fps
manim -qm file.py SceneName

# High Quality: 1920x1080, 60fps
manim -qh file.py SceneName

# 2K Quality: 2560x1440, 60fps
manim -qp file.py SceneName

# 4K Quality: 3840x2160, 60fps
manim -qk file.py SceneName
```

### Common Combinations

```bash
# Preview + Low Quality (development workflow)
manim -pql file.py SceneName

# Preview + High Quality (final check)
manim -pqh file.py SceneName
```

## Preview Flag

```bash
# -p: Open video after rendering
manim -p file.py SceneName

# Without -p: Render only (no auto-open)
manim file.py SceneName
```

## Rendering Multiple Scenes

```bash
# Render all scenes in file
manim -a file.py

# Render specific scenes
manim file.py Scene1 Scene2 Scene3
```

## Output Options

### Save Last Frame Only

```bash
# -s: Save only the last frame as PNG
manim -s file.py SceneName

# With quality
manim -sql file.py SceneName
```

### Output Format

```bash
# GIF output
manim --format gif file.py SceneName

# PNG sequence
manim --format png file.py SceneName

# WebM (default is MP4)
manim --format webm file.py SceneName
```

### Custom Output Directory

```bash
manim -o custom_name file.py SceneName
manim --media_dir /path/to/output file.py SceneName
```

## Frame Control

```bash
# Start from specific animation number
manim -n 5 file.py SceneName

# Render frames from animation 3 to 7
manim -n 3,7 file.py SceneName
```

## Resolution and FPS

```bash
# Custom resolution
manim -r 1920,1080 file.py SceneName

# Custom frame rate
manim --fps 24 file.py SceneName

# Both
manim -r 1280,720 --fps 30 file.py SceneName
```

## Transparency

```bash
# Render with transparent background
manim -t file.py SceneName
```

## Renderer Selection

```bash
# Cairo renderer (default, 2D)
manim --renderer cairo file.py SceneName

# OpenGL renderer (3D, faster preview)
manim --renderer opengl file.py SceneName
```

## Other Useful Flags

```bash
# Verbose output
manim -v DEBUG file.py SceneName

# Quiet mode
manim -v WARNING file.py SceneName

# Show progress bar
manim --progress_bar display file.py SceneName

# Disable caching
manim --disable_caching file.py SceneName

# Write to movie even if no animations
manim --write_to_movie file.py SceneName
```

## Help

```bash
# Show all options
manim --help

# Show render command options
manim render --help
```

## Other Commands

```bash
# Check installation and dependencies
manim checkhealth

# Initialize new project
manim init

# Show config values
manim cfg show

# Write current config to file
manim cfg write

# List installed plugins
manim plugins -l
```

## Jupyter Notebook Support

Use the `%%manim` cell magic in Jupyter notebooks:

```python
%%manim -qm -v WARNING MyScene
class MyScene(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
```

Flags work the same as CLI (`-qm`, `-ql`, etc.).

## Typical Development Workflow

```bash
# 1. Develop with fast preview
manim -pql scene.py MyScene

# 2. Check at medium quality
manim -pqm scene.py MyScene

# 3. Final render at high quality
manim -qh scene.py MyScene

# 4. Create GIF for sharing
manim --format gif -qm scene.py MyScene
```

## Best Practices

1. **Use -pql for development** - Fast iteration cycle
2. **Use -qh for final output** - Good quality, reasonable render time
3. **Use -s for thumbnails** - Quick last-frame capture
4. **Use -a sparingly** - Renders everything, can be slow
5. **Use --format gif for demos** - Easy to share and embed
