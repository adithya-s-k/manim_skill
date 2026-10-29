---
name: positioning
description: move_to, next_to, align_to, shift, to_edge and to_corner in ManimGX
metadata:
  tags: position, move_to, next_to, shift, align_to, edge, corner, layout
---

# Positioning in ManimGX

The frame is centred on the origin. x goes left→right, y goes down→up; points are
`[x, y, 0]`.

## shift

```python
circle.shift(m.RIGHT * 2)
circle.shift(m.UP + m.RIGHT)
circle.shift(m.LEFT).shift(m.DOWN)
```

## move_to

```python
circle.move_to(m.ORIGIN)
circle.move_to(m.RIGHT * 3 + m.UP)
circle.move_to(other)              # centre of another mobject
circle.move_to(other.get_top())
```

## next_to

```python
circle.next_to(square, m.RIGHT)
circle.next_to(square, m.DOWN, buff=0.5)
circle.next_to(square, m.RIGHT, aligned_edge=m.UP)
```

## align_to

```python
circle.align_to(square, m.LEFT)
circle.align_to(square, m.UP)
```

## Edges and corners

```python
title = m.Text("Title").to_edge(m.UP)
note = m.Text("note").to_edge(m.DOWN, buff=1)
logo = m.Square().to_corner(m.UL)
```

## Getting positions

```python
circle.get_center()
circle.get_top()      # edge centres: get_bottom(), get_left(), get_right()
circle.get_corner(m.UL)
circle.get_start()    # start/end of a path
circle.get_end()
```

## Animated positioning

```python
self.play(square.animate.shift(m.RIGHT * 2))
self.play(square.animate.move_to(m.UP * 2))
self.play(square.animate.to_edge(m.LEFT))
```

## Safe area

Keep important content inside x ∈ [-7.1, 7.1], y ∈ [-4, 4] for 16:9. For a tall 9:16 video
the frame is 8 wide; keep everything inside x ∈ [-4, 4] there.
