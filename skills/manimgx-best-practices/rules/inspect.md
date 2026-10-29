---
name: inspect
description: manimgx inspect, storyboard, layout problems and the fix-and-re-inspect loop
metadata:
  tags: inspect, storyboard, layout, clipping, overlap, debug, feedback
---

# Inspecting a scene

`manimgx inspect` is ManimGX's agent feedback loop: it runs the scene without encoding video
and reports what is visually wrong.

## Command

```bash
manimgx inspect scene.py
manimgx inspect scene.py -t 1.5,end     # specific moments: seconds, or 'end'
manimgx inspect scene.py MyScene        # pick a scene in a multi-scene file
```

## What it checks

For 2D scenes:

- a mobject the frame cuts off;
- texts that cover each other, a line through a text, or a fill over it;
- text too small to read.

Each problem names the mobject as your code names it and is outlined and numbered in
`<Scene>.storyboard.png`. Layout problems exit with code 1; notes (like a graph leaving the
frame) do not. 3D scenes get pictures and a timeline, with layout checks skipped.

## Sample report

```
crowded.py: Crowded, 3.00 s, 2 plays
storyboard: Crowded.storyboard.png
  #0   0.00– 2.00s  crowded.py:8  Write(Text 'A title much too long for t…')
  #1   2.00– 3.00s  crowded.py:9  FadeIn(Text 'a note')
layout: 2 problems
  [1] t=2–3s (crowded.py:8)  title (...): 1.35 past the left edge, 1.35 past the right edge
  [2] t=3s (crowded.py:9)  title (...) and note (...): texts overlap
```

## The loop

1. Write the scene.
2. `inspect` it; read the timeline and every layout problem.
3. Fix each problem: shrink, reposition (`next_to`, `to_edge` with `buff`), or shorten text.
4. Re-inspect until it is clean.
5. `render` and check the video.

`inspect` checks only the sampled moments, not every frame. Add `-t` for moments that matter.
