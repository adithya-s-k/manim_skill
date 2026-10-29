---
name: cli
description: manimgx render, inspect and present commands and their flags
metadata:
  tags: cli, render, inspect, present, resolution, fps, command
---

# ManimGX CLI

ManimGX's CLI is `manimgx`. It writes files beside the scene file and prints what it wrote.

```bash
manimgx render  scene.py [Scene]   # MP4 + storyboard + subtitles
manimgx inspect scene.py [Scene]   # timeline + layout checks + storyboard, no video
manimgx present scene.py [Scene]   # video as slides in the browser
```

## render

```bash
manimgx render scene.py                  # 1920×1080 at 60 fps
manimgx render scene.py MyScene          # pick a scene in a multi-scene file
manimgx render scene.py -r 1280x720 --fps 30   # quick draft
manimgx render scene.py -o out.mp4       # rename the output
```

- `-r WxH` / `--fps N` override the scene's `m.config`.
- `render` also writes `<Scene>.storyboard.png` and, if the scene has captions or a voice, a
  `.srt`.
- Errors print the failing line and often a rename hint.

## inspect

```bash
manimgx inspect scene.py
manimgx inspect scene.py -t 1.5,end
manimgx inspect scene.py -o detail.png
```

See [inspect.md](inspect.md) for what it checks.

## present

`self.next_section("name", notes="...")` starts a slide; `present` renders the video and opens
a page that stops at each section. Only use it when the task asks for a presentation.

## Quality flags

There are no `-ql`/`-qm`/`-qh` flags. Resolution and frame rate are explicit:

| Quality | Flags |
| --- | --- |
| Draft | `-r 854x480 --fps 15` |
| Default | `-r 1920x1080 --fps 60` |
| High | `-r 1920x1080 --fps 60` |
| 4K | `-r 3840x2160 --fps 60` |
