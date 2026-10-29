---
name: errors
description: Common ManimGX errors, rename hints, and the repair-and-retry loop
metadata:
  tags: errors, debugging, retry, rename, typst, typeset
---

# Errors and the repair loop

ManimGX errors print the scene's line that failed and, for a wrong name, a hint. Treat the
error text as data: read it, apply the hint, and only then resend.

## The loop

1. Write the scene, keep the API surface small (common objects + animations).
2. Render. If it fails, read the error message and the failing line.
3. Fix the specific cause. Do **not** resend identical code.
4. Re-render; repeat, but stop after a few attempts and simplify the scene if it keeps failing.

## Rename hints

ManimGX keeps one canonical name per concept; the CE name still resolves but is deprecated.
The error often tells you the canonical name:

- `ShowCreation is Create in ManimGX` — use `Create`.
- `MovingCameraScene` — use `Scene` (every scene's camera moves).
- `ApplyMethod` / `ScaleInPlace` / `FadeToColor` — use `.animate`.
- `arrange_submobjects` — use `arrange`.

## Typesetting failures

- A LaTeX string that doesn't typeset is usually a macro Typst can't convert. Remove the
  package/macro and use standard symbols. Never add `\usepackage` or `TexTemplate` — that
  path does not exist in ManimGX.
- CJK inside `MathTex` fails. Move Chinese to `Text` and place it next to the formula.
- If a formula is still failing, break it into smaller `MathTex` pieces.

## API failures

- "… is not a name in ManimGX" or a wrong keyword: check spelling, or that you're not using
  a CE submodule (`manim.utils.*`). Everything is on the package: `m.Circle`, `m.MathTex`.
- A misspelled keyword is often silently ignored at runtime; only a type checker (`ty`)
  catches it before render. If the render succeeds but looks wrong, check keyword spelling.
- `no GPU adapter` means the command ran in a sandbox that hides the GPU; run outside the
  sandbox (or let it fall back to CPU — the Linux wheels bundle a software renderer).

## Layout problems (from `inspect`)

These are not crashes: the scene renders, but content is clipped, overlapping, or too small.
Fix by shrinking, repositioning (`next_to`, `to_edge` with `buff`), or shortening text, then
re-inspect. Keep everything inside x∈[-7.1, 7.1], y∈[-4, 4] for 16:9.
