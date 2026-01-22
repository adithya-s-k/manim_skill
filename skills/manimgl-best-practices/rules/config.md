# Configuration in ManimGL

ManimGL uses `custom_config.yml` files for configuration. These files control directories, camera settings, window properties, and more.

## Configuration File Location

### Default Locations

ManimGL looks for `custom_config.yml` in this order:

1. Current directory
2. Parent directories (recursively up to project root)
3. ManimGL installation directory

```
my_project/
├── custom_config.yml      # Project-specific config
├── scenes/
│   ├── custom_config.yml  # Scenes-specific config (overrides project config)
│   └── scene.py
└── manimlib/              # ManimGL installation
```

### Multiple Configs

```bash
# Use specific config file
manimgl scene.py MyScene --config_file /path/to/config.yml

# Project structure with multiple configs
project/
├── custom_config.yml          # Default for project
├── experiments/
│   ├── custom_config.yml      # Overrides for experiments
│   └── test_scene.py
└── final/
    ├── custom_config.yml      # High quality settings
    └── final_scene.py
```

## Basic Configuration

### Minimal custom_config.yml

```yaml
# Directories
directories:
  output: "./media/videos"
  raster_images: "./media/images"
  vector_images: "./media/svg"
  sounds: "./media/sounds"
  data: "./media/data"

# Window configuration
window_config:
  size: "default"  # or "fullscreen"

# Camera settings
camera_config:
  pixel_height: 1080
  pixel_width: 1920
  frame_rate: 60
```

## Detailed Configuration Options

### Directory Configuration

```yaml
directories:
  # Where rendered videos are saved
  output: "/path/to/output/videos"

  # Where temporary files go
  temporary_storage: "/tmp/manim"

  # Image resources
  raster_images: "./assets/images"
  vector_images: "./assets/svg"

  # Audio resources
  sounds: "./assets/audio"

  # Data files
  data: "./assets/data"

  # LaTeX templates
  tex_templates: "./assets/tex_templates"

  # Font directory
  fonts: "./assets/fonts"
```

### Camera Configuration

```yaml
camera_config:
  # Resolution
  pixel_width: 1920
  pixel_height: 1080

  # Frame rate
  frame_rate: 60

  # Background color
  background_color: "#000000"

  # Frame settings
  frame_height: 8.0
  frame_width: 14.222222222222221  # 16:9 aspect ratio

  # Quality presets
  # These override pixel_width, pixel_height, frame_rate
  quality:
    low:
      pixel_width: 854
      pixel_height: 480
      frame_rate: 15
    medium:
      pixel_width: 1280
      pixel_height: 720
      frame_rate: 30
    high:
      pixel_width: 1920
      pixel_height: 1080
      frame_rate: 60
    ultra_high:
      pixel_width: 3840
      pixel_height: 2160
      frame_rate: 60
```

### Window Configuration

```yaml
window_config:
  # Window size: "default", "fullscreen", or [width, height]
  size: "default"
  # size: "fullscreen"
  # size: [1280, 720]

  # Window position on screen
  position: "UR"  # Upper right
  # Options: UL, UR, DL, DR, TOP, BOTTOM, LEFT, RIGHT, CENTER

  # Monitor to display on (for multi-monitor setups)
  monitor: 0

  # Window title
  window_title: "ManimGL Preview"

  # Show file name in title
  show_file_name_in_title: true
```

### Style Configuration

```yaml
style:
  # Default color constants
  background_color: "#000000"

  # Font settings
  font: "Consolas"
  tex_font: "Latin Modern Math"

  # Default stroke width
  stroke_width: 4

  # Default animation run time
  default_animation_run_time: 1.0
```

### Universal Import Configuration

```yaml
# Auto-import common modules
universal_import_line: |
  from manimlib import *
  import numpy as np
  import itertools as it
```

## Quality Presets

### Command Line Override

```bash
# Use low quality preset
manimgl scene.py MyScene -l

# Use medium quality
manimgl scene.py MyScene -m

# Use high quality
manimgl scene.py MyScene -h

# Use 4K quality
manimgl scene.py MyScene --uhd
```

### Custom Quality Preset

```yaml
camera_config:
  quality:
    custom:
      pixel_width: 2560
      pixel_height: 1440
      frame_rate: 120
```

## LaTeX Configuration

### TeX Configuration

