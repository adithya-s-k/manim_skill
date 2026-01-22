---
name: config
description: Configuration system, manim.cfg, and settings
metadata:
  tags: config, configuration, settings, manim.cfg, options
---

# Configuration

Configure Manim's behavior through files and code.

## Configuration Hierarchy

Manim reads configuration from (in order of precedence):
1. Command-line arguments (highest priority)
2. User's `manim.cfg` in current directory
3. User's global config
4. Default values (lowest priority)

## manim.cfg File

Create a `manim.cfg` file in your project directory:

```ini
[CLI]
# Preview after rendering
preview = True

# Default quality
quality = medium_quality

# Output format
format = mp4

# Frame rate
frame_rate = 30

[output]
# Custom output directory
media_dir = ./media

# Save last frame as PNG
save_last_frame = False

[renderer]
# Background color
background_color = BLACK

[style]
# Default font
font = Arial
```

## Common Configuration Options

### CLI Section

```ini
[CLI]
# Quality presets: low_quality, medium_quality, high_quality, production_quality, fourk_quality
quality = medium_quality

# Preview video after rendering
preview = True

# Frame rate
frame_rate = 30

# Output format: mp4, gif, mov, webm, png
format = mp4

# Transparent background
transparent = False

# Progress bar: display, leave, none
progress_bar = display
```

### Rendering Section

```ini
[renderer]
# Background color (hex or color name)
background_color = #1e1e1e

# Renderer type: cairo, opengl
renderer = cairo
```

### Resolution

```ini
[CLI]
# Frame dimensions
pixel_width = 1920
pixel_height = 1080
```

## Programmatic Configuration

Access and modify config in your Python code:

```python
# Access config values
config.pixel_width  # e.g., 1920
config.frame_rate  # e.g., 30
config.background_color  # e.g., BLACK

# Modify config (before creating scenes)
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60
config.background_color = BLUE_E
```

### In Scene

```python
class MyScene(Scene):
    def construct(self):
        # Access frame dimensions
        width = config.frame_width
        height = config.frame_height

        # Create rectangle matching frame size
        frame_rect = Rectangle(
            width=width,
            height=height,
            stroke_color=WHITE
        )
        self.add(frame_rect)
```

## Background Color

### In Config File

```ini
[renderer]
background_color = BLACK
# Or hex color
background_color = #1a1a2e
```

### In Code

```python
class DarkBackground(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        # ... rest of scene
```

## Output Directory Structure

Default media directory structure:
```
media/
├── videos/
│   └── scene_file/
│       ├── 480p15/       # Low quality
│       ├── 720p30/       # Medium quality
│       ├── 1080p60/      # High quality
│       └── 2160p60/      # 4K quality
├── images/
│   └── scene_file/
│       └── SceneName.png
└── Tex/                  # LaTeX cache
```

### Custom Output Directory

```ini
[output]
media_dir = ./output
```

Or via CLI:
```bash
manim --media_dir ./output file.py Scene
```

## Tex Configuration

For LaTeX rendering:

```ini
[tex]
# Custom preamble
preamble = \usepackage{amsmath}\usepackage{amssymb}

# Tex compiler
tex_compiler = latex
```

## Caching

```ini
[CLI]
# Disable caching (useful for debugging)
disable_caching = True

# Max cached files
max_files_cached = 100
```

## Viewing Current Config

```bash
# Show all config values
manim cfg show

# Show specific section
manim cfg show CLI

# Write current config to file
manim cfg write
```

## Project-Specific Config

Create `manim.cfg` in your project root:

```ini
[CLI]
quality = high_quality
preview = True
frame_rate = 60

[renderer]
background_color = #0d1117

[output]
media_dir = ./renders
```

## Plugins

Manim has an extensible plugin system:

```bash
# List installed plugins
manim plugins -l

# Install a plugin
pip install manim-pluginname
```

Enable plugins in `manim.cfg`:

```ini
[CLI]
plugins = manim-pluginname
# For multiple plugins:
plugins = plugin1,plugin2
```

## Best Practices

1. **Use manim.cfg for project defaults** - Consistent settings across team
2. **Keep quality low during development** - Faster iteration
3. **Set background_color in config** - Not in every scene
4. **Use custom media_dir** - Keep renders organized
5. **Commit manim.cfg to version control** - Share settings with collaborators
