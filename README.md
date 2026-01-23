# Manim Skills Repository

![Visitors](https://visitor-badge.laobi.icu/badge?page_id=adithya-s-k.manim_skill)
![GitHub stars](https://img.shields.io/github/stars/adithya-s-k/manim_skill?style=flat-square)
![GitHub forks](https://img.shields.io/github/forks/adithya-s-k/manim_skill?style=flat-square)
![GitHub issues](https://img.shields.io/github/issues/adithya-s-k/manim_skill?style=flat-square)
![License](https://img.shields.io/github/license/adithya-s-k/manim_skill?style=flat-square)

> **⚡ Quick Start:** Add both Manim skills to your AI agent instantly:
> ```bash
> npx skills add adithya-s-k/manim_skill
> ```

A comprehensive collection of best practices, patterns, and examples for both **Manim Community Edition** and **ManimGL** (3Blue1Brown's version). This repository provides battle-tested code examples and guidelines for creating mathematical animations.


https://github.com/user-attachments/assets/3cd398b7-7cc6-43c1-a6e9-20077be6b009


## 📚 About the Two Versions

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

> **Important**: These are **separate, incompatible** frameworks. Code written for one will not work with the other without modifications.

---

## 🚀 Installation

### Prerequisites (Both Versions)
1. **Python 3.7+** - Required
2. **FFmpeg** - For video encoding
3. **LaTeX** - For mathematical typesetting (TeX Live, MiKTeX, or MacTeX)

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

## 🔌 Skills.sh Integration

This repository provides two **AI Agent Skills** that can be installed with a single command using [skills.sh](https://skills.sh/):

### Install with npx (Recommended)

```bash
# Install Manim Community Edition best practices
npx skills add adithya-s-k/manim_skill/skills/manimce-best-practices

# Install ManimGL best practices
npx skills add adithya-s-k/manim_skill/skills/manimgl-best-practices

# Or install both
npx skills add adithya-s-k/manim_skill/skills/manimce-best-practices adithya-s-k/manim_skill/skills/manimgl-best-practices
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
│   └── manimgl-best-practices/     # ManimGL skills
│       ├── SKILL.md
│       └── rules/
│           ├── animations.md
│           ├── 3d.md
│           ├── camera.md
│           └── ...
│
└── tests/
    ├── manimce/                    # Tests for Community Edition
    └── manimgl/                    # Tests for ManimGL
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

> **Note**: Parallel testing with many workers can cause out-of-memory errors. Use 4-6 workers max, or test files individually.

---

## 🔍 Key Differences Between Versions

| Feature | Manim Community | ManimGL |
|---------|----------------|---------|
| **Import** | `from manim import *` | `from manimlib import *` |
| **CLI Command** | `manim` | `manimgl` |
| **Scene Base Class** | `Scene`, `MovingCameraScene` | `Scene`, `InteractiveScene` |
| **Creation Animation** | `Create()` | `ShowCreation()` |
| **Text Class** | `Text()`, `MathTex()` | `Text()`, `Tex()` |
| **3D Rendering** | Limited | Full OpenGL support |
| **Interactive Mode** | No | Yes (`-se` flag, `.embed()`) |
| **Camera Control** | `MovingCameraScene` | `self.camera.frame` |
| **Configuration** | Python config | YAML files |
| **Color Constants** | Same | Same + variations (e.g., `BLUE_A`, `BLUE_E`) |

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

**Note**: This license applies to the educational materials and code examples in this repository. The underlying Manim frameworks (Manim Community Edition and ManimGL) have their own respective licenses.

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

