---
name: config
description: m.config settings, resolution, frame rate and background color in ManimGX
metadata:
  tags: config, settings, resolution, pixel_width, pixel_height, frame_rate, background
---

# Configuration in ManimGX

Set scene-wide settings on `m.config` after the import. There is no `manim.cfg` and no
CLI config file.

## Common settings

```python
import manimgx as m

m.config.background_color = m.WHITE
m.config.pixel_width = 1280
m.config.pixel_height = 720
m.config.frame_rate = 30
```

- `background_color` — default `#000000` (black).
- `pixel_width` / `pixel_height` — output size; default 1920 × 1080.
- `frame_rate` — default 60.
- `frame_height` — the frame's short side in scene units; default 8.

## CLI overrides

`-r` and `--fps` override the file's settings for one render:

```bash
manimgx render scene.py -r 1280x720 --fps 30
```

## Tall video

```python
m.config.pixel_width = 1080
m.config.pixel_height = 1920
```

The frame's short side is still 8 units, so a tall frame is 8 wide and about 14.2 high.
Keep content inside x ∈ [-4, 4].

## Per-scene background

```python
class OnWhite(m.Scene):
    def setup(self):
        m.config.background_color = m.WHITE
```

Prefer `setup()` when only one scene should change the background.
