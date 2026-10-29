# Manim Skills Repository

![Visitors](https://visitor-badge.laobi.icu/badge?page_id=adithya-s-k.manim_skill)
![GitHub stars](https://img.shields.io/github/stars/adithya-s-k/manim_skill?style=flat-square)
![GitHub forks](https://img.shields.io/github/forks/adithya-s-k/manim_skill?style=flat-square)
![GitHub issues](https://img.shields.io/github/issues/adithya-s-k/manim_skill?style=flat-square)
![License](https://img.shields.io/github/license/adithya-s-k/manim_skill?style=flat-square)

> **⚡ Quick Start:** Add the Manim skills to your AI agent instantly:
> ```bash
> npx skills add adithya-s-k/manim_skill
> ```

A comprehensive collection of best practices, patterns, and examples for **Manim Community Edition**, **ManimGL** (3Blue1Brown's version), and **ManimGX** (the Rust + wgpu engine for agents). This repository provides battle-tested code examples and guidelines for creating mathematical animations.


https://github.com/user-attachments/assets/3cd398b7-7cc6-43c1-a6e9-20077be6b009


## 📚 About the Versions

### Manim Community Edition (`manim`)
- **Repository**: https://github.com/ManimCommunity/manim
- **Focus**: Community-maintained, stable, well-documented
- **Best For**: Production use, educational content, collaborative projects
- **Command**: `manim` CLI
- **Import**: `from manim import *`

### ManimGL (`manimgl`)
- **Repository**: https://github.com/3b1b/manim
- **Focus**: Grant Sanderson's (3Blue1Brown) original version with OpenGL rendering
- **Best For**: Interactive development, 3D scenes, rapid prototyping
- **Command**: `manimgl` CLI
- **Import**: `from manimlib import *`

### ManimGX (`manimgx`)
- **Repository**: https://github.com/academa-labs/manimgx
- **Focus**: A Rust + wgpu engine that speaks Manim CE's API; Typst typesetting, fast 3D, and `manimgx inspect` for agent feedback
- **Best For**: Fast renders, 3D, and agent-driven workflows
- **Command**: `manimgx` CLI
- **Import**: `import manimgx as m` or `from manimgx import *`

> **Important**: These are **separate frameworks** with different behavior. Code written for one will not always work with another without modifications. ManimGX keeps CE's API names but decides how they behave; see `skills/manimgx-best-practices/rules/differences.md`.

---

## 🚀 Installation

### Prerequisites (Manim Community Edition and ManimGL)
1. **Python 3.7+** - Required
2. **FFmpeg** - For video encoding
3. **LaTeX** - For mathematical typesetting (TeX Live, MiKTeX, or MacTeX)

> **ManimGX** needs none of these: install it with Python 3.13+ and it brings its own typesetting and encoder. See [Installing ManimGX](#installing-manimgx).

#### Install FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html and add to PATH

#### Install LaTeX

**macOS:**
```bash
brew install mactex
```

**Ubuntu/Debian:**
```bash
sudo apt install texlive-full
```

**Windows:**
Install MiKTeX from https://miktex.org/download

---

### Installing Manim Community Edition

```bash
# Using pip
pip install manim

# Using uv (recommended for this project)
uv pip install manim

# Verify installation
manim --version
```

**Documentation**: https://docs.manim.community/

---

### Installing ManimGL

```bash
# Using pip
pip install manimgl

# Using uv (recommended for this project)
uv pip install manimgl

# Verify installation
manimgl --version
```

**Additional macOS (ARM) requirement:**
```bash
arch -arm64 brew install pkg-config cairo
```

---

### Installing ManimGX

```bash
# Using uv (recommended; installs Python 3.13 if needed)
uv tool install --python 3.13 manimgx

# Using pip in a Python 3.13+ virtual environment
python3.13 -m venv .venv && .venv/bin/pip install manimgx

# Verify installation
manimgx --version
```

ManimGX does not need LaTeX, FFmpeg, or a plugin system: Typst typesets the text and math,
and the wheel encodes the video. It draws on the GPU (Metal, Direct3D 12, Vulkan) and falls
back to CPU rendering when there is none.

**Documentation**: https://manimgx.academa.ai/

---

## 🔌 Skills.sh Integration

This repository provides three **AI Agent Skills** that can be installed with a single command using [skills.sh](https://skills.sh/):

### Install with npx (Recommended)

```bash
# Install Manim Community Edition best practices
npx skills add adithya-s-k/manim_skill/skills/manimce-best-practices

# Install ManimGL best practices
npx skills add adithya-s-k/manim_skill/skills/manimgl-best-practices

# Install ManimGX best practices
npx skills add adithya-s-k/manim_skill/skills/manimgx-best-practices

# Or install all
npx skills add adithya-s-k/manim_skill/skills/manimce-best-practices adithya-s-k/manim_skill/skills/manimgl-best-practices adithya-s-k/manim_skill/skills/manimgx-best-practices
```

### What are Skills?

Skills are **reusable capabilities for AI coding agents**. Once installed, your AI assistant (like Claude, GitHub Copilot, or Cursor) automatically gains access to:
- ✅ Domain-specific best practices
- ✅ Working code examples
- ✅ Common patterns and anti-patterns
- ✅ Framework-specific knowledge

The skills follow the [Agent Skills open standard](https://github.com/anthropics/skills) and work across multiple AI tools.

### When Skills Activate

**manimce-best-practices** - Automatically loads when:
- You import `from manim import *`
- You use the `manim` CLI command
- You work with Scene classes, mathematical animations, or LaTeX rendering
- You create educational videos or visual explanations with Manim Community

**manimgl-best-practices** - Automatically loads when:
- You import `from manimlib import *`
- You use the `manimgl` CLI command
- You work with InteractiveScene, 3D rendering, or camera frame control
- You use interactive mode with `.embed()` or `checkpoint_paste()`

**manimgx-best-practices** - Automatically loads when:
- You import `manimgx` (`import manimgx as m` or `from manimgx import *`)
- You use the `manimgx` CLI (`render`, `inspect`, `present`)
- You work with Typst text/math, `Scene` camera frames, 3D scenes, or `manimgx inspect`
- You need ManimGX's behavior where it differs from Manim CE

---

## 📖 Using This Repository

### Repository Structure

```
manim_skill/
├── skills/
│   ├── manimce-best-practices/     # Manim Community Edition skills
│   │   ├── SKILL.md                # Skill metadata
│   │   └── rules/                  # Individual best practice guides
│   │       ├── animations.md
│   │       ├── scenes.md
│   │       ├── mobjects.md
│   │       └── ...
│   │
│   ├── manimgl-best-practices/     # ManimGL skills
│   │   ├── SKILL.md
│   │   └── rules/
│   │       ├── animations.md
│   │       ├── 3d.md
│   │       ├── camera.md
│   │       └── ...
│   │
│   └── manimgx-best-practices/     # ManimGX skills
│       ├── SKILL.md
│       └── rules/
│           ├── differences.md
│           ├── scenes.md
│           ├── latex.md
│           └── ...
│
└── tests/
    ├── manimce/                    # Tests for Community Edition
    ├── manimgl/                    # Tests for ManimGL
    └── manimgx/                    # Tests for ManimGX
```

### What's Inside Each Skill File?

Each `.md` file contains:
- **Best practices** for specific Manim features
- **Working code examples** (all tested!)
- **Common patterns** and use cases
- **Pitfalls to avoid**
- **API differences** between versions

---

## 🎯 Quick Start Examples

### Manim Community Edition

```python
from manim import *

class BasicExample(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)

        self.play(Create(circle))
        self.wait()
```

**Run it:**
```bash
manim -pql scene.py BasicExample
# -p: preview after rendering
# -q: quality (l=low, m=medium, h=high)
```

### ManimGL

```python
from manimlib import *

class BasicExample(InteractiveScene):
    def construct(self):
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)

        self.play(ShowCreation(circle))
        self.wait()
```

**Run it:**
```bash
manimgl scene.py BasicExample --write_file
# --write_file: save video output
# -s: skip to last frame
# -w: write file without opening
```

### ManimGX

```python
import manimgx as m

class BasicExample(m.Scene):
    def construct(self):
        circle = m.Circle()
        circle.set_fill(m.BLUE, opacity=0.5)
        circle.set_stroke(m.BLUE_E, width=4)

        self.play(m.Create(circle))
        self.wait()
```

**Run it:**
```bash
manimgx render scene.py BasicExample
# Writes BasicExample.mp4 and a storyboard beside the file
# Add -r 1280x720 --fps 30 for a quick draft
# manimgx inspect scene.py checks layout before you render
```

---

## 🧪 Running Tests

This repository includes comprehensive tests to ensure all code examples work correctly.

### Test Manim Community Edition Skills

```bash
# Test all files
uv run python tests/manimce/test_all_skills.py

# Test specific file
uv run python tests/manimce/test_all_skills.py animations.md

# Run with multiple workers (faster)
uv run python tests/manimce/test_all_skills.py -j 4
```

### Test ManimGL Skills

```bash
# Test all files
uv run python tests/manimgl/test_all_skills.py

# Test specific file
uv run python tests/manimgl/test_all_skills.py 3d.md

# Run with multiple workers (use caution - can cause OOM)
uv run python tests/manimgl/test_all_skills.py -j 4
```

### Test ManimGX Skills

```bash
# Test all files (uses `manimgx` on PATH, or `uv run --with manimgx`)
python3 tests/manimgx/test_all_skills.py

# Test specific file
python3 tests/manimgx/test_all_skills.py latex.md

# Run with multiple workers
python3 tests/manimgx/test_all_skills.py -j 4
```

> **Note**: Parallel testing with many workers can cause out-of-memory errors. Use 4-6 workers max, or test files individually.

---

## 🔍 Key Differences Between Versions

| Feature | Manim Community | ManimGL | ManimGX |
|---------|----------------|---------|---------|
| **Import** | `from manim import *` | `from manimlib import *` | `import manimgx as m` / `from manimgx import *` |
| **CLI Command** | `manim` | `manimgl` | `manimgx` |
| **Scene Base Class** | `Scene`, `MovingCameraScene` | `Scene`, `InteractiveScene` | `Scene`, `ThreeDScene` |
| **Creation Animation** | `Create()` | `ShowCreation()` | `Create()` |
| **Text Class** | `Text()`, `MathTex()` | `Text()`, `Tex()` | `Text()`, `MathTex()` (Typst) |
| **3D Rendering** | Limited | Full OpenGL support | Full GPU support (wgpu) |
| **Interactive Mode** | No | Yes (`-se` flag, `.embed()`) | No |
| **Camera Control** | `MovingCameraScene` | `self.camera.frame` | `self.camera.frame` (every `Scene`) |
| **Configuration** | Python config | YAML files | `m.config` |
| **Color Constants** | Same | Same + variations (e.g., `BLUE_A`, `BLUE_E`) | Same |

ManimGX also has a layout-checking `inspect` command that ManimCE and ManimGL do not; see
`skills/manimgx-best-practices/rules/inspect.md`.

---

## 📚 Exploring Skills

### For Manim Community Edition:
Start with these guides in `skills/manimce-best-practices/rules/`:
1. **scenes.md** - Scene structure and lifecycle
2. **animations.md** - Basic animation patterns
3. **mobjects.md** - Creating and manipulating objects
4. **colors.md** - Color systems and styling
5. **text.md** - Text and LaTeX rendering

### For ManimGL:
Start with these guides in `skills/manimgl-best-practices/rules/`:
1. **scenes.md** - Scene types and InteractiveScene
2. **animations.md** - Animation fundamentals
3. **camera.md** - Camera movement and 3D orientation
4. **3d.md** - 3D object creation and rendering
5. **interactive.md** - Interactive development workflow

### For ManimGX:
Start with these guides in `skills/manimgx-best-practices/rules/`:
1. **differences.md** - ManimGX vs Manim CE (read first)
2. **scenes.md** - Scene structure and per-frame time
3. **latex.md** - MathTex/Tex with Typst
4. **inspect.md** - Storyboard and layout checks
5. **camera.md** - Moving camera and 3D

---

## 🤝 Contributing

Found an issue with an example? Want to add a new best practice?

1. Ensure your code example works with the target Manim version
2. Add it to the appropriate skill file
3. Run the tests to verify: `uv run python tests/<version>/test_all_skills.py <filename>`
4. Submit a pull request

---

## 📄 License

This repository is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Note**: This license applies to the educational materials and code examples in this repository. The underlying Manim frameworks (Manim Community Edition, ManimGL, and ManimGX) have their own respective licenses.

---

## 🔗 Resources

### Manim Community Edition
- **Documentation**: https://docs.manim.community/
- **Discord**: https://www.manim.community/discord/
- **GitHub**: https://github.com/ManimCommunity/manim

### ManimGL
- **Documentation**: https://3b1b.github.io/manim/
- **GitHub**: https://github.com/3b1b/manim
- **Tutorial Videos**: Grant's YouTube channel

### ManimGX
- **Documentation**: https://manimgx.academa.ai/
- **GitHub**: https://github.com/academa-labs/manimgx
- **Agent guide**: https://manimgx.academa.ai/llms.txt
- **Gallery**: https://manimgx.academa.ai/gallery/

### General
- **3Blue1Brown**: https://www.youtube.com/@3blue1brown
- **Manim Community**: https://www.manim.community/

---

## ⚠️ Troubleshooting

### Common Issues

**"Command not found: manim/manimgl"**
- Verify installation: `pip list | grep manim`
- Check PATH configuration
- Try: `python -m manim` or `python -m manimlib`

**LaTeX errors**
- Install full LaTeX distribution (not basic)
- ManimCE: Try `manim --tex_template <template>` with different templates
- ManimGL: Check `custom_defaults.yml` for LaTeX configuration

**Video won't play**
- Install media codecs for your OS
- Try different quality settings (`-ql`, `-qm`, `-qh`)
- Check FFmpeg installation: `ffmpeg -version`

**Out of Memory (parallel tests)**
- Reduce worker count: `-j 2` or `-j 4`
- Test files individually
- Close other applications

**Import errors / wrong version**
- Check you're importing the right version:
  - `from manim import *` → Manim Community
  - `from manimlib import *` → ManimGL
- Uninstall conflicting versions: `pip uninstall manim manimgl manimlib`
- Reinstall the version you need

---

## 🙏 Acknowledgments

This repository exists thanks to the incredible work of:

### Grant Sanderson (3Blue1Brown)
Creator of the original **Manim** animation engine and the **3Blue1Brown** YouTube channel. Grant's pioneering work in mathematical visualization has inspired millions of learners worldwide and created an entirely new paradigm for explaining complex concepts through programmatic animation. His commitment to open-source education and visual storytelling has fundamentally changed how mathematics is taught and understood.

**Website**: https://www.3blue1brown.com/
**YouTube**: https://www.youtube.com/@3blue1brown
**Manim (ManimGL)**: https://github.com/3b1b/manim

### The Manim Community
The dedicated team and contributors who maintain **Manim Community Edition**, ensuring the framework remains accessible, well-documented, and actively developed. Their tireless efforts in creating comprehensive documentation, managing community support, and continuously improving the codebase have made mathematical animation accessible to educators, students, and creators everywhere.

**Website**: https://www.manim.community/
**GitHub**: https://github.com/ManimCommunity/manim
**Discord**: https://www.manim.community/discord/

---

### Standing on the Shoulders of Giants

Both frameworks represent countless hours of development, documentation, community support, and creative problem-solving. This repository simply aims to organize and share knowledge about these powerful tools. All credit for the underlying technology goes to Grant Sanderson and the Manim Community contributors.

Thank you for making mathematical beauty programmable and accessible to all. 🎓✨