```yaml
tex_config:
  # TeX compiler
  tex_compiler: "latex"  # or "xelatex", "lualatex"

  # TeX template
  tex_template: "tex_template.tex"

  # Additional packages
  tex_packages:
    - "amsmath"
    - "amssymb"
    - "mathtools"

  # Text to LaTeX map
  text_to_replace: {
    # Replacements for common symbols
    "pi": "\\pi",
    "alpha": "\\alpha"
  }
```

## Project-Specific Configuration

### Development Config (fast iteration)

```yaml
# dev_config.yml
directories:
  output: "./output/dev"

camera_config:
  pixel_height: 480
  pixel_width: 854
  frame_rate: 15

window_config:
  size: [1280, 720]
  position: "UR"
```

Usage:

```bash
manimgl scene.py MyScene --config_file dev_config.yml
```

### Production Config (high quality)

```yaml
# prod_config.yml
directories:
  output: "./output/final"

camera_config:
  pixel_height: 2160
  pixel_width: 3840
  frame_rate: 60

style:
  default_animation_run_time: 1.5
```

## Runtime Configuration Override

### Command Line Override

```bash
# Override single value
manimgl scene.py MyScene --config camera_config.frame_rate=30

# Override multiple values
manimgl scene.py MyScene \
  --config camera_config.frame_rate=30 \
  --config camera_config.pixel_width=1280 \
  --config camera_config.pixel_height=720

# Override output directory
manimgl scene.py MyScene --config directories.output=/tmp/manim_output
```

## Complete Example Configuration

### Full custom_config.yml

```yaml
# Directory Configuration
directories:
  output: "./media/videos"
  temporary_storage: "/tmp/manim"
  raster_images: "./assets/images"
  vector_images: "./assets/svg"
  sounds: "./assets/audio"
  data: "./assets/data"
  tex_templates: "./assets/tex"
  fonts: "./assets/fonts"

# Camera Configuration
camera_config:
  pixel_width: 1920
  pixel_height: 1080
  frame_rate: 60
  background_color: "#0a0a0a"
  frame_height: 8.0
  frame_width: 14.222222222222221

# Window Configuration
window_config:
  size: "default"
  position: "UR"
  monitor: 0
  window_title: "ManimGL Preview"
  show_file_name_in_title: true

# Style Configuration
style:
  background_color: "#0a0a0a"
  font: "Consolas"
  tex_font: "Latin Modern Math"
  stroke_width: 4
  default_animation_run_time: 1.0

# TeX Configuration
tex_config:
  tex_compiler: "latex"
  tex_template: "tex_template.tex"
  tex_packages:
    - "amsmath"
    - "amssymb"
    - "mathtools"
    - "physics"

# Universal Imports
universal_import_line: |
  from manimlib import *
  import numpy as np
  import itertools as it
  import random

# Logging
log_level: "INFO"  # DEBUG, INFO, WARNING, ERROR
```

## Best Practices

1. **Separate dev and prod configs**: Use different configs for development and final renders
2. **Project-level configs**: Keep `custom_config.yml` in project root
3. **Override for testing**: Use `--config` flag for temporary changes
4. **Version control**: Commit `custom_config.yml` to git
5. **Document custom settings**: Add comments to explain non-standard values
6. **Consistent paths**: Use relative paths for portability
7. **Quality presets**: Use built-in quality flags (-l, -m, -h) instead of manual resolution changes

## Common Configurations

### For YouTube Videos (1080p)

```yaml
camera_config:
  pixel_width: 1920
  pixel_height: 1080
  frame_rate: 60
  background_color: "#000000"
```

### For Quick Testing

```yaml
camera_config:
  pixel_width: 854
  pixel_height: 480
  frame_rate: 15
```

### For 4K Production

```yaml
camera_config:
  pixel_width: 3840
  pixel_height: 2160
  frame_rate: 60
```

### For Vertical Video (TikTok/Shorts)

```yaml
camera_config:
  pixel_width: 1080
  pixel_height: 1920
  frame_rate: 60
  frame_height: 14.222222222222221
  frame_width: 8.0
```

## Troubleshooting

### Config Not Loading

```bash
# Check which config is being used
manimgl scene.py MyScene --verbose

# Specify config explicitly
manimgl scene.py MyScene --config_file ./custom_config.yml
```

### Invalid Configuration

- Ensure YAML syntax is correct (indentation, colons, etc.)
- Check for typos in configuration keys
- Verify paths exist and are accessible
- Use quotes around paths with spaces

### Performance Issues

```yaml
# Reduce quality for testing
camera_config:
  pixel_width: 854
  pixel_height: 480
  frame_rate: 15

# Use temporary storage on SSD
directories:
  temporary_storage: "/path/to/fast/storage"
```
